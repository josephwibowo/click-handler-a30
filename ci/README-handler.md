# Handler fork preparation

The source baseline is pallets/click at
`2247b35ea1c47c727d7a06e51fa280e12a863ff6`. Both upstream issues remain unfixed
in this bootstrap. The independent `acceptance/` matrix must fail there.

The following commands are mandatory local evidence for the applicable exact
candidate. Run in Ubuntu 24.04 amd64, retaining environment and candidate identity,
raw JUnit for pytest, and each command's output and exit. The full-host pytest rows
include new regressions and do not inherit the native sandbox's literal `/tmp`
exclusion. The existing stress deselection remains in project configuration.

```sh
uv run --locked --python 3.10 --no-default-groups --group tests pytest tests -p no:cacheprovider --junitxml=/results/upstream-3.10.xml --basetemp=/results/tmp-3.10
uv run --locked --python 3.13 --no-default-groups --group tests pytest tests -p no:cacheprovider --junitxml=/results/upstream-3.13.xml --basetemp=/results/tmp-3.13
uv run --locked --python 3.13 --no-default-groups --group dev ruff check --no-fix .
uv run --locked --python 3.13 --no-default-groups --group dev ruff format --check .
uv run --locked --python 3.13 --no-default-groups --group typing mypy
uv run --locked --python 3.13 --no-default-groups --group typing pyright --ignoreexternal --verifytypes click
```

Use a fresh operator-owned absolute output directory (`/results` above), with
separate report and temporary paths for each Python row. The pytest additions
only place evidence and scratch output outside the candidate; they do not change
test selection. Retain genuine raw JUnit, including distinct skips/xfails and
failures/errors, and each row's stdout/stderr and exit code. The four static-tool
rows retain their real stdout/stderr and exits; do not manufacture JUnit passes
for them.

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

The six protected native modes and seven profiles remain separately mandatory SQL
observations. `check_objective.py lint` (EO-2) runs Ruff and mypy; pyright runs
in the local matrix because its Node child cannot run in the native sandbox.
External matrix reports are not SQL mandatory observations or provider statuses.
The protected objective matrix runs against the composed candidate. Release,
nightly and lock automation stays disabled on this fork.

Before approving JOS-73, the operator must bind exact runtime identities and
assurance profiles, finish the whole-objective shell checks, prove the public
fork's integration-only ruleset, and present the exact revision/delegation digest.
The independent Bash/Zsh tests require supported real shells; absence is a refusal,
not a skip. Preserve the authenticated Handler fixture unchanged.

The default budget proposal is 12 compute units and 10 delivery actions. A tracker
ticket, this bootstrap and a passing local matrix grant no runtime or publication
authority. No upstream comment/PR, release or automatic merge is authorized.
