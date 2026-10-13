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
are in the approved JOS-60 revision; neither feature may hide another requirement.
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

Publication stays on this public fork as ordinary linked per-feature PRs. The
operator reviews App-authored PRs and merges the lowest one first, with a merge
commit. Handler observes; it never merges. No upstream communication or release.

```handler-acceptance-v2
{"bindings":[{"kind":"success_example","method":"executable_check","profile_ids":["3141fefb3c5c2ca9c34f31488cc93bc3f4b673a29ffd83b127cd196894d87028"],"reference_id":"SE-1"},{"kind":"success_example","method":"executable_check","profile_ids":["239fd0fc3a8238dee23e0073d3bc8559809171094a92144183615be66b80870d"],"reference_id":"SE-2"},{"kind":"success_example","method":"executable_check","profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"reference_id":"SE-3"},{"kind":"engineering_obligation","method":"executable_check","profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:796da8afa8ff61ca2f5490cdf1b281fc676377ac9cc6b4abdeea90687ee4a355"},{"kind":"engineering_obligation","method":"executable_check","profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:1093aac86a9b19448049a28489dc46df7e75c938ff01ebf13bbf59fafff904b9"},{"kind":"engineering_obligation","method":"executable_check","profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:5272bd537cd498db9f9ad27f39d11508ef8dd15e438c814c5cf12e656e4d5368"},{"kind":"engineering_obligation","method":"executable_check","profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:e3b5e46dba7a30ae973eed9c7713207d19cadcb29105981c439dfd033d46387f"}],"checks":[{"profile_id":"3141fefb3c5c2ca9c34f31488cc93bc3f4b673a29ffd83b127cd196894d87028","requires":["completion-defaults"]},{"profile_id":"239fd0fc3a8238dee23e0073d3bc8559809171094a92144183615be66b80870d","requires":["completion-defaults","completion-equals"]},{"profile_id":"c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179","requires":["completion-defaults","completion-equals"]},{"profile_id":"e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5","requires":[]}],"contributions":[{"contribution_id":"completion-defaults","kind":"success_example","production_paths":["src/click/core.py"],"reference_id":"SE-1"},{"contribution_id":"completion-equals","kind":"success_example","production_paths":["src/click/shell_completion.py"],"reference_id":"SE-2"}],"schema_version":2}
```

```handler-assurance-v1
{"bindings":[{"feature_profile_ids":["3141fefb3c5c2ca9c34f31488cc93bc3f4b673a29ffd83b127cd196894d87028"],"integrated_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"kind":"success_example","negative_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"SE-1"},{"feature_profile_ids":["239fd0fc3a8238dee23e0073d3bc8559809171094a92144183615be66b80870d"],"integrated_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"kind":"success_example","negative_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"SE-2"},{"feature_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"integrated_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"kind":"success_example","negative_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"SE-3"},{"feature_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"integrated_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"kind":"engineering_obligation","negative_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:796da8afa8ff61ca2f5490cdf1b281fc676377ac9cc6b4abdeea90687ee4a355"},{"feature_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"integrated_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"kind":"engineering_obligation","negative_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:1093aac86a9b19448049a28489dc46df7e75c938ff01ebf13bbf59fafff904b9"},{"feature_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"integrated_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"kind":"engineering_obligation","negative_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:5272bd537cd498db9f9ad27f39d11508ef8dd15e438c814c5cf12e656e4d5368"},{"feature_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"integrated_profile_ids":["c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"],"kind":"engineering_obligation","negative_profile_ids":["e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"],"reference_id":"obligation:e3b5e46dba7a30ae973eed9c7713207d19cadcb29105981c439dfd033d46387f"}],"schema_version":1}
```
