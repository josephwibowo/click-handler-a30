---
id: click-completion-checks
name: click-completion-checks
kind: procedure
status: active
description: Run local and integrated frozen Click checks against the candidate.
scope:
  - src/click/**
evidence: []
supersedes: []
---

# Click completion checks

Read the approved completion contract and corpus index. Match Click's existing
Python/testing conventions; use public behavior and name each regression.
Run the check named by the admitted task, then the protected composed check:

- `/home/openhands/spike-native-venv/bin/python ci/check_objective.py defaults`: callable/default-map behavior and controls.
- `/home/openhands/spike-native-venv/bin/python ci/check_objective.py equals`: word-break/attached equals completion.
- `/home/openhands/spike-native-venv/bin/python ci/check_objective.py integrated`: whole-objective independent matrix.
- `/home/openhands/spike-native-venv/bin/python ci/check_objective.py upstream`: full upstream default tests, excluding
  the 31,000 stress cases upstream normally deselects and the one case that reads
  the literal host /tmp, which the native sandbox hides.
- `/home/openhands/spike-native-venv/bin/python ci/check_objective.py lint`: the required check's
  ruff check, ruff format --check and mypy, as the workflow runs them.
  Format the files you changed first (`/home/openhands/spike-native-venv/bin/python -m ruff
  format --no-cache <paths>`); fix lint and type findings in the source, never with
  configuration or ignore comments.

Report real outcomes and named failures. Missing Bash >=4.4 or Zsh is a refusal,
never a skip. Do not edit `.handler/`, `.github/`, `acceptance/`, `ci/`, pyproject
or uv.lock. Do not weaken an approved check or manufacture a repair. Source and
Git metadata stay read-only during independent checks; only reports/ is an output.
No credential, database or publisher access is granted to native roles.
