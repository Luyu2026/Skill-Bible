#!/usr/bin/env python3
"""Public, unauthenticated discovery. Scores are lexical hints, never identity verdicts.

By default only GitHub is queried (repository search; code search additionally when
a token is configured). SkillHub is queried only when explicitly selected via
--sources or the `sources` argument. Each request has a finite per-request timeout,
and remaining budget caps each socket timeout. When the budget runs out, later
sources are skipped without retries. Socket timeouts are not a strict wall-clock
deadline for DNS or a response that keeps delivering bytes.
"""
import argparse
import datetime as dt
import json
import os
import time
import urllib.parse
import urllib.request

DEFAULT_SOURCES = ['github']
ALL_SOURCES = ('github', 'skillhub')
GITHUB_CODE_SOURCE = 'github_code'


def fetch(url, headers=None, timeout=20):
    request_headers = {'User-Agent': 'find-skill-from-video/1.0', 'Accept': 'application/json'}
    request_headers.update(headers or {})
    with urllib.request.urlopen(urllib.request.Request(url, headers=request_headers), timeout=timeout) as r:
        return json.load(r)


def rows(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ('skills', 'items', 'list', 'records', 'results', 'data'):
            if key in payload:
                found = rows(payload[key])
                if found is not None:
                    return found
    return None


def normalize(item, source, keyword):
    repo = item.get('repository') if isinstance(item.get('repository'), dict) else {}
    name = (item.get('full_name') or item.get('name') or item.get('title') or item.get('slug')
            or repo.get('full_name') or '')
    if source == 'github_code' and repo.get('full_name'):
        name = repo['full_name'] + ':' + (item.get('path') or '')
    owner = item.get('ownerName') or item.get('author') or item.get('owner') or repo.get('owner') or ''
    if isinstance(owner, dict):
        owner = owner.get('login') or owner.get('name') or ''
    namespace = item.get('namespace') if isinstance(item.get('namespace'), dict) else {}
    if not owner:
        owner = namespace.get('displayName') or namespace.get('handle') or ''
    license_hint = item.get('license') or item.get('license_name')
    if isinstance(license_hint, dict):
        license_hint = license_hint.get('spdx_id') or license_hint.get('name')
    url = (item.get('html_url') or item.get('url') or item.get('homepage')
           or item.get('github_url') or item.get('repository_url') or repo.get('html_url'))
    upstream = item.get('upstream_url') or item.get('github_url') or item.get('repository_url')
    description = item.get('description') or repo.get('description') or ''
    tokens = keyword.lower().split()
    similarity = round(100 * sum(t in (str(name)+' '+str(description)).lower() for t in tokens) / max(1, len(tokens)))
    raw = {k: item.get(k) for k in (
        'id', 'full_name', 'name', 'slug', 'path', 'html_url', 'homepage', 'url',
        'owner', 'ownerName', 'namespace', 'publisher', 'description',
        'license', 'topics', 'stargazers_count', 'downloads', 'stars', 'score',
        'source', 'upstream_url', 'verified', 'version', 'updated_at', 'repository',
    ) if item.get(k) is not None}
    return dict(name=name, source=source, url=url, author=owner, description=description,
                license_hint=license_hint, upstream_url=upstream, match_method='public_keyword_search',
                identity_score=0, capability_similarity=similarity,
                identity_evidence=[], verification='unverified', raw=raw)


def parse_sources(sources):
    """Normalize a source selection to a list of known source names.

    Accepts None (default: GitHub only), a single string, or an iterable of
    strings. Comma-separated values inside one string are supported, e.g.
    'github,skillhub'. Unknown names raise ValueError.
    """
    if sources is None:
        return list(DEFAULT_SOURCES)
    if isinstance(sources, str):
        sources = [sources]
    normalized = []
    for item in sources:
        for part in str(item).split(','):
            part = part.strip().lower()
            if part not in ALL_SOURCES:
                raise ValueError("unknown source %r; choose from %s" % (part, ', '.join(ALL_SOURCES)))
            if part not in normalized:
                normalized.append(part)
    if not normalized:
        raise ValueError('no sources selected')
    return normalized


def search(keyword, fixture=None, sources=None, request_timeout=20, total_budget=60):
    request_timeout = float(request_timeout)
    total_budget = float(total_budget)
    if request_timeout <= 0:
        raise ValueError('request_timeout must be > 0')
    if total_budget <= 0:
        raise ValueError('total_budget must be > 0')
    # request_timeout may exceed total_budget on purpose: each real request is
    # capped by min(request_timeout, remaining_budget), so the budget always wins.
    sources = parse_sources(sources)
    result = {'keyword': keyword, 'fixture': bool(fixture), 'candidates': [], 'requests': [], 'failures': [],
              'scoring': 'identity_score=0 until independent verification; capability_similarity is lexical overlap, not functional validation',
              'sources_selected': sources, 'elapsed_seconds': None, 'budget_exhausted': False}
    github_token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    planned = []
    if 'github' in sources:
        planned.append(('github', 'https://api.github.com/search/repositories?' + urllib.parse.urlencode({'q': keyword, 'per_page': 10})))
        if github_token:
            planned.append((GITHUB_CODE_SOURCE, 'https://api.github.com/search/code?' + urllib.parse.urlencode({'q': keyword + ' filename:SKILL.md', 'per_page': 10})))
    if 'skillhub' in sources:
        # Only the verified `keyword` parameter is sent; no guessed filters.
        planned.append(('skillhub', 'https://api.skillhub.cn/api/skills?' + urllib.parse.urlencode({'keyword': keyword})))
    # Keep explicit source=skipped records for un-executed sources: a source that
    # was never queried must never be presented as "no results from that source".
    for source in ALL_SOURCES:
        if source not in sources:
            result['requests'].append({'source': source, 'status': 'skipped',
                                       'reason': 'source not selected; use --sources to include it',
                                       'retrieved_at': dt.datetime.now(dt.timezone.utc).isoformat()})
    started = time.monotonic()
    for source, url in planned:
        record = dict(source=source, url=url, retrieved_at=dt.datetime.now(dt.timezone.utc).isoformat())
        remaining = total_budget - (time.monotonic() - started)
        if remaining <= 0:
            record.update(status='skipped', reason='total budget exhausted; remaining requests skipped')
            result['requests'].append(record)
            result['budget_exhausted'] = True
            continue
        req_started = time.monotonic()
        try:
            if fixture is not None:
                if source not in fixture:
                    record.update(status='skipped', reason='source absent from fixture')
                    result['requests'].append(record)
                    continue
                payload = fixture[source]
                headers = None
            else:
                headers = {'Authorization': 'Bearer ' + github_token} if source.startswith('github') and github_token else None
                # Bound each real request by the remaining budget as well as the
                # configured timeout, so a slow response cannot overrun the deadline.
                payload = fetch(url, headers, min(request_timeout, remaining))
            items = rows(payload)
            if items is None:
                raise ValueError('Unrecognized response schema; no candidates inferred')
            result['candidates'].extend(normalize(i, source, keyword) for i in items if isinstance(i, dict))
            record.update(status='fixture' if fixture is not None else 'success', count=len(items))
        except Exception as exc:
            record.update(status='failed', error=str(exc))
            result['failures'].append(record.copy())
        record['elapsed_seconds'] = round(time.monotonic() - req_started, 3)
        result['requests'].append(record)
    if 'github' in sources and not github_token:
        result['requests'].append({'source': GITHUB_CODE_SOURCE, 'status': 'skipped',
                                   'reason': 'GITHUB_TOKEN/GH_TOKEN not set; GitHub code search requires authentication',
                                   'retrieved_at': dt.datetime.now(dt.timezone.utc).isoformat()})
    def _request_status(source_name):
        for r in result['requests']:
            if r['source'] == source_name:
                return r.get('status'), r.get('reason')
        return None, None

    limitations = []
    if 'github' in sources:
        code_status, code_reason = _request_status(GITHUB_CODE_SOURCE)
        if code_status == 'success':
            limitations.append('GitHub code search succeeded with the configured token; code results are lexical hints and require upstream verification.')
        elif code_status == 'fixture':
            limitations.append('GitHub code search exercised via fixture only (not a live request); code results are lexical hints and require upstream verification.')
        elif code_status == 'failed':
            limitations.append('GitHub code search failed in this run (see github_code request record); code-level discovery is incomplete, not confirmed as having no results.')
        elif code_status == 'skipped':
            if github_token:
                limitations.append('GitHub code search was skipped in this run (reason: %s); code-level discovery is incomplete.' % (code_reason or 'not executed'))
            else:
                limitations.append('GitHub code search requires authentication; code search was skipped (not performed) because GITHUB_TOKEN/GH_TOKEN is not set. Repository search only.')
        else:
            limitations.append('GitHub code search outcome not recorded; code-level discovery not confirmed in this run.')
    else:
        limitations.append('GitHub was not selected in this run; no GitHub repository/code search was attempted.')
    if 'skillhub' in sources:
        limitations.append('SkillHub entries require upstream verification against the real repository; hit counts never establish original authorship.')
    else:
        limitations.append('SkillHub was not queried in this run (selected sources: %s); this run makes no claim about SkillHub-covered entries.' % ', '.join(sources))
    if result['budget_exhausted']:
        limitations.append('Total budget of %ss was exhausted; remaining requests were skipped, not retried.' % total_budget)
    limitations.append('Discovery does not verify SKILL.md, license, video identity or compatibility. Scores are lexical hints; no candidate is identified as the original by hit count.')
    result['limitations'] = limitations
    result['elapsed_seconds'] = round(time.monotonic() - started, 3)
    return result


def _cli_sources(value):
    try:
        return parse_sources(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('keyword')
    p.add_argument('--fixture', type=argparse.FileType('r'))
    p.add_argument('--output')
    p.add_argument('--summary', action='store_true', help='print compact discovery summary; --output still saves complete evidence')
    p.add_argument('--sources', action='append', type=_cli_sources, default=None,
                   help='sources to query: github and/or skillhub, comma-separated (default: github only; SkillHub is never queried unless selected)')
    p.add_argument('--timeout', type=float, default=20.0, help='per-request timeout in seconds (default 20)')
    p.add_argument('--total-budget', type=float, default=60.0, help='total wall-clock budget in seconds (default 60)')
    args = p.parse_args()
    if args.timeout <= 0 or args.total_budget <= 0:
        p.error('--timeout and --total-budget must be > 0')
    sources = [s for group in (args.sources or []) for s in group] or None
    result = search(args.keyword, json.load(args.fixture) if args.fixture else None,
                    sources=sources, request_timeout=args.timeout, total_budget=args.total_budget)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(text + '\n')
    if args.summary:
        print(json.dumps({
            'fixture': result['fixture'], 'elapsed_seconds': result['elapsed_seconds'],
            'budget_exhausted': result['budget_exhausted'],
            'requests': result['requests'],
            'candidates': [{k: c.get(k) for k in ('name', 'url', 'source', 'upstream_url', 'verification')}
                           for c in result['candidates']],
            'limitations': result['limitations'], 'full_output': args.output,
        }, ensure_ascii=False, indent=2))
    else:
        print(text)
    success = any(r.get('status') in ('success', 'fixture') for r in result['requests'])
    return 0 if success else 2


if __name__ == '__main__':
    raise SystemExit(main())
