#!/usr/bin/env python3
"""Collect public video evidence without authentication or invented transcription.

Default is --frames 0: metadata and subtitle capture only. The video itself is
never downloaded and ffmpeg is never invoked unless --frames N (N > 0) is given
explicitly. Subtitle languages default to zh.* and en.*; extend with --sub-langs.
Every external subprocess is bounded by a per-stage timeout and the remaining
total budget, so a stalled platform never blocks the run forever. Failures keep
the concrete stage, elapsed time and a resume hint; partial evidence (metadata,
transcript) is kept and usable on its own.
"""
import argparse
import datetime as dt
import importlib.util
import json
import shutil
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

DEFAULT_SUB_LANGS = ['zh.*', 'en.*']


def run(command, timeout=None):
    try:
        r = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError('command timed out after %.0fs' % (timeout or 0))
    if r.returncode:
        raise RuntimeError(r.stderr[-2000:] or r.stdout[-2000:] or 'exit %d' % r.returncode)
    return r.stdout


def ytdlp_command():
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    if importlib.util.find_spec("yt_dlp") is not None:
        return [sys.executable, "-m", "yt_dlp"]
    raise RuntimeError("yt-dlp CLI/module unavailable; supply authorized transcript/screenshots")


def ffprobe_duration(path, timeout=None):
    if not shutil.which("ffprobe"):
        return None
    try:
        value = run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ], timeout=timeout).strip()
        return float(value)
    except Exception:
        return None


