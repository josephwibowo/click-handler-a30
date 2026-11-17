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

Objective acceptance is held out (SPEC §12.1, D-0107). The `click-held-out-*` controls
run files the operator installed at `/opt/handler-held-out/click-equals-v1` in the native
container; no native role can read them, and this policy pins only their manifest. The
upstream suite and lint stay visible and runnable. Their reports are retained like any
check output.

The orchestrator chooses bounded actions and working-plan revisions. Investigator
turns observe without candidate writes; assessor turns independently judge an exact
retained submission. Only the tier-selected implementer may mutate the admitted
candidate scope. All four use the operator's Claude subscription through the pinned
Claude Code fixture, `claude-opus-5-5` / `high`. Declarations grant nothing.
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
    "tests/handler_regressions/*.json/**"
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
    "tests/handler_regressions/*.json"
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
    "tests/handler_regressions/*.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "/handler-held-out/check_held_out.py",
          "defaults"
        ],
        "artifacts": [
          "reports/held-out-defaults.xml"
        ],
        "expects": "junit_xml",
        "held_out": {
          "files": [
            {
              "path": "acceptance/__init__.py",
              "mode": "100644",
              "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
              "byte_size": 0
            },
            {
              "path": "acceptance/shell_probe.py",
              "mode": "100644",
              "sha256": "48f686285d8452989863a5464789771473a2e3f1e287fde54614fd316cdfec30",
              "byte_size": 6062
            },
            {
              "path": "acceptance/test_completion_defaults.py",
              "mode": "100644",
              "sha256": "8877a0f1fe92e8d334c767f5244730fba14c114aa02a0ea0307b582f8a00990e",
              "byte_size": 4486
            },
            {
              "path": "acceptance/test_equals_shells.py",
              "mode": "100644",
              "sha256": "ef97e21864b81cd67086d3714a85d0bce71e114e168de5af0b3bfa79459281db",
              "byte_size": 4526
            },
            {
              "path": "acceptance/test_negative_inputs.py",
              "mode": "100644",
              "sha256": "973ecf0960d50adc8653ae595c0e862e3e89b241d6f17b6411aec8686be3ef59",
              "byte_size": 1145
            },
            {
              "path": "check_held_out.py",
              "mode": "100644",
              "sha256": "6b67cca7f0af4713c9ba9dcc97b0c33befc2cba26dd26d267c11c65b8a1121d5",
              "byte_size": 2632
            },
            {
              "path": "pytest.ini",
              "mode": "100644",
              "sha256": "aaabed120d2fb059160bb38bf8843dc0bbb6abca5f013dffb5228bfffb9a3404",
              "byte_size": 39
            }
          ],
          "root": "/opt/handler-held-out/click-equals-v1"
        },
        "working_directory": ""
      }
    ],
    "name": "click-held-out-defaults"
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
    "tests/handler_regressions/*.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "/handler-held-out/check_held_out.py",
          "equals"
        ],
        "artifacts": [
          "reports/held-out-equals.xml"
        ],
        "expects": "junit_xml",
        "held_out": {
          "files": [
            {
              "path": "acceptance/__init__.py",
              "mode": "100644",
              "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
              "byte_size": 0
            },
            {
              "path": "acceptance/shell_probe.py",
              "mode": "100644",
              "sha256": "48f686285d8452989863a5464789771473a2e3f1e287fde54614fd316cdfec30",
              "byte_size": 6062
            },
            {
              "path": "acceptance/test_completion_defaults.py",
              "mode": "100644",
              "sha256": "8877a0f1fe92e8d334c767f5244730fba14c114aa02a0ea0307b582f8a00990e",
              "byte_size": 4486
            },
            {
              "path": "acceptance/test_equals_shells.py",
              "mode": "100644",
              "sha256": "ef97e21864b81cd67086d3714a85d0bce71e114e168de5af0b3bfa79459281db",
              "byte_size": 4526
            },
            {
              "path": "acceptance/test_negative_inputs.py",
              "mode": "100644",
              "sha256": "973ecf0960d50adc8653ae595c0e862e3e89b241d6f17b6411aec8686be3ef59",
              "byte_size": 1145
            },
            {
              "path": "check_held_out.py",
              "mode": "100644",
              "sha256": "6b67cca7f0af4713c9ba9dcc97b0c33befc2cba26dd26d267c11c65b8a1121d5",
              "byte_size": 2632
            },
            {
              "path": "pytest.ini",
              "mode": "100644",
              "sha256": "aaabed120d2fb059160bb38bf8843dc0bbb6abca5f013dffb5228bfffb9a3404",
              "byte_size": 39
            }
          ],
          "root": "/opt/handler-held-out/click-equals-v1"
        },
        "working_directory": ""
      }
    ],
    "name": "click-held-out-equals"
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
    "tests/handler_regressions/*.json"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/usr/local/share/handler-click-checks/bin/python",
          "/handler-held-out/check_held_out.py",
          "negative"
        ],
        "artifacts": [
          "reports/held-out-negative.xml"
        ],
        "expects": "junit_xml",
        "held_out": {
          "files": [
            {
              "path": "acceptance/__init__.py",
              "mode": "100644",
              "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
              "byte_size": 0
            },
            {
              "path": "acceptance/shell_probe.py",
              "mode": "100644",
              "sha256": "48f686285d8452989863a5464789771473a2e3f1e287fde54614fd316cdfec30",
              "byte_size": 6062
            },
            {
              "path": "acceptance/test_completion_defaults.py",
              "mode": "100644",
              "sha256": "8877a0f1fe92e8d334c767f5244730fba14c114aa02a0ea0307b582f8a00990e",
              "byte_size": 4486
            },
            {
              "path": "acceptance/test_equals_shells.py",
              "mode": "100644",
              "sha256": "ef97e21864b81cd67086d3714a85d0bce71e114e168de5af0b3bfa79459281db",
              "byte_size": 4526
            },
            {
              "path": "acceptance/test_negative_inputs.py",
              "mode": "100644",
              "sha256": "973ecf0960d50adc8653ae595c0e862e3e89b241d6f17b6411aec8686be3ef59",
              "byte_size": 1145
            },
            {
              "path": "check_held_out.py",
              "mode": "100644",
              "sha256": "6b67cca7f0af4713c9ba9dcc97b0c33befc2cba26dd26d267c11c65b8a1121d5",
              "byte_size": 2632
            },
            {
              "path": "pytest.ini",
              "mode": "100644",
              "sha256": "aaabed120d2fb059160bb38bf8843dc0bbb6abca5f013dffb5228bfffb9a3404",
              "byte_size": 39
            }
          ],
          "root": "/opt/handler-held-out/click-equals-v1"
        },
        "working_directory": ""
      }
    ],
    "name": "click-held-out-negative"
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
    "tests/handler_regressions/*.json"
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
    "auth_mode": "claude_subscription",
    "cancel_grace_seconds": 8,
    "claude_cli_version": "2.1.322",
    "container_id": "20ef8a5aec1c87afbfc74b14ccae14874c830b53306d885e35c3825677b921e0",
    "endpoint": "http://127.0.0.1:55523",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 90,
    "image_digest": "sha256:1d4e7e96509debe7b9c961e2f4c82c1e690ccec37986c112f74985c96361de87",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "claude-opus-5-5",
    "model_provider": "anthropic",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "profile_id": "click-a30-orchestrator-claude-v1",
    "reasoning_effort": "high",
    "role": "orchestrator",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "Bash",
      "Read",
      "Glob",
      "Grep"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-claude-g0-home",
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
    "auth_mode": "claude_subscription",
    "cancel_grace_seconds": 8,
    "claude_cli_version": "2.1.322",
    "container_id": "20ef8a5aec1c87afbfc74b14ccae14874c830b53306d885e35c3825677b921e0",
    "endpoint": "http://127.0.0.1:55523",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 90,
    "image_digest": "sha256:1d4e7e96509debe7b9c961e2f4c82c1e690ccec37986c112f74985c96361de87",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "claude-opus-5-5",
    "model_provider": "anthropic",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "profile_id": "click-a30-investigator-claude-v1",
    "reasoning_effort": "high",
    "role": "investigator",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "Bash",
      "Read",
      "Glob",
      "Grep"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-claude-g0-home",
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
    "auth_mode": "claude_subscription",
    "cancel_grace_seconds": 8,
    "claude_cli_version": "2.1.322",
    "container_id": "20ef8a5aec1c87afbfc74b14ccae14874c830b53306d885e35c3825677b921e0",
    "endpoint": "http://127.0.0.1:55523",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 300,
    "image_digest": "sha256:1d4e7e96509debe7b9c961e2f4c82c1e690ccec37986c112f74985c96361de87",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "claude-opus-5-5",
    "model_provider": "anthropic",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "profile_id": "click-a30-implementer-claude-v1",
    "reasoning_effort": "high",
    "role": "implementer",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "Bash",
      "Read",
      "Glob",
      "Grep",
      "Edit",
      "Write"
    ],
    "validation_timeout_seconds": 270,
    "volume_name": "handler-claude-g0-home",
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
    "auth_mode": "claude_subscription",
    "cancel_grace_seconds": 8,
    "claude_cli_version": "2.1.322",
    "container_id": "20ef8a5aec1c87afbfc74b14ccae14874c830b53306d885e35c3825677b921e0",
    "endpoint": "http://127.0.0.1:55523",
    "environment": {
      "LANG": "C.UTF-8",
      "PATH": "/usr/local/bin:/usr/bin:/bin"
    },
    "idle_timeout_seconds": 390,
    "image_digest": "sha256:1d4e7e96509debe7b9c961e2f4c82c1e690ccec37986c112f74985c96361de87",
    "max_context_bytes": 65536,
    "mcp_servers": [],
    "model": "claude-opus-5-5",
    "model_provider": "anthropic",
    "native_home": "/home/openhands",
    "native_python": "/home/openhands/spike-native-venv/bin/python",
    "profile_id": "click-a30-assessor-claude-v1",
    "reasoning_effort": "high",
    "role": "assessor",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "Bash",
      "Read",
      "Glob",
      "Grep"
    ],
    "validation_timeout_seconds": 360,
    "volume_name": "handler-claude-g0-home",
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
      "profile_id": "click-a30-implementer-claude-v1"
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
