# Click objective fork

This public fork delivers the real behaviors reported in pallets/click#2614 and
pallets/click#2847 under one explicitly approved Handler objective.

- Match Click's existing Python, typing, test and documentation conventions.
- Work on topic branches; the operator reviews and merges ordinary PRs bottom-up.
- Preserve upstream license and attribution. Do not contact upstream maintainers
  or publish a release as part of this objective.
- The approved scope is the named source/test/docs paths, not the whole repository.
- `.handler/`, `.github/`, `acceptance/`, `ci/`, `pyproject.toml` and `uv.lock` are
  operator-owned and protected from task mutation.
- Every role receives the full integrated requirement. Run the named local check
  for a feature and the protected objective checks for the composed candidate.
- Do not weaken checks, hide callable-default execution, or fake a repair.
- Tests verify public Click behavior. Substitute external boundaries only where
  isolation requires it; do not replace production completion or parsing.
- Keep source and Git metadata unchanged during independent checks; write reports
  and temporary test data only under the declared `reports/` output directory.

The provider-required `handler-check` runs the upstream `tests/` suite, including
each contribution's new public regressions, lint and typing. Protected whole-
objective tests live separately in `acceptance/` and run in Handler's independent
assurance. They intentionally fail on the approved unfixed base and need both
contributions. This avoids requiring a later contribution on the bottom PR.