def collect(url, out, frames=0, fixture=None, sub_langs=None, timeout=30, total_budget=180,
            retries=0, extractor_retries=0):
    timeout = float(timeout)
    total_budget = float(total_budget)
    if timeout <= 0 or total_budget <= 0:
        raise ValueError('timeout and total_budget must be > 0')
    # A per-stage timeout may exceed the total budget on purpose: every subprocess
    # is capped by min(stage_timeout, remaining_budget), so the budget always wins.
    if not 0 <= int(frames) <= 30:
        raise ValueError('frames must be 0..30')
    frames = int(frames)
    retries = int(retries)
    extractor_retries = int(extractor_retries)
    if retries < 0 or extractor_retries < 0:
        raise ValueError('retries and extractor_retries must be >= 0')
    if sub_langs is None:
        sub_langs = list(DEFAULT_SUB_LANGS)
    if not sub_langs or not all(isinstance(s, str) and s.strip() for s in sub_langs):
        raise ValueError('sub_langs must be a non-empty list of language patterns')
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    result = dict(url=url, fixture=fixture is not None, collected_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                  elapsed_seconds=None, metadata={}, transcript_status='missing', transcript=[], frames=[],
                  evidence=[], failures=[])

    def remaining():
        return total_budget - (time.monotonic() - started)

    def stage_timeout():
        return max(0.0, min(timeout, remaining()))

    def failure(stage, exc, resume=None):
        result['failures'].append({'stage': stage, 'error': str(exc),
                                   'elapsed_seconds': round(time.monotonic() - started, 3),
                                   'resume': resume})

    if urllib.parse.urlparse(url).scheme not in ('https', 'http'):
        failure('input', 'Only public HTTP(S) URLs accepted')
        result['elapsed_seconds'] = round(time.monotonic() - started, 3)
        return result
    budget = stage_timeout()
    if budget <= 0:
        failure('metadata', 'total budget exhausted before metadata stage', resume='increase --total-budget and rerun')
        result['elapsed_seconds'] = round(time.monotonic() - started, 3)
        return result
    if fixture is not None:
        info = fixture['metadata']
    else:
        try:
            downloader = ytdlp_command()
        except RuntimeError as exc:
            failure('dependency', exc, resume='supply authorized transcript/screenshots; tool installation requires separate authorization')
            result['elapsed_seconds'] = round(time.monotonic() - started, 3)
            return result
        cmd = downloader + ['--ignore-config', '--no-playlist',
                                 '--socket-timeout', str(int(timeout)),
                                 '--retries', str(retries),
                                 '--extractor-retries', str(extractor_retries),
                                 '--skip-download', '--write-info-json', '--write-subs', '--write-auto-subs',
                                 '--sub-langs', ','.join(sub_langs), '--sub-format', 'json3',
                                 '-o', str(out / 'video.%(ext)s'), '--', url]
        try:
            run(cmd, timeout=budget)
        except Exception as exc:
            # Metadata+subtitles is one command; it can fail after usable outputs
            # were already written (e.g. one subtitle language failing). Keep any
            # readable info.json and saved subtitle files, and record the failure.
            failure('metadata', exc, resume='reuse any saved evidence; supply authorized transcript/screenshots if access is restricted; increase budget only for a genuine timeout')
        info_path = out / 'video.info.json'
        if not info_path.exists():
            result['elapsed_seconds'] = round(time.monotonic() - started, 3)
            return result
        try:
            info = json.loads(info_path.read_text())
        except Exception as exc:
            failure('metadata', exc, resume='supply authorized transcript/screenshots with timestamps')
            result['elapsed_seconds'] = round(time.monotonic() - started, 3)
            return result
    keys = ('id', 'title', 'uploader', 'uploader_id', 'channel', 'description', 'duration', 'thumbnail',
            'upload_date', 'timestamp', 'extractor_key', 'webpage_url', 'chapters', 'subtitles',
            'automatic_captions', 'is_live')
    result['metadata'] = {k: info.get(k) for k in keys}
    result['evidence'].append({'source': url, 'kind': 'metadata', 'timestamp': None,
                               'artifact': 'fixture' if fixture is not None else str(out / 'video.info.json')})
    subtitle_files = [] if fixture is not None else sorted(out.glob('video.*.json3'))
    for path in subtitle_files:
        try:
            segments = []
            for event in json.loads(path.read_text()).get('events', []):
                text = ''.join(s.get('utf8', '') for s in event.get('segs', [])).strip()
                if text:
                    segments.append({'start_seconds': event.get('tStartMs', 0) / 1000, 'text': text,
                                     'source': str(path), 'kind': 'subtitle_or_auto_caption',
                                     'language': path.name[len('video.'):-len('.json3')]})
            result['transcript'].extend(segments)
        except Exception as exc:
            failure('subtitle_parse', exc)
    if fixture is not None:
        result['transcript'] = fixture.get('transcript', [])
    if result['transcript']:
        result['transcript_status'] = 'available'
        result['evidence'].extend({'source': s.get('source', 'fixture'), 'kind': 'transcript',
                                   'timestamp_seconds': s['start_seconds'], 'excerpt': s['text']}
                                  for s in result['transcript'])
        (out / 'transcript.txt').write_text('\n'.join('[%s] %s' % (format(s['start_seconds'], '.3f'), s['text']) for s in result['transcript']))
    else:
        failure('transcript', 'No readable subtitles; no transcription generated',
                resume='supply authorized transcript or captions with timestamps, or rerun with more --sub-langs')
    if frames and fixture is None:
        if result['metadata'].get('is_live'):
            failure('frames', 'Live stream (is_live=true): uniform time sampling not applicable',
                    resume='provide authorized timestamped screenshots; transcript/metadata above remain usable')
        else:
            try:
                budget = stage_timeout()
                if budget <= 0:
                    raise RuntimeError('total budget exhausted before frames stage')
                if not shutil.which('ffmpeg'):
                    raise RuntimeError('ffmpeg unavailable; ask for timestamped screenshots')
                cmd = ytdlp_command() + ['--ignore-config', '--no-playlist',
                                         '--socket-timeout', str(int(timeout)),
                                         '--retries', str(retries),
                                         '--extractor-retries', str(extractor_retries),
                                         '--max-filesize', '500M', '-f', 'worst[ext=mp4]/worst',
                                         '-o', str(out / 'source.%(ext)s'), '--', url]
                run(cmd, timeout=budget)
                videos = [p for p in out.glob('source.*') if p.suffix not in ('.part', '.ytdl')]
                if not videos:
                    raise RuntimeError('Video download unavailable or exceeds size limit')
                duration = result['metadata'].get('duration') or ffprobe_duration(videos[0], timeout=stage_timeout())
                if not duration or float(duration) <= 0:
                    raise RuntimeError('Finite duration required for uniform sampling')
                result['metadata']['duration'] = float(duration)
                for i in range(frames):
                    budget = stage_timeout()
                    if budget <= 0:
                        raise RuntimeError('total budget exhausted; extracted %d/%d frames' % (i, frames))
                    timestamp = float(duration) * (i + 0.5) / frames
                    image = out / ('frame-%02d.jpg' % (i + 1))
                    run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', str(timestamp),
                         '-i', str(videos[0]), '-frames:v', '1', str(image)], timeout=budget)
                    if not image.exists():
                        raise RuntimeError('Frame not produced')
                    result['frames'].append({'source': url, 'timestamp_seconds': round(timestamp, 3),
                                             'path': str(image), 'visual_review': 'pending'})
            except Exception as exc:
                failure('frames', exc,
                        resume='reuse this metadata/transcript; rerun with explicit --frames N and larger --total-budget, or supply timestamped screenshots')
    result['elapsed_seconds'] = round(time.monotonic() - started, 3)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('url')
    p.add_argument('--output-dir', required=True, type=Path)
    p.add_argument('--frames', type=int, default=0,
                   help='frames to extract; 0 (default) means metadata/subtitles only, no video download, no ffmpeg')
    p.add_argument('--sub-langs', nargs='+', default=None,
                   help='subtitle language patterns, e.g. zh.* en.* (default: zh.* en.*)')
    p.add_argument('--timeout', type=float, default=30.0, help='per-stage timeout in seconds (default 30)')
    p.add_argument('--total-budget', type=float, default=180.0, help='total wall-clock budget in seconds (default 180)')
    p.add_argument('--retries', type=int, default=0, help='yt-dlp --retries (default 0, no automatic retry)')
    p.add_argument('--extractor-retries', type=int, default=0, help='yt-dlp --extractor-retries (default 0)')
    p.add_argument('--fixture', type=argparse.FileType('r'))
    p.add_argument('--summary', action='store_true', help='print artifact locations and counts rather than full metadata/transcript')
    a = p.parse_args()
    if not 0 <= a.frames <= 30:
        p.error('--frames must be 0..30')
    if a.timeout <= 0 or a.total_budget <= 0:
        p.error('--timeout and --total-budget must be > 0')
    if a.retries < 0 or a.extractor_retries < 0:
        p.error('--retries and --extractor-retries must be >= 0')
    # New directory prevents stale captions from contaminating another video.
    if a.output_dir.exists() and any(a.output_dir.iterdir()):
        p.error('--output-dir must be empty or new')
    result = collect(a.url, a.output_dir, a.frames, json.load(a.fixture) if a.fixture else None,
                     sub_langs=a.sub_langs, timeout=a.timeout, total_budget=a.total_budget,
                     retries=a.retries, extractor_retries=a.extractor_retries)
    (a.output_dir / 'evidence.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    displayed = result
    if a.summary:
        displayed = {k: result[k] for k in ('url', 'fixture', 'elapsed_seconds', 'transcript_status', 'failures')}
        displayed.update(title=result['metadata'].get('title'),
                         transcript_segments=len(result['transcript']), frames=len(result['frames']),
                         evidence_file=str(a.output_dir / 'evidence.json'))
    print(json.dumps(displayed, ensure_ascii=False, indent=2))
    return 2 if not result['metadata'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
