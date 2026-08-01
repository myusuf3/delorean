# Tasks

Working notes on outstanding work, written 2026-08-01. Grouped by what kind of
decision each item needs rather than by priority.

## In flight

### PR #139 — land the stranded boundary work

Two commits were pushed to `add-timestamp-naming` after PR #137 had already been
merged, so they never reached master. #139 carries them:

- `midnight`, `start_of_day` and `end_of_day` now return `Delorean` instead of a
  bare `datetime`. They previously did `return self._dt.replace(...)` without
  re-wrapping, unlike `replace()` and `shift()` a few lines away. **Breaking**
  for callers doing `d.midnight.strftime(...)`.
- `start_of_month`, `end_of_month`, `start_of_year`, `end_of_year` (closes #85).

Master is currently half-applied: `d.timestamp` exists but `d.midnight` still
returns a `datetime`. 112 tests on the branch versus 102 on master.

### PR #138 — recommend closing

An autonomous AI bot PR against issue #79. The whole diff is `import pytz` added
to `delorean/__init__.py`, with no tests or docs. It does not fix the issue: the
reporter asked for `from delorean import utc` or a `timezone` helper so callers
never touch pytz, and this instead makes pytz a formal part of delorean's public
namespace, which is the opposite of the complaint.

Note our ruff `per-file-ignores` for `F401` on `__init__.py` means that unused
import would not be flagged.

A real fix for #79 is small and worth doing: export a `utc` constant and/or a
`timezone` helper, which also moves toward the pytz abstraction below.

## Bugs

### Fractional-second truncation (issue #75)

The only confirmed live bug in the tracker. `Delorean._shift_date` does
`num_shifts = int(args[0])`, so fractional shifts are silently truncated:

    next_second(0.5) -> no movement at all (int(0.5) == 0)
    next_second(1.5) -> moves 1 second

Silently doing nothing is the harmful part. Either support fractions for the
time-based units, or reject non-integers with a clear `TypeError`. Weekday and
calendar units cannot take fractions either way, so they need handling
separately. Needs a test covering both the fractional case and the integer path
it must not regress.

## Release

### Cut a release

Everything from this session is unreleased, and `CHANGES.rst` has no entry for
any of it. Issue #104 is someone explicitly asking for a release, open since
2019.

Needs a changelog line, most significant first:

- Dropped Python 3.9; `requires-python` is now `>=3.10`. The only change that
  narrows what users can do, so it drives the version number (convention would
  be 1.1.0).
- Boundary properties now return `Delorean` (breaking, see #139).
- Build moved from `setup.py` to `pyproject.toml`/hatchling; version is
  single-sourced in `pyproject.toml`.
- `Delorean.__getattr__` returned the `AttributeError` class instead of raising
  it, so `hasattr()` wrongly reported `True` for invalid shift names.
- Added `timestamp`/`from_timestamp`; `epoch` retained as an alias (#86).
- Added month and year boundary properties (#85).
- Dropped the `mock` dev dependency for `unittest.mock` (#113).
- Trove classifiers restored; license switched to PEP 639 format.
- Documentation corrections: quickstart wrongly claimed `parse()` converts
  offsets to UTC (it stores a `pytz.FixedOffset`) and wrongly documented
  `.naive`. Documented how DST gaps and ambiguous times resolve.
- Note for #95: `delorean.dates.UTC` (the constant `UTC = "UTC"`) was removed in
  commit `afac86a`, first shipped in 0.6.0, and never documented. Mention it
  here as previously undocumented rather than inventing a retroactive 0.6.0
  section, and point users at `"UTC"` or `pytz.utc`.

Not a behaviour change: the `datetime.utcnow()`/`utcfromtimestamp()`
replacements are exactly equivalent to what they replaced.

Context: `CHANGES.rst` documents **only** 1.0.0. Nine of the ten released tags
(`v0.3` through `0.6.0`) have no entry at all, so "Release History" is currently
a single-release file. A full backfill from git tags is a separate, larger job.

### Adopt a changelog tool

`CHANGES.rst` is hand-written, which conflicts with the rule never to hand-edit
changelogs. towncrier and scriv are the usual choices, generating entries from
per-change fragment files. Worth doing before the next release so the entries
above can be generated rather than typed.

`docs/changelog.rst` just includes `../CHANGES.rst`, so whatever the tool
renders flows into the docs automatically. The deleted `releases_issue_uri` /
`releases_release_uri` settings in `docs/conf.py` were for the `releases` Sphinx
extension, which renders a changelog with linked issues — worth reconsidering
alongside the tool choice.

## Infrastructure

### Dependency vulnerability scanning

We have none. The old `test_lint_python.yml` ran `safety check` but with
`|| true`, so it never gated anything, and that workflow was deleted. Community
PR #124 had added a `safety_scan.yml`, which was the only real gate in the repo.

Options, cheapest first:

- GitHub Dependabot alerts: free, no workflow or secret, enabled in repo
  settings.
- `pip-audit`: free, no API key, maintained by PyPA. Runs as a normal CI step.
- Safety CLI (what #124 used): now requires a `SAFETY_API_KEY` secret.

Recommend Dependabot plus a `pip-audit` step, avoiding the API-key dependency.

### Pre-commit hooks

No `.pre-commit-config.yaml` exists. black and ruff are configured and
CI-enforced, so hooks would catch formatting locally instead of via red CI, the
main source of avoidable failures. Keep hook versions in step with the dev
dependency group so local and CI results agree.

### Stricter ruff rules

Currently `select = ["E4", "E7", "E9", "F", "I"]` — ruff's documented default
plus import sorting, pinned explicitly because the implicit default set changes
between releases. Broader families were left off because they demand library
changes that did not belong in a lint-setup PR:

- `DTZ` (48 findings) wants `tzinfo` on every `datetime()` call. Mostly wrong for
  this project, since handling naive datetimes is the library's domain.
  Recommend leaving off.
- `TRY004` (`dates.py:43`): `is_datetime_instance` raises `ValueError` for a type
  error; convention says `TypeError`. Changing it is **breaking** for anyone
  catching `ValueError`, so it belongs in a 2.0 discussion.
- `S110` + `BLE001` (`interface.py:75`): `except Exception: pass` in `parse()`'s
  ISO-first fallback. Intentional, but broad enough to swallow real bugs; a
  narrower `except ValueError` would be better.
- `SIM103` (`dates.py:33`): `is_datetime_naive` could `return dt.tzinfo is None`
  directly.
- `PIE790`: unnecessary `pass` in the exception classes.
- `UP031`/`UP004`/`UP009`: printf-style formatting, useless `object` inheritance,
  obsolete utf-8 coding declarations.

Also consider replacing the `F401` per-file-ignore on `delorean/__init__.py`
with an explicit `__all__`, which documents the public API instead of
suppressing the warning — and would stop hiding genuinely unused imports like
the one in PR #138.

## Documentation

### Document the dynamically-generated weekday methods

`next_tuesday`, `last_tuesday`, `next_monday` and the rest are absent from the
generated API reference. They are synthesized at runtime by
`Delorean.__getattr__` via `functools.partial` (`delorean/dates.py:~288`), so
autodoc has nothing to introspect. Confirmed pre-existing by rebuilding from
master.

Effect: the library's most distinctive feature appears only in quickstart prose
and is missing from the API docs. Fix by listing them explicitly in
`docs/interface.rst` or documenting the `next_`/`last_` + unit naming pattern.
All 28 direction/unit combinations were verified working.

### Modernize the docs theme

Cosmetic and entirely optional. `docs/_themes/kr` is a vendored copy of the old
Flask "kr" theme. It still renders correctly on current Sphinx, so this is not a
defect. Switching to furo or sphinx-rtd-theme would drop ~6 vendored files and
give mobile-responsive output plus dark mode; the tradeoff is losing the current
look and the custom sidebar templates.

## Design questions for a 2.0

These travel together and want deciding as a set rather than one at a time.

### Migrate off pytz to zoneinfo (#79)

The largest and most disruptive item. pytz is maintained but superseded by stdlib
`zoneinfo`. Delorean's public API is built on pytz semantics: it returns pytz
timezone objects, exposes `pytz.FixedOffset` in `parse()`, and uses
`localize()`/`normalize()` throughout. This is a breaking change warranting a
2.0, not a cleanup.

`tzlocal` 5.x already returns `zoneinfo.ZoneInfo` objects and delorean handles
that fine, so the two coexist today.

Note `zoneinfo` resolves DST gaps and ambiguity via the `fold` attribute under
different rules than pytz's `is_dst=False`. The tests added for that behaviour
mean a migration will fail loudly rather than silently changing answers.

### Related open issues

- **#86** `epoch` naming — partially addressed. `timestamp` and `from_timestamp`
  now exist with `epoch` as an alias. Removing the alias needs a
  `DeprecationWarning` first, which commits to a 2.0 timeline.
- **#53** ISO 8601 strings with no offset are cast to UTC; reporter argues that
  is wrong.
- **#11** month-end arithmetic: shifting from the 31st into a shorter month
  clamps. Currently `next_month(2)` from Jan 31 gives Mar 31, not Mar 28, because
  the count is applied as a single `relativedelta` rather than iteratively, which
  avoids drift.
- **#96** business-day timedelta (feature request).
- **#68** a 2015 open discussion thread; likely closeable.

## Recently completed

For context on what changed and why the above is scoped as it is.

- Build migrated to `pyproject.toml` + uv with a lockfile; `setup.py`,
  `version.py`, `MANIFEST.in` and the requirements files deleted.
- nose replaced with pytest; `make test` works again (closed #123).
- Python 3.9 dropped; matrix is 3.10–3.14. The lockfile had been carrying
  duplicate entries for ten packages to support 3.9.
- CI rebuilt: tests across five Pythons, a docs job running doctests and
  `html -W`, and a format job running black and ruff.
- Deprecated `datetime.utcnow()`/`utcfromtimestamp()` calls replaced.
- Documentation: quickstart went from 0 genuinely-executed examples to 71 (two
  blocks were marked `+SKIP` and reported as passing without running). Five
  SyntaxErrors fixed, plus factually wrong claims about `parse()` and `.naive`.
- Daylight-saving gap and ambiguity resolution documented and locked in by tests.
- `Delorean.__getattr__` bug fixed (`return` → `raise`).
- Issue tracker triaged from 27 open to 12; fifteen closed with verification.
