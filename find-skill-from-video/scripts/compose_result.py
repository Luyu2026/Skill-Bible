#!/usr/bin/env python3
"""Package manually verified findings; this gate does not perform verification.

not_found uses limited-scope semantics: content reviewed, search complete, and at
least one actually-successful main path (GitHub / GitHub code / public web / direct
upstream) present in sources_checked, with no unresolved conflict. It means "not
found within this run's actual search scope", never "absent from the whole
internet". SkillHub is not a hard gate for not_found, and confirmed_original never
requires SkillHub. search_scope (sources_checked, search_complete plus the input
query scope, e.g. the keywords actually searched) is passed through so callers can
see exactly what was covered.
"""
import argparse
import json

# Only actually-successful main discovery paths can support a limited not_found.
# Failed sources and un-searched sources must never be listed here.
MAIN_SOURCES = {'github', 'github_code', 'public_web', 'direct_upstream'}

# Query-scope fields carried on the input that describe what was actually searched.
QUERY_SCOPE_KEYS = ('search_query', 'queries', 'query', 'keywords', 'search_terms')


def _main_path_success(sources_checked):
    return any(s in MAIN_SOURCES for s in (sources_checked or []))


def compose(data):
    evidence = data.get('evidence', [])
    ids = {e['id']: e for e in evidence}
    originals, alternatives = [], []
    limitations = list(data.get('limitations', []))
    video = data.get('video', {})
    search_complete = data.get('search_complete') is True
    sources_checked = list(data.get('sources_checked', []))
    for candidate in data.get('candidates', []):
        c = candidate.copy()
        classification = c.get('classification')
        refs = [ids[i] for i in c.get('identity_evidence', []) if i in ids]
        timed_anchor = any(e.get('kind') in ('video_frame', 'video_subtitle') and
                           isinstance(e.get('timestamp_seconds'), (int, float)) and e.get('source') and
                           e.get('excerpt') for e in refs)
        extracted_body = any(e.get('kind') == 'video_extract' and e.get('source') == video.get('url')
                             and e.get('excerpt') and e.get('method') and e.get('verified') is True
                             and e.get('content_level') == 'body' for e in refs)
        video_anchor = timed_anchor or extracted_body
        upstream = any(e.get('kind') == 'upstream_skill' and e.get('source') == c.get('skill_file_url')
                       and e.get('excerpt') and e.get('verified') is True for e in refs)
        independent = any(e.get('kind') == 'identity_corroboration' and e.get('verified') is True
                          and e.get('source') and e.get('excerpt') for e in refs)
        if classification == 'confirmed_original':
            if video.get('content_reviewed') and video_anchor and upstream and independent and not c.get('conflicts'):
                originals.append(c)
            else:
                limitations.append(f"{c.get('name')}: confirmed_original rejected; missing identity evidence or unresolved conflict")
        elif classification == 'probable_original':
            if video.get('content_reviewed') and video_anchor and upstream and c.get('gaps') and not c.get('conflicts'):
                originals.append(c)
            else:
                limitations.append(f"{c.get('name')}: probable_original lacks review, upstream, or explicit gaps")
        elif classification in ('same_capability', 'partial_substitute'):
            cap_refs = [ids[i] for i in c.get('capability_evidence', []) if i in ids]
            usable_file = any(e.get('kind') == 'upstream_skill' and e.get('verified') is True
                              and e.get('source') == c.get('skill_file_url') and e.get('excerpt') for e in cap_refs)
            if video.get('content_reviewed') and c.get('availability') == 'available' and usable_file and c.get('capability_verified') is True:
                c['label'] = '替代'
                alternatives.append(c)
            else:
                limitations.append(f"{c.get('name')}: substitute not verified usable")
    if any(c['classification'] == 'confirmed_original' for c in originals):
        status = 'original_found'
    elif originals:
        status = 'probable_original'
    elif alternatives:
        status = 'alternative_only'
    elif video.get('content_reviewed') and search_complete and _main_path_success(sources_checked) and not data.get('unresolved_conflict'):
        status = 'not_found'
        limitations.append('not_found 仅表示本次实际检索范围（sources_checked: %s；search_complete: true）内未找到，不代表全网或未覆盖来源不存在。'
                           % ','.join(sources_checked))
    else:
        status = 'needs_more_evidence'
    search_scope = {'sources_checked': sources_checked, 'search_complete': search_complete}
    # Pass through the input query scope: the keywords / queries actually searched,
    # not just the source names. A caller-supplied search_scope dict supplements
    # (never overrides) the normalized fields above.
    for key in QUERY_SCOPE_KEYS:
        value = data.get(key)
        if value is not None:
            search_scope[key] = value
    supplied_scope = data.get('search_scope')
    if isinstance(supplied_scope, dict):
        for key, value in supplied_scope.items():
            if key not in search_scope:
                search_scope[key] = value
    return dict(status=status, fixture=bool(data.get('fixture')), video=video, original=originals,
                alternatives=alternatives, evidence=evidence, limitations=limitations,
                search_scope=search_scope,
                next_action=data.get('next_action') or '补充带时间点的视频内容、身份锚点或未覆盖来源，然后重新核验。')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=argparse.FileType('r'))
    a = p.parse_args()
    print(json.dumps(compose(json.load(a.input)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
