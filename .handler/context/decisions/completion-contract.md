---
id: completion-contract
kind: decision
status: active
description: Frozen requirements and check bindings for both real Click completion issues.
scope:
  - src/click/core.py
  - src/click/shell_completion.py
evidence: []
supersedes: []
---

# Completion contract

The two source issues are pallets/click#2614 and #2847. Their complete requirements
are in JOS-73; a fresh imported revision must preserve them and receive explicit
approval. Neither feature may hide another requirement.
Completion must leave callable parameter/default-map defaults unevaluated while
preserving explicit/literal context values. Ordinary invocation still evaluates
its callable normally. Bash word-break and attached equals forms, and actual Zsh
Tab completion, preserve the option prefix and choose the matching values.

Deliver the two issues as separate serial feature contributions. The equals
contribution composes with the callable-default contribution. The independent
integrated matrix sees both from the start; it is never withheld to manufacture a
repair. The orchestrator chooses implementation slices, investigations, checks and
working-plan revisions within the approved objective and finite allowance; this
note imposes no fixed task count or repair route. Retain enough objective allowance
for independent assessment, genuine repair and continuation.

A real failure requires immutable test-first repair: retain the observed failure,
prepare the required regression separately, implement the repair under its own
funded admission, and obtain fresh exact-case passes and independent assessment.
Ordinary implementation cannot bypass known repair preparation. If no genuine
failure occurs, delivery can succeed but A-30 repair remains unproved. Never
sabotage a candidate.

Source/test/docs scope is the approved named paths. Every implementation admission
must retain the approved negative protected-path exclusions in its writable-path
expression. Policy, CI, protected acceptance, lockfile and package configuration
stay operator-owned. Protected acceptance lives separately in acceptance/ because
both contributions are required to pass it.

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

Native checks execute the approved candidate's source and write only reports/.

The revision-2 engineering constraint is the existing upstream default test suite.
Publication, budget accounting, bootstrap ownership, subscription provenance and A-30
reporting are host/operator controls, not coding acceptance conditions. They remain
required in the delegation, exclusions and runbook. Do not assign future PR merges or
host quota accounting to candidate test evidence. The protected checks and all three
success examples are unchanged.

EO-2 is the protected native ruff and mypy gate: ruff check, ruff format --check
and mypy with the uv.lock tool versions and pyproject configuration, run by
`ci/check_objective.py lint` (profile `click-lint`). Every
implementation slice and retained submission must satisfy EO-2 beside EO-1,
and independent assessment requires fresh observations on the composed candidate.
Fix a finding in the source; never change the tool configuration or suppress it with an ignore
comment.

Publication stays on this public fork as ordinary linked per-feature PRs. The
operator reviews App-authored PRs and merges the lowest one first, with a merge
commit. Handler observes; it never merges. No upstream communication or release.

## Required evidence and check matrix

These are the unchanged SE/EO expectations and contribution dependencies. They are
required context for the orchestrator and independent assessor. Current Handler
pins each `handler:surface` command as a mandatory control at approval; this note
does not define a second acceptance parser or a task/feature binding protocol.
Every check in the table is mandatory, including the independent integrated and
negative controls. Agent-added checks are advisory observations; independent
assessment judges their relevance, and they cannot waive mandatory controls or
immutable required regression cases. Missing/corrupt reports, collection errors,
failures and skips cannot become behavioral passes. EO-1 uses the protected
workflow-step method below; inner platform skips remain skipped evidence.

| Reference | Required behavior/evidence | Feature observation | Independent composed observation | Negative controls |
| --- | --- | --- | --- | --- |
| SE-1 | Callable parameter/default-map defaults stay unevaluated during completion; explicit/literal context values and ordinary invocation remain correct. | `click-defaults` | `click-integrated` | `click-negative` |
| SE-2 | Bash word-break/split and attached equals forms preserve the option prefix and matching values; actual Zsh Tab completion works. | `click-equals` | `click-integrated` | `click-negative` |
| SE-3 | Both completion behaviors work together through the actual clean Bash/Zsh interaction, including ordinary invocation afterward. | `click-composed-feature` | `click-integrated` | `click-negative` |
| EO-1 | Successful existing upstream default-suite workflow process, preserving the frozen stress-case deselection and one explicit literal-host `/tmp` exclusion. | `click-upstream` | `click-integrated` | `click-negative` |
| EO-2 | Lock-pinned ruff check, ruff format --check and mypy with unchanged project configuration; fix findings in source without ignores. | `click-lint` | `click-integrated` | `click-negative` |

`completion-defaults` addresses SE-1 in `src/click/core.py`.
`completion-equals` addresses SE-2 in `src/click/shell_completion.py` and composes
with `completion-defaults`. The defaults check depends on the first contribution;
the equals, composed-feature and integrated checks depend on both. Upstream,
negative and lint checks have no contribution prerequisite. Independent assessment
still checks all objective requirements against the exact cumulative submission.

The protected profile identities and commands remain:

| Profile | Mode / report under `reports/` | Profile ID |
| --- | --- | --- |
| `click-defaults` | `defaults` / `defaults.xml` | `61b3300a3521fb24b721f61b313c9e26363b923c3a594dca4b2563a8a564f09e` |
| `click-equals` | `equals` / `equals.xml` | `d7672df0c6023c5e4fa5b38a13bd7c1c6d3580b72d5a33bc7313a1bd96873b7c` |
| `click-composed-feature` | `integrated` / `integrated.xml` | `6b006d908c1352131d933014f51d39c0a77c97634634b47f66c6db56ca277552` |
| `click-integrated` | `integrated` / `integrated.xml` | `9661a375018630436226bc0754814e37d03249086a68ed04a2f18164047dbf8f` |
| `click-upstream` | `upstream-workflow` / `upstream-workflow.xml` | `918ff36224e2774a3f47b5cdaca548cad3a73ff332bd9dcc69ab0f0f4914917b` |
| `click-negative` | `negative` / `negative.xml` | `d025ec624e92f0aecfc93f3b56d93e046e8ced666f986ad5fc0ba12ca32f52a1` |
| `click-lint` | `lint` / `lint.xml` | `72441eff5f0e44f7524c6b15fd6dd3f89086b6bdeef199bd319e7513dcf410c1` |

Submission coverage claims grant nothing. Independent initial assessment judges the
exact retained checkpoint, approved requirements, environment, producer and fresh
mandatory/regression evidence. Changed bases require fresh rebased assessment
before restricted continuation. A retained finding closes only on immutable
observed fail/repair/pass evidence. Human merges remain the operator's action.

EO-1 certifies the named `protected_workflow::upstream_default_pytest_process_succeeds`
process outcome only. Its new protected `upstream-workflow` command must exit zero
and produce complete, nonempty, unique original JUnit with at least one genuine
pass and no failures/errors or contradictory counts. The captured outer JUnit
retains exact original bytes as base64, SHA256, counts and all case identities
in `system-out`; inner skips/xfails are explicitly preserved as skips, never
claimed executed passes. Independent assessment reads that evidence. This
workflow case cannot certify immutable required regressions or close retained
findings without their separate exact-case failure/repair/pass evidence.
