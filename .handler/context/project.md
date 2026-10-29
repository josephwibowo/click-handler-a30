---
id: project-profile
kind: project
status: active
description: Standing project profile naming the writable surfaces, validation profile, and context policy that bound every objective.
scope: []
evidence: []
supersedes: []
---

# Project Overlay

## Narrative

The prose in this file is explanatory; machine-read declarations use typed fences.

This uncommitted bootstrap draft binds all four role declarations to the selected
current, non-archived proof substrate using dated target metadata from 2026-10-22.
The existing physical container and native login volume may support a separately
authorized fresh operational scope; these declarations require neither a newly
created container nor another login. Current outer-profile and sandbox readbacks,
the six frozen check modes, source validation, review and the bootstrap commit
remain pending. The final committed policy and fresh database, artifact namespace,
candidate/control/attempt scope and owned engine must be selected before native
objective execution. No archived target, old namespace, draft declaration or dated
readback grants objective authority. Image, SDK/CLI, interpreter and permission
pins remain required contracts, not proof of current runtime readiness.

The orchestrator chooses bounded actions and working-plan revisions. Investigator
turns observe without candidate writes; assessor turns independently judge an exact
retained submission. Only the tier-selected implementer may mutate the admitted
candidate scope. All four use the declared native ChatGPT subscription, with the
existing `gpt-6.1-sol` / `high` selection retained. Declarations grant nothing.
Zero-write knowledge proposal and independent review use the investigator and
assessor profiles when supported; proposed notes gain no authority before the
operator merges them.

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

```handler:identity
{
  "repository_identity": "Click completion objective"
}
```

```handler:conventions
{
  "branch_prefix": "codex/",
  "integration_branch": "main",
  "worktree_pattern": "../click-{slug}"
}
```

```handler:floor
{
  "level": "standard"
}
```

```handler:forbidden
{
  "globs": [
    ".handler/**",
    ".github/**",
    "acceptance/**",
    "ci/**",
    "pyproject.toml",
    "uv.lock",
    "**/.env*",
    "**/*.pem",
    "tests/handler_regressions/callable_defaults.json/**",
    "tests/handler_regressions/equals_completion.json/**",
    "tests/handler_regressions/integrated_completion.json/**"
  ]
}
```

```handler:surface
{
  "globs": [
    "src/click/core.py",
    "src/click/shell_completion.py",
    "tests/test_shell_completion.py",
    "tests/test_defaults.py",
    "tests/test_context.py",
    "tests/test_parser.py",
    "docs/shell-completion.md",
    "CHANGES.md",
    "tests/handler_regressions/callable_defaults.json",
    "tests/handler_regressions/equals_completion.json",
    "tests/handler_regressions/integrated_completion.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "ci/check_objective.py",
          "upstream-workflow"
        ],
        "artifacts": [
          "reports/upstream-workflow.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-upstream",
    "profile_id": "918ff36224e2774a3f47b5cdaca548cad3a73ff332bd9dcc69ab0f0f4914917b"
  }
}
```

```handler:surface
{
  "globs": [
    "src/click/core.py",
    "src/click/shell_completion.py",
    "tests/test_shell_completion.py",
    "tests/test_defaults.py",
    "tests/test_context.py",
    "tests/test_parser.py",
    "docs/shell-completion.md",
    "CHANGES.md",
    "tests/handler_regressions/callable_defaults.json",
    "tests/handler_regressions/equals_completion.json",
    "tests/handler_regressions/integrated_completion.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "ci/check_objective.py",
          "defaults"
        ],
        "artifacts": [
          "reports/defaults.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-defaults",
    "profile_id": "61b3300a3521fb24b721f61b313c9e26363b923c3a594dca4b2563a8a564f09e"
  }
}
```

```handler:surface
{
  "globs": [
    "src/click/core.py",
    "src/click/shell_completion.py",
    "tests/test_shell_completion.py",
    "tests/test_defaults.py",
    "tests/test_context.py",
    "tests/test_parser.py",
    "docs/shell-completion.md",
    "CHANGES.md",
    "tests/handler_regressions/callable_defaults.json",
    "tests/handler_regressions/equals_completion.json",
    "tests/handler_regressions/integrated_completion.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "ci/check_objective.py",
          "equals"
        ],
        "artifacts": [
          "reports/equals.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-equals",
    "profile_id": "d7672df0c6023c5e4fa5b38a13bd7c1c6d3580b72d5a33bc7313a1bd96873b7c"
  }
}
```

