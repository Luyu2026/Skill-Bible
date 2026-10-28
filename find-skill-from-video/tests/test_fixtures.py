#!/usr/bin/env python3
"""Offline synthetic behavioral tests. Never evidence of real video/API success."""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compose = load_script('compose_result').compose


def no_token_env():
    return {**os.environ, 'GITHUB_TOKEN': '', 'GH_TOKEN': ''}


def original_case():
    url = 'https://github.com/example/demo-skill/blob/fixture/SKILL.md'
    return {'fixture': True, 'video': {'url': 'https://example.invalid/video', 'content_reviewed': True},
            'evidence': [
                {'id': 'v1', 'kind': 'video_frame', 'source': 'https://example.invalid/video', 'timestamp_seconds': 130,
                 'excerpt': 'Synthetic frame shows example/demo-skill SKILL.md', 'verified': True},
                {'id': 'u1', 'kind': 'upstream_skill', 'source': url, 'timestamp_seconds': None,
                 'excerpt': 'Synthetic name: demo-skill; demo workflow', 'verified': True},
                {'id': 'a1', 'kind': 'identity_corroboration', 'source': 'https://example.invalid/author',
                 'timestamp_seconds': None, 'excerpt': 'Synthetic creator attribution agrees', 'verified': True}],
            'candidates': [{'name': 'demo-skill', 'url': url, 'author': 'example', 'classification': 'confirmed_original',
                            'availability': 'available', 'skill_file_url': url, 'license': 'MIT (synthetic)',
                            'identity_score': 100, 'capability_similarity': 100, 'identity_evidence': ['v1', 'u1', 'a1'],
                            'capability_evidence': ['u1'], 'gaps': []}],
            'limitations': ['Synthetic evidence only; not a live verification'], 'next_action': 'Open synthetic fixture for inspection'}


