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
are in the approved JOS-71 revision; neither feature may hide another requirement.
Completion must leave callable parameter/default-map defaults unevaluated while
preserving explicit/literal context values. Ordinary invocation still evaluates
its callable normally. Bash word-break and attached equals forms, and actual Zsh
Tab completion, preserve the option prefix and choose the matching values.

Deliver the two issues as separate serial feature contributions. F2 composes the
completion changes with F1's callable-default behavior. The independent integrated
matrix sees both from the start; it is never withheld to manufacture a repair.
Keep each initial task's compute allocation to one unit and retain the remaining
objective allowance for planning, challenge, independent assurance and repair.
A real failure must take the recorded repair route. If none occurs, delivery can
succeed but the A-30 repair requirement remains unproved. Never sabotage a candidate.

Source/test/docs scope is the approved named paths. Every task must retain the
approved negative protected-path exclusions in its writable-path expression. Policy, CI, protected acceptance,
lockfile and package configuration stay operator-owned. Required provider checks
run the upstream suite and each contribution's new regressions. Protected acceptance
lives separately in acceptance/ because both contributions are required to pass it.
Native checks execute the approved candidate's source and write only reports/.

The revision-2 engineering constraint is the existing upstream default test suite.
Publication, budget accounting, bootstrap ownership, subscription provenance and A-30
reporting are executor/operator controls, not coding acceptance conditions. They remain
required in the delegation, exclusions and runbook. Do not assign future PR merges or
host quota accounting to candidate test evidence. The protected checks and all three
success examples are unchanged.

Publication stays on this public fork as ordinary linked per-feature PRs. The
operator reviews App-authored PRs and merges the lowest one first, with a merge
commit. Handler observes; it never merges. No upstream communication or release.

```handler-acceptance-v2
{"bindings":[{"kind":"success_example","method":"executable_check","profile_ids":["405c433e750bac08ec4c57722ccf4aebcdb453c2641b9c112b82a02247f8a2eb"],"reference_id":"SE-1"},{"kind":"success_example","method":"executable_check","profile_ids":["9b6ec5c71505e5fc4211041f4d5e6adc688b8b8af71b543bd059bc46e8353767"],"reference_id":"SE-2"},{"kind":"success_example","method":"executable_check","profile_ids":["1c7f2f3e772bedd14748849052eb58cda2ac0670d6ad3392e04ab73e1eb15e90"],"reference_id":"SE-3"},{"kind":"engineering_obligation","method":"executable_check","profile_ids":["e0580cf7fe4327b5fe14a63e69100f9ba76431dde3c754c4a992be3d9452a292"],"reference_id":"EO-1"}],"checks":[{"profile_id":"405c433e750bac08ec4c57722ccf4aebcdb453c2641b9c112b82a02247f8a2eb","requires":["completion-defaults"]},{"profile_id":"9b6ec5c71505e5fc4211041f4d5e6adc688b8b8af71b543bd059bc46e8353767","requires":["completion-defaults","completion-equals"]},{"profile_id":"1c7f2f3e772bedd14748849052eb58cda2ac0670d6ad3392e04ab73e1eb15e90","requires":["completion-defaults","completion-equals"]},{"profile_id":"a86bdfafcfc3adf891ca674f03b6ab298de10aaf1b9942da3df32be6fba41790","requires":["completion-defaults","completion-equals"]},{"profile_id":"e0580cf7fe4327b5fe14a63e69100f9ba76431dde3c754c4a992be3d9452a292","requires":[]},{"profile_id":"7dfa285225e6767e0135f8a844f5d78567bd2f2382a08166a0cc46b4657a2dee","requires":[]}],"contributions":[{"contribution_id":"completion-defaults","kind":"success_example","production_paths":["src/click/core.py"],"reference_id":"SE-1"},{"contribution_id":"completion-equals","kind":"success_example","production_paths":["src/click/shell_completion.py"],"reference_id":"SE-2"}],"schema_version":2}
```

```handler-assurance-v1
{"bindings":[{"feature_profile_ids":["405c433e750bac08ec4c57722ccf4aebcdb453c2641b9c112b82a02247f8a2eb"],"integrated_profile_ids":["a86bdfafcfc3adf891ca674f03b6ab298de10aaf1b9942da3df32be6fba41790"],"kind":"success_example","negative_profile_ids":["7dfa285225e6767e0135f8a844f5d78567bd2f2382a08166a0cc46b4657a2dee"],"reference_id":"SE-1"},{"feature_profile_ids":["9b6ec5c71505e5fc4211041f4d5e6adc688b8b8af71b543bd059bc46e8353767"],"integrated_profile_ids":["a86bdfafcfc3adf891ca674f03b6ab298de10aaf1b9942da3df32be6fba41790"],"kind":"success_example","negative_profile_ids":["7dfa285225e6767e0135f8a844f5d78567bd2f2382a08166a0cc46b4657a2dee"],"reference_id":"SE-2"},{"feature_profile_ids":["1c7f2f3e772bedd14748849052eb58cda2ac0670d6ad3392e04ab73e1eb15e90"],"integrated_profile_ids":["a86bdfafcfc3adf891ca674f03b6ab298de10aaf1b9942da3df32be6fba41790"],"kind":"success_example","negative_profile_ids":["7dfa285225e6767e0135f8a844f5d78567bd2f2382a08166a0cc46b4657a2dee"],"reference_id":"SE-3"},{"feature_profile_ids":["e0580cf7fe4327b5fe14a63e69100f9ba76431dde3c754c4a992be3d9452a292"],"integrated_profile_ids":["a86bdfafcfc3adf891ca674f03b6ab298de10aaf1b9942da3df32be6fba41790"],"kind":"engineering_obligation","negative_profile_ids":["7dfa285225e6767e0135f8a844f5d78567bd2f2382a08166a0cc46b4657a2dee"],"reference_id":"EO-1"}],"schema_version":1}
```
