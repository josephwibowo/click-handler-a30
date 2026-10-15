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
    "**/*.pem"
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
    "CHANGES.md"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/home/openhands/spike-native-venv/bin/python",
          "ci/check_objective.py",
          "upstream"
        ],
        "artifacts": [
          "reports/upstream.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-upstream",
    "profile_id": "e0580cf7fe4327b5fe14a63e69100f9ba76431dde3c754c4a992be3d9452a292"
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
    "CHANGES.md"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/home/openhands/spike-native-venv/bin/python",
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
    "profile_id": "405c433e750bac08ec4c57722ccf4aebcdb453c2641b9c112b82a02247f8a2eb"
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
    "CHANGES.md"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/home/openhands/spike-native-venv/bin/python",
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
    "profile_id": "9b6ec5c71505e5fc4211041f4d5e6adc688b8b8af71b543bd059bc46e8353767"
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
    "CHANGES.md"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/home/openhands/spike-native-venv/bin/python",
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
    "profile_id": "1c7f2f3e772bedd14748849052eb58cda2ac0670d6ad3392e04ab73e1eb15e90"
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
    "CHANGES.md"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/home/openhands/spike-native-venv/bin/python",
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
    "profile_id": "a86bdfafcfc3adf891ca674f03b6ab298de10aaf1b9942da3df32be6fba41790"
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
    "CHANGES.md"
  ],
  "level": "standard",
  "profile": {
    "commands": [
      {
        "argv": [
          "/home/openhands/spike-native-venv/bin/python",
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
    "profile_id": "7dfa285225e6767e0135f8a844f5d78567bd2f2382a08166a0cc46b4657a2dee"
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
  "role": "planner",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "fa5798b3b6c24f372ed3d925758abe45813a0d45410ff5d0725ba4301810208a",
    "endpoint": "http://127.0.0.1:55298",
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
    "profile_id": "click-a30-planner-v1",
    "reasoning_effort": "high",
    "role": "planner",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-click-a30-native-login",
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
  "role": "reviewer",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "fa5798b3b6c24f372ed3d925758abe45813a0d45410ff5d0725ba4301810208a",
    "endpoint": "http://127.0.0.1:55298",
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
    "profile_id": "click-a30-reviewer-v1",
    "reasoning_effort": "high",
    "role": "reviewer",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-click-a30-native-login",
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
  "role": "implementer",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "fa5798b3b6c24f372ed3d925758abe45813a0d45410ff5d0725ba4301810208a",
    "endpoint": "http://127.0.0.1:55298",
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
    "profile_id": "click-a30-implementer-v1",
    "reasoning_effort": "high",
    "role": "implementer",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file",
      "write_file"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-click-a30-native-login",
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
  "role": "objective_assurance",
  "worker_config": {
    "agent_server_version": "1.53.0",
    "apps_enabled": false,
    "auth_mode": "chatgpt",
    "cancel_grace_seconds": 8,
    "codex_cli_version": "0.160.1",
    "codex_sdk_version": "0.160.1",
    "container_id": "fa5798b3b6c24f372ed3d925758abe45813a0d45410ff5d0725ba4301810208a",
    "endpoint": "http://127.0.0.1:55298",
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
    "profile_id": "click-a30-objective_assurance-v1",
    "reasoning_effort": "high",
    "role": "objective_assurance",
    "schema_version": 1,
    "startup_timeout_seconds": 90,
    "tools": [
      "exec_command",
      "read_file"
    ],
    "validation_timeout_seconds": 120,
    "volume_name": "handler-click-a30-native-login",
    "wall_clock_seconds": 300,
    "workspace_root": "/workspace/toy",
    "workspace_sdk_version": "1.53.0",
    "workspace_version": "1.53.0"
  }
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
