# Click objective fork

This public fork is prepared to deliver the real behaviors reported in
pallets/click#2614 and pallets/click#2847 under one explicitly approved fresh
Handler objective. Bootstrap preparation grants no objective authority.

- Match Click's existing Python, typing, test and documentation conventions.
- Work on topic branches; the operator reviews and merges ordinary PRs bottom-up.
- Preserve upstream license and attribution. Do not contact upstream maintainers
  or publish a release as part of this objective.
- The approved scope is the named source/test/docs paths, not the whole repository.
- `.handler/`, `.github/`, `acceptance/`, `ci/`, `pyproject.toml` and `uv.lock` are
  operator-owned and protected from candidate mutation.
- Every role receives the full integrated requirement. Run the named local check
  for a feature and the protected objective checks for the composed candidate.
- Do not weaken checks, hide callable-default execution, or fake a repair.
- Tests verify public Click behavior. Substitute external boundaries only where
  isolation requires it; do not replace production completion or parsing.
- Keep source and Git metadata unchanged during independent checks; write reports
  and temporary test data only under the declared `reports/` output directory.

The operator must retain local evidence for the exact applicable candidate on
Ubuntu 24.04 amd64: the upstream `tests/` suite on Python 3.10 and 3.13, and on
Python 3.13 Ruff check, Ruff format check, mypy and pyright. Run the six locked
commands in `ci/README-handler.md`, retaining raw reports, output, exit codes,
environment and candidate identity. The full-host suite includes new regressions
and does not inherit the native sandbox's literal `/tmp` exclusion. Missing or
failing evidence blocks delivery; it is not a provider status or a Handler SQL
mandatory observation. The protected native checks remain separately mandatory.

The approved delivery policy requires protected human review and
`provider_checks: none`. Before publication, the operator must positively prove
zero effective provider-required checks and all applicable protections for the
integration branch. Joseph is the named eligible human reviewer.

GitHub Actions MUST remain permanently disabled in both `josephwibowo/handler`
and `josephwibowo/click-handler-a30`. Never enable, dispatch or rerun Actions, or
add hosted CI. `.github/workflows/handler-check.yml` remains inert command
provenance.

The dated observation on 28 October 2026 recorded Actions disabled in both
repositories. That historical snapshot is not fresh provider evidence for future
publication. Local results do not claim a provider check ran or passed. Human
review and merge remain operator actions.

Protected whole-objective tests live separately in `acceptance/` and run in
Handler's isolated checks and independent submission assessment. They intentionally
fail on the approved unfixed base and need both contributions; a bottom PR does
not require the later contribution.