```handler:surface
{
  "globs": [
    "src/click/core.py",
    "src/click/shell_completion.py",
    "tests/test_shell_completion.py",
    "tests/test_defaults.py",
    "tests/test_context.py",
    "tests/test_parser.py",
    "docs/shell-completion.md",
    "CHANGES.md",
    "tests/handler_regressions/callable_defaults.json",
    "tests/handler_regressions/equals_completion.json",
    "tests/handler_regressions/integrated_completion.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "ci/check_objective.py",
          "integrated"
        ],
        "artifacts": [
          "reports/integrated.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-composed-feature",
    "profile_id": "6b006d908c1352131d933014f51d39c0a77c97634634b47f66c6db56ca277552"
  }
}
```

```handler:surface
{
  "globs": [
    "src/click/core.py",
    "src/click/shell_completion.py",
    "tests/test_shell_completion.py",
    "tests/test_defaults.py",
    "tests/test_context.py",
    "tests/test_parser.py",
    "docs/shell-completion.md",
    "CHANGES.md",
    "tests/handler_regressions/callable_defaults.json",
    "tests/handler_regressions/equals_completion.json",
    "tests/handler_regressions/integrated_completion.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "ci/check_objective.py",
          "integrated"
        ],
        "artifacts": [
          "reports/integrated.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-integrated",
    "profile_id": "9661a375018630436226bc0754814e37d03249086a68ed04a2f18164047dbf8f"
  }
}
```

```handler:surface
{
  "globs": [
    "src/click/core.py",
    "src/click/shell_completion.py",
    "tests/test_shell_completion.py",
    "tests/test_defaults.py",
    "tests/test_context.py",
    "tests/test_parser.py",
    "docs/shell-completion.md",
    "CHANGES.md",
    "tests/handler_regressions/callable_defaults.json",
    "tests/handler_regressions/equals_completion.json",
    "tests/handler_regressions/integrated_completion.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "ci/check_objective.py",
          "negative"
        ],
        "artifacts": [
          "reports/negative.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-negative",
    "profile_id": "d025ec624e92f0aecfc93f3b56d93e046e8ced666f986ad5fc0ba12ca32f52a1"
  }
}
```

```handler:surface
{
  "globs": [
    "src/click/core.py",
    "src/click/shell_completion.py",
    "tests/test_shell_completion.py",
    "tests/test_defaults.py",
    "tests/test_context.py",
    "tests/test_parser.py",
    "docs/shell-completion.md",
    "CHANGES.md",
    "tests/handler_regressions/callable_defaults.json",
    "tests/handler_regressions/equals_completion.json",
    "tests/handler_regressions/integrated_completion.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "ci/check_objective.py",
          "lint"
        ],
        "artifacts": [
          "reports/lint.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-lint",
    "profile_id": "72441eff5f0e44f7524c6b15fd6dd3f89086b6bdeef199bd319e7513dcf410c1"
  }
}
```

```handler:capability
{
  "budgets": {
    "reworks": 1,
    "tokens": 10000,
    "wall_clock_seconds": 300
  },
  "env_allowlist": [
    "PATH"
  ],
  "level": "standard",
  "role": "orchestrator",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "bebde9c2182cb561f2ac1ef94013215bc0ddde82001236364362dd518e0c1c7f",
    "endpoint": "http://127.0.0.1:55243",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 90,
    "image_digest": "sha256:59859aa007ee2bea2402b0259ea104d871d90e8e8c6e8788da20d3bba3f528b4",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "gpt-6.1-sol",
    "model_provider": "openai",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "permission_profile": "spike",
    "plugins_enabled": false,
    "profile_id": "click-a30-orchestrator-v2",
    "reasoning_effort": "high",
    "role": "orchestrator",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-jos42-agent-led-20261019-proof-native-login",
    "wall_clock_seconds": 300,
    "workspace_root": "/workspace/toy",
    "workspace_sdk_version": "1.53.0",
    "workspace_version": "1.53.0"
  }
}
```

