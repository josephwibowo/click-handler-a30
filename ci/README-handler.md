# Handler fork preparation

The source baseline is pallets/click at
`2247b35ea1c47c727d7a06e51fa280e12a863ff6`. Both upstream issues remain unfixed
in this bootstrap. The independent `acceptance/` matrix must fail there.

`handler-check` requires the upstream suite, lint and typing. Handler runs its
ruff and mypy steps as `check_objective.py lint` (EO-2) on every task and the
composed candidate; its `pyright --verifytypes` step cannot run in the native
sandbox, which refuses the Node child process pyright starts. The protected
objective matrix runs separately after the composed candidate exists. Actions
uses public standard runners, pinned actions, read-only repository permissions
and no secrets. Release/nightly/lock automation stays disabled on this fork.

Before approving JOS-73, the operator must bind exact runtime identities and
assurance profiles, finish the whole-objective shell checks, prove the public
fork's integration-only ruleset, and present the exact revision/delegation digest.
The independent Bash/Zsh tests require supported real shells; absence is a refusal,
not a skip. Preserve the authenticated Handler fixture unchanged.

The default budget proposal is 12 compute units and 10 delivery actions. A tracker
ticket, this bootstrap and a passing CI run grant no runtime or publication
authority. No upstream comment/PR, release or automatic merge is authorized.