class Fixtures(unittest.TestCase):
    def test_other_video_is_not_identity_anchor(self):
        data = original_case()
        data['evidence'][0]['source'] = 'https://example.invalid/another-video'
        result = compose(data)
        self.assertEqual(result['status'], 'needs_more_evidence')
        self.assertEqual(result['original'], [])
        self.assertEqual(result['leads'][0]['classification'], 'unverified_lead')

    def test_resolved_video_url_and_unverified_frame(self):
        data = original_case()
        data['video']['resolved_url'] = 'https://example.invalid/resolved?id=one'
        data['evidence'][0]['source'] = 'https://example.invalid/resolved?id=one'
        self.assertEqual(compose(data)['status'], 'original_found')
        data['evidence'][0]['source'] = 'https://example.invalid/resolved?id=other'
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')
        data['evidence'][0]['source'] = 'https://example.invalid/resolved?id=one'
        data['evidence'][0]['verified'] = False
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')

    def test_collection_not_complete_from_one_or_duplicate_file(self):
        data = original_case()
        data['video']['expected_count'] = 6
        data['candidates'].append(copy.deepcopy(data['candidates'][0]))
        result = compose(data)
        self.assertEqual(result['coverage'], {'expected_count': 6, 'confirmed_file_count': 1, 'complete': False})

    def test_conflicting_candidate_cannot_be_kept_as_lead(self):
        data = original_case()
        data['candidates'][0]['conflicts'] = ['Different creator; no migration evidence']
        result = compose(data)
        self.assertEqual(result['original'], [])
        self.assertEqual(result['leads'], [])

    def test_native_video_body_without_timestamp(self):
        data = original_case()
        data['evidence'][0].update(kind='video_extract', timestamp_seconds=None,
                                  method='synthetic-native-video-tool', verified=True, content_level='body')
        self.assertEqual(compose(data)['status'], 'original_found')
        data['evidence'] = data['evidence'][:2]
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')

    def test_native_video_metadata_not_body_evidence(self):
        data = original_case()
        for change in ({'content_level': 'metadata'}, {'verified': False}, {'method': ''},
                       {'source': 'https://example.invalid/other-video'}):
            case = copy.deepcopy(data)
            case['evidence'][0].update(kind='video_extract', timestamp_seconds=None,
                                      method='synthetic-native-video-tool', verified=True, content_level='body')
            case['evidence'][0].update(change)
            self.assertEqual(compose(case)['status'], 'needs_more_evidence')

    def test_original_and_missing_anchor(self):
        data = original_case()
        self.assertEqual(compose(data)['status'], 'original_found')
        data['evidence'].pop()
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')
        data['candidates'][0]['classification'] = 'probable_original'
        data['candidates'][0]['gaps'] = ['Creator identity missing']
        self.assertEqual(compose(data)['status'], 'probable_original')

    def test_author_topic_date_match_without_body_stays_lead(self):
        # Synthetic counterpart of an unreadable landing page with a strong author lead.
        data = original_case()
        data['video']['content_reviewed'] = False
        data['evidence'] = data['evidence'][1:]
        data['evidence'][1]['excerpt'] = 'Synthetic author repository, topic and publication date agree'
        data['candidates'][0]['identity_evidence'] = ['u1', 'a1']
        data['candidates'][0]['gaps'] = ['Original video body anchor missing']
        for classification in ('probable_original', 'confirmed_original'):
            with self.subTest(classification=classification):
                data['candidates'][0]['classification'] = classification
                result = compose(data)
                self.assertEqual(result['status'], 'needs_more_evidence')
                self.assertEqual(result['original'], [])
                self.assertEqual(result['leads'][0]['classification'], 'unverified_lead')
                self.assertEqual(result['alternatives'], [])
                self.assertFalse(result['alternative_search_authorized'])

    def test_alternative_and_reference(self):
        data = original_case()
        data['alternative_search_authorized'] = True
        c = data['candidates'][0]
        c.update(classification='same_capability', identity_score=0, identity_evidence=[], capability_verified=True)
        result = compose(data)
        self.assertEqual(result['status'], 'alternative_only')
        self.assertEqual(result['original'], [])
        self.assertEqual(result['alternatives'][0]['label'], '替代')
        c['classification'] = 'reference_only'
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')

    def test_no_alternatives_without_user_consent(self):
        data = original_case()
        data['candidates'][0].update(classification='same_capability', capability_verified=True)
        for consent in (None, False, 'true'):
            data['alternative_search_authorized'] = consent
            result = compose(data)
            self.assertEqual(result['alternatives'], [])
            self.assertIn('要不要', result['next_action'])
            self.assertIn('1–3', result['next_action'])

    def test_alternative_from_supplied_description_not_video_identity(self):
        data = original_case()
        data['video']['content_reviewed'] = False
        data['alternative_search_authorized'] = True
        data['target_requirement'] = {'source': 'share_text', 'description': '照片转旅行视频'}
        data['candidates'][0].update(classification='partial_substitute', capability_verified=True)
        result = compose(data)
        self.assertEqual(result['status'], 'alternative_only')
        self.assertFalse(result['video']['content_reviewed'])
        data['candidates'][0]['classification'] = 'confirmed_original'
        self.assertEqual(compose(data)['original'], [])

    def test_consent_does_not_replace_target_or_upstream(self):
        data = original_case()
        data['alternative_search_authorized'] = True
        data['video']['content_reviewed'] = False
        data['candidates'][0].update(classification='same_capability', capability_verified=True)
        for requirement in ({}, {'source': 'model_guess', 'description': 'Make video'},
                            {'source': 'user_request', 'description': ' '}):
            data['target_requirement'] = requirement
            self.assertEqual(compose(data)['alternatives'], [])
        data['target_requirement'] = {'source': 'user_request', 'description': '照片转旅行视频'}
        data['evidence'][1]['verified'] = False
        self.assertEqual(compose(data)['alternatives'], [])

    def test_limited_scope_not_found_and_gates(self):
        data = {'video': {'content_reviewed': True}, 'search_complete': True, 'sources_checked': ['github']}
        result = compose(data)
        self.assertEqual(result['status'], 'not_found')
        self.assertEqual(result['search_scope'], {'sources_checked': ['github'], 'search_complete': True})
        self.assertTrue(any('本次实际检索范围' in limitation for limitation in result['limitations']))
        # Only title / no video evidence can never be not_found.
        data['video'] = {'content_reviewed': False}
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')
        data['video'] = {'content_reviewed': True}
        # Search incomplete -> needs_more_evidence.
        data['search_complete'] = False
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')
        data['search_complete'] = True
        # SkillHub alone is not a main path; no successful main path -> needs_more_evidence.
        data['sources_checked'] = ['skillhub']
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')
        data['sources_checked'] = ['github']
        # Unresolved conflict blocks not_found.
        data['unresolved_conflict'] = True
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')
        data['unresolved_conflict'] = False
        # Empty successful scope -> needs_more_evidence.
        data['sources_checked'] = []
        self.assertEqual(compose(data)['status'], 'needs_more_evidence')

    def test_original_without_skillhub(self):
        data = original_case()
        data['sources_checked'] = ['github']
        data['search_complete'] = True
        # confirmed_original never requires SkillHub.
        self.assertEqual(compose(data)['status'], 'original_found')

    def test_search_cli(self):
        env = no_token_env()
        base = [sys.executable, str(ROOT/'scripts/search_skills.py')]
        fixture = str(ROOT/'tests/fixtures/search_results.json')
        r = subprocess.run(base + ['demo skill', '--fixture', fixture], capture_output=True, text=True, check=True, env=env)
        data = json.loads(r.stdout)
        self.assertTrue(data['fixture'])
        # Default is GitHub only; SkillHub gets an explicit skipped record, never a query.
        self.assertEqual({c['source'] for c in data['candidates']}, {'github'})
        self.assertTrue(any(x['source'] == 'github_code' and x['status'] == 'skipped' and 'GITHUB_TOKEN' in x['reason']
                            for x in data['requests']))
        self.assertTrue(any(x['source'] == 'skillhub' and x['status'] == 'skipped' and 'not selected' in x['reason']
                            for x in data['requests']))
        self.assertTrue(all(c['identity_score'] == 0 for c in data['candidates']))
        self.assertTrue(all('capability_similarity' in c for c in data['candidates']))
        # Explicit dual-source selection queries SkillHub with only the keyword param.
        r2 = subprocess.run(base + ['demo skill', '--fixture', fixture, '--sources', 'github,skillhub'],
                            capture_output=True, text=True, check=True, env=env)
        data2 = json.loads(r2.stdout)
        self.assertEqual({c['source'] for c in data2['candidates']}, {'github', 'skillhub'})
        skillhub = [x for x in data2['requests'] if x['source'] == 'skillhub'][0]
        self.assertEqual(skillhub['url'], 'https://api.skillhub.cn/api/skills?keyword=demo+skill')
        search = load_script('search_skills')
        malformed = search.search('demo', {'github': {}, 'skillhub': {'data': {'skills': []}}}, sources=['github', 'skillhub'])
        self.assertEqual(len(malformed['failures']), 1)

    def test_default_never_queries_skillhub(self):
        search = load_script('search_skills')
        fetched = []

        def fake_fetch(url, headers=None, timeout=None):
            fetched.append(url)
            return {'items': []}

        with mock.patch.object(search, 'fetch', side_effect=fake_fetch), \
                mock.patch.dict(os.environ, {'GITHUB_TOKEN': '', 'GH_TOKEN': ''}):
            result = search.search('demo skill')
        self.assertEqual(fetched, ['https://api.github.com/search/repositories?q=demo+skill&per_page=10'])
        self.assertTrue(any(x['source'] == 'skillhub' and x['status'] == 'skipped' and 'not selected' in x['reason']
                            for x in result['requests']))
        self.assertTrue(any('SkillHub was not queried' in limitation for limitation in result['limitations']))
        self.assertTrue(result['elapsed_seconds'] is not None)

    def test_explicit_skillhub_only_keyword_param(self):
        search = load_script('search_skills')
        calls = []

        def fake_fetch(url, headers=None, timeout=None):
            calls.append((url, timeout))
            if 'api.github.com' in url:
                return {'items': []}
            return {'data': {'skills': []}}

        with mock.patch.object(search, 'fetch', side_effect=fake_fetch), \
                mock.patch.dict(os.environ, {'GITHUB_TOKEN': '', 'GH_TOKEN': ''}):
            result = search.search('demo', sources=['github', 'skillhub'], request_timeout=7, total_budget=60)
        skillhub_calls = [(url, t) for url, t in calls if 'skillhub' in url]
        self.assertEqual(len(skillhub_calls), 1)
        url, timeout = skillhub_calls[0]
        self.assertEqual(url, 'https://api.skillhub.cn/api/skills?keyword=demo')
        for param in ('page', 'pageSize', 'sortBy'):
            self.assertNotIn(param, url)
        self.assertTrue(all(t == 7 for _, t in calls))
        self.assertEqual(result['elapsed_seconds'] is not None, True)

    def test_budget_exhausted_skips_remaining_requests(self):
        search = load_script('search_skills')
        fetched = []

        def fake_fetch(url, headers=None, timeout=None):
            fetched.append(url)
            time.sleep(0.25)
            return {'items': []} if 'api.github.com' in url else {'data': {'skills': []}}

        with mock.patch.object(search, 'fetch', side_effect=fake_fetch), \
                mock.patch.dict(os.environ, {'GITHUB_TOKEN': 't', 'GH_TOKEN': 't'}):
            # github + github_code run within the budget; skillhub is skipped.
            result = search.search('demo', sources=['github', 'skillhub'], request_timeout=0.1, total_budget=0.4)
        self.assertEqual(len(fetched), 2)
        skillhub = [x for x in result['requests'] if x['source'] == 'skillhub'][0]
        self.assertEqual(skillhub['status'], 'skipped')
        self.assertIn('budget', skillhub['reason'])
        self.assertTrue(result['budget_exhausted'])

    def test_fetch_timeout_capped_by_remaining_budget(self):
        search = load_script('search_skills')
        observed = []

        def fake_fetch(url, headers=None, timeout=None):
            observed.append(timeout)
            time.sleep(0.4)
            return {'items': []} if 'api.github.com' in url else {'data': {'skills': []}}

        with mock.patch.object(search, 'fetch', side_effect=fake_fetch), \
                mock.patch.dict(os.environ, {'GITHUB_TOKEN': 't', 'GH_TOKEN': 't'}):
            # request_timeout=10 but total_budget=0.5: every fetch must be capped by
            # min(request_timeout, remaining_budget), not wait the full 10s.
            result = search.search('demo', sources=['github', 'skillhub'], request_timeout=10, total_budget=0.5)
        self.assertEqual(len(observed), 2)  # github + github_code; skillhub skipped by budget
        self.assertLessEqual(observed[0], 0.5)
        self.assertLess(observed[1], observed[0])  # remaining budget shrinks the timeout
        self.assertTrue(result['budget_exhausted'])

    def test_limitations_reflect_actual_code_search_outcome(self):
        search = load_script('search_skills')

        def fail_code(url, headers=None, timeout=None):
            if '/search/code' in url:
                raise RuntimeError('simulated code search failure')
            return {'items': []} if '/search/repositories' in url else {'data': {'skills': []}}

        with mock.patch.object(search, 'fetch', side_effect=fail_code), \
                mock.patch.dict(os.environ, {'GITHUB_TOKEN': 't', 'GH_TOKEN': 't'}):
            result = search.search('demo', sources=['github', 'skillhub'])
        code = [r for r in result['requests'] if r['source'] == 'github_code'][0]
        self.assertEqual(code['status'], 'failed')
        self.assertTrue(any('failed' in limitation and 'github_code' in limitation for limitation in result['limitations']))
        self.assertFalse(any('succeeded' in limitation for limitation in result['limitations']))

        def ok_fetch(url, headers=None, timeout=None):
            return {'items': []} if 'api.github.com' in url else {'data': {'skills': []}}

        with mock.patch.object(search, 'fetch', side_effect=ok_fetch), \
                mock.patch.dict(os.environ, {'GITHUB_TOKEN': 't', 'GH_TOKEN': 't'}):
            result2 = search.search('demo', sources=['github', 'skillhub'])
        code2 = [r for r in result2['requests'] if r['source'] == 'github_code'][0]
        self.assertEqual(code2['status'], 'success')
        self.assertTrue(any('succeeded' in limitation for limitation in result2['limitations']))

    def test_metadata_partial_output_retained_on_command_failure(self):
        video = load_script('video_evidence')

        def fake_run(command, timeout=None):
            out_tpl = command[command.index('-o') + 1]
            out_dir = Path(out_tpl).parent
            (out_dir / 'video.info.json').write_text(json.dumps(
                {'id': 'x', 'title': 'Synthetic', 'uploader': 'example', 'duration': 180, 'is_live': False}))
            (out_dir / 'video.zh-Hans.json3').write_text(json.dumps(
                {'events': [{'tStartMs': 42000, 'segs': [{'utf8': 'Synthetic demo-skill line'}]}]}))
            raise RuntimeError('simulated subtitle failure after info write')

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'ev'
            with mock.patch.object(video, 'run', side_effect=fake_run):
                result = video.collect('https://example.invalid/video', out, frames=0)
            transcript_text = (out/'transcript.txt').read_text()
        self.assertEqual(result['metadata'].get('title'), 'Synthetic')
        self.assertEqual(result['transcript_status'], 'available')
        self.assertIn('[42.000]', transcript_text)
        self.assertTrue(any(f['stage'] == 'metadata' for f in result['failures']))

    def test_search_scope_passes_through_input_query_scope(self):
        data = {'video': {'content_reviewed': True}, 'search_complete': True, 'sources_checked': ['github'],
                'query': 'resume-tailor-skill', 'search_query': 'filename:SKILL.md "resume-tailor-skill"'}
        result = compose(data)
        self.assertEqual(result['status'], 'not_found')
        scope = result['search_scope']
        self.assertEqual(scope['query'], 'resume-tailor-skill')
        self.assertEqual(scope['search_query'], 'filename:SKILL.md "resume-tailor-skill"')
        self.assertEqual(scope['sources_checked'], ['github'])
        self.assertIs(scope['search_complete'], True)
        # A caller-supplied search_scope dict supplements without overriding.
        data['search_scope'] = {'platform': 'douyin'}
        scope2 = compose(data)['search_scope']
        self.assertEqual(scope2['platform'], 'douyin')
        self.assertEqual(scope2['sources_checked'], ['github'])

    def test_invalid_timeout_and_budget_rejected(self):
        search = load_script('search_skills')
        with self.assertRaises(ValueError):
            search.search('demo', request_timeout=0)
        with self.assertRaises(ValueError):
            search.search('demo', total_budget=0)
        with self.assertRaises(ValueError):
            search.search('demo', sources=['unknown'])
        # request_timeout > total_budget is allowed: min(timeout, remaining) caps it.

    def test_video_missing_and_available_transcript_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture_path = ROOT/'tests/fixtures/video_evidence.json'
            command = [sys.executable, str(ROOT/'scripts/video_evidence.py'), 'https://example.invalid/video',
                       '--output-dir', str(Path(tmp)/'missing'), '--fixture', str(fixture_path)]
            r = subprocess.run(command, capture_output=True, text=True, check=True)
            data = json.loads(r.stdout)
            self.assertEqual(data['transcript_status'], 'missing')
            self.assertEqual(data['transcript'], [])
            self.assertFalse((Path(tmp)/'missing/transcript.txt').exists())
            fixture = json.loads(fixture_path.read_text())
            fixture['transcript'] = [{'start_seconds': 42, 'text': 'Synthetic demo-skill line', 'source': 'fixture'}]
            path = Path(tmp)/'captions.json'
            path.write_text(json.dumps(fixture))
            command[-1] = str(path)
            command[command.index('--output-dir')+1] = str(Path(tmp)/'available')
            data = json.loads(subprocess.run(command, capture_output=True, text=True, check=True).stdout)
            self.assertEqual(data['transcript_status'], 'available')
            self.assertIn('[42.000]', (Path(tmp)/'available/transcript.txt').read_text())

    def test_frames_zero_never_downloads_or_runs_ffmpeg(self):
        video = load_script('video_evidence')
        commands = []

        def fake_run(command, timeout=None):
            commands.append(command)
            if '--write-info-json' in command:
                out_tpl = command[command.index('-o') + 1]
                out_dir = Path(out_tpl).parent
                (out_dir / 'video.info.json').write_text(json.dumps(
                    {'id': 'x', 'title': 'Synthetic', 'uploader': 'example', 'duration': 180, 'is_live': False}))
            return ''

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(video, 'run', side_effect=fake_run):
                result = video.collect('https://example.invalid/video', Path(tmp)/'ev', frames=0)
        self.assertEqual(result['frames'], [])
        self.assertEqual(result['metadata'].get('title'), 'Synthetic')
        for cmd in commands:
            flat = ' '.join(cmd)
            self.assertNotIn('worst', flat)
            self.assertNotIn('ffmpeg', flat)
            self.assertNotIn('ffprobe', flat)

    def test_subprocess_bounded_by_remaining_budget(self):
        video = load_script('video_evidence')
        timeouts = []

        def fake_run(command, timeout=None):
            timeouts.append(timeout)
            if '--write-info-json' in command:
                out_tpl = command[command.index('-o') + 1]
                out_dir = Path(out_tpl).parent
                (out_dir / 'video.info.json').write_text(json.dumps(
                    {'id': 'x', 'title': 'Synthetic', 'uploader': 'example', 'duration': 180, 'is_live': False}))
            return ''

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(video, 'run', side_effect=fake_run):
                video.collect('https://example.invalid/video', Path(tmp)/'ev', frames=0, timeout=30, total_budget=5)
        self.assertEqual(len(timeouts), 1)
        self.assertLessEqual(timeouts[0], 5)

    def test_frames_stage_failure_keeps_partial_evidence(self):
        video = load_script('video_evidence')

        def fake_run(command, timeout=None):
            if '--write-info-json' in command:
                out_tpl = command[command.index('-o') + 1]
                out_dir = Path(out_tpl).parent
                (out_dir / 'video.info.json').write_text(json.dumps(
                    {'id': 'x', 'title': 'Synthetic', 'uploader': 'example', 'duration': 180, 'is_live': False}))
                return ''
            raise RuntimeError('simulated frames stage failure')

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(video, 'run', side_effect=fake_run):
                result = video.collect('https://example.invalid/video', Path(tmp)/'ev', frames=2, timeout=10, total_budget=60)
        self.assertTrue(result['metadata'])
        self.assertEqual(result['frames'], [])
        frames_fail = [f for f in result['failures'] if f['stage'] == 'frames']
        self.assertEqual(len(frames_fail), 1)
        self.assertIn('elapsed_seconds', frames_fail[0])
        self.assertIn('resume', frames_fail[0])

    def test_live_stream_never_downloads_video(self):
        video = load_script('video_evidence')
        commands = []

        def fake_run(command, timeout=None):
            commands.append(command)
            if '--write-info-json' in command:
                out_tpl = command[command.index('-o') + 1]
                out_dir = Path(out_tpl).parent
                (out_dir / 'video.info.json').write_text(json.dumps(
                    {'id': 'x', 'title': 'Live', 'uploader': 'example', 'duration': None, 'is_live': True}))
            return ''

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(video, 'run', side_effect=fake_run):
                result = video.collect('https://example.invalid/video', Path(tmp)/'ev', frames=2)
        self.assertIs(result['metadata'].get('is_live'), True)
        self.assertEqual(result['frames'], [])
        self.assertTrue(any(f['stage'] == 'frames' and 'Live' in f['error'] for f in result['failures']))
        self.assertFalse(any('worst' in ' '.join(c) for c in commands))

    def test_compose_cli_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            for expected, data in [('original_found', original_case()), ('alternative_only', original_case())]:
                if expected == 'alternative_only':
                    data['alternative_search_authorized'] = True
                    data['candidates'][0].update(classification='partial_substitute', capability_verified=True)
                path = Path(tmp)/'input.json'
                path.write_text(json.dumps(data))
                r = subprocess.run([sys.executable, str(ROOT/'scripts/compose_result.py'), str(path)],
                                   capture_output=True, text=True, check=True)
                result = json.loads(r.stdout)
                self.assertEqual(result['status'], expected)
                self.assertTrue(result['fixture'])
                self.assertTrue({'status', 'video', 'original', 'alternatives', 'evidence', 'limitations', 'next_action'} <= result.keys())
                print(json.dumps({'fixture': True, 'status': result['status'], 'original_count': len(result['original']),
                                  'alternative_count': len(result['alternatives'])}))


    def test_missing_downloader_returns_structured_failure(self):
        video = load_script('video_evidence')
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
                video, 'ytdlp_command', side_effect=RuntimeError('yt-dlp unavailable')):
            result = video.collect('https://example.invalid/video', Path(tmp))
        self.assertEqual(result['metadata'], {})
        self.assertEqual(result['failures'][0]['stage'], 'dependency')

    def test_search_summary_preserves_complete_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'search.json'
            r = subprocess.run([
                sys.executable, str(ROOT/'scripts/search_skills.py'), 'demo',
                '--fixture', str(ROOT/'tests/fixtures/search_results.json'),
                '--summary', '--output', str(output),
            ], capture_output=True, text=True, check=True)
            summary, full = json.loads(r.stdout), json.loads(output.read_text())
        self.assertEqual(summary['full_output'], str(output))
        self.assertEqual(len(summary['candidates']), len(full['candidates']))
        self.assertNotIn('raw', summary['candidates'][0])
        self.assertIn('raw', full['candidates'][0])

    def test_video_summary_preserves_evidence_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([
                sys.executable, str(ROOT/'scripts/video_evidence.py'), 'https://example.invalid/video',
                '--output-dir', tmp, '--fixture', str(ROOT/'tests/fixtures/video_evidence.json'),
                '--summary',
            ], capture_output=True, text=True, check=True)
            summary = json.loads(r.stdout)
            full = json.loads(Path(summary['evidence_file']).read_text())
        self.assertNotIn('metadata', summary)
        self.assertIn('metadata', full)
        self.assertEqual(summary['frames'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