```handler:capability
{
  "budgets": {
    "reworks": 1,
    "tokens": 10000,
    "wall_clock_seconds": 300
  },
  "env_allowlist": [
    "PATH"
  ],
  "level": "standard",
  "role": "investigator",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "bebde9c2182cb561f2ac1ef94013215bc0ddde82001236364362dd518e0c1c7f",
    "endpoint": "http://127.0.0.1:55243",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 90,
    "image_digest": "sha256:59859aa007ee2bea2402b0259ea104d871d90e8e8c6e8788da20d3bba3f528b4",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "gpt-6.1-sol",
    "model_provider": "openai",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "permission_profile": "spike",
    "plugins_enabled": false,
    "profile_id": "click-a30-investigator-v2",
    "reasoning_effort": "high",
    "role": "investigator",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-jos42-agent-led-20261019-proof-native-login",
    "wall_clock_seconds": 300,
    "workspace_root": "/workspace/toy",
    "workspace_sdk_version": "1.53.0",
    "workspace_version": "1.53.0"
  }
}
```

```handler:capability
{
  "budgets": {
    "reworks": 1,
    "tokens": 10000,
    "wall_clock_seconds": 900
  },
  "env_allowlist": [
    "PATH"
  ],
  "level": "standard",
  "role": "implementer",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "bebde9c2182cb561f2ac1ef94013215bc0ddde82001236364362dd518e0c1c7f",
    "endpoint": "http://127.0.0.1:55243",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 300,
    "image_digest": "sha256:59859aa007ee2bea2402b0259ea104d871d90e8e8c6e8788da20d3bba3f528b4",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "gpt-6.1-sol",
    "model_provider": "openai",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "permission_profile": "spike",
    "plugins_enabled": false,
    "profile_id": "click-a30-implementer-v2",
    "reasoning_effort": "high",
    "role": "implementer",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file",
      "write_file"
    ],
    "validation_timeout_seconds": 270,
    "volume_name": "handler-jos42-agent-led-20261019-proof-native-login",
    "wall_clock_seconds": 900,
    "workspace_root": "/workspace/toy",
    "workspace_sdk_version": "1.53.0",
    "workspace_version": "1.53.0"
  }
}
```

```handler:capability
{
  "budgets": {
    "reworks": 1,
    "tokens": 10000,
    "wall_clock_seconds": 900
  },
  "env_allowlist": [
    "PATH"
  ],
  "level": "standard",
  "role": "assessor",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "bebde9c2182cb561f2ac1ef94013215bc0ddde82001236364362dd518e0c1c7f",
    "endpoint": "http://127.0.0.1:55243",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 390,
    "image_digest": "sha256:59859aa007ee2bea2402b0259ea104d871d90e8e8c6e8788da20d3bba3f528b4",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "gpt-6.1-sol",
    "model_provider": "openai",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "permission_profile": "spike",
    "plugins_enabled": false,
    "profile_id": "click-a30-assessor-v2",
    "reasoning_effort": "high",
    "role": "assessor",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file"
    ],
    "validation_timeout_seconds": 360,
    "volume_name": "handler-jos42-agent-led-20261019-proof-native-login",
    "wall_clock_seconds": 900,
    "workspace_root": "/workspace/toy",
    "workspace_sdk_version": "1.53.0",
    "workspace_version": "1.53.0"
  }
}
```

```handler:tiers
{
  "tiers": [
    {
      "name": "default",
      "profile_id": "click-a30-implementer-v2"
    }
  ]
}
```

```handler:agent
{
  "decisions_per_run": 64,
  "unproductive_limit": 6
}
```

```handler:review
{
  "review": "required"
}
```

```handler:context
{
  "allow_required_only": true,
  "max_pack_bytes": 65536,
  "required_paths": [
    "project.md",
    "decisions/completion-contract.md",
    "procedures/click-completion-checks/SKILL.md"
  ]
}
```
