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
          "reports/upstream/junit.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-upstream",
    "profile_id": "e6b69d65fc7849da39bfefd439c620459fa6762a75e79a92f0463a580cefbad5"
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
          "reports/defaults/junit.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-defaults",
    "profile_id": "3141fefb3c5c2ca9c34f31488cc93bc3f4b673a29ffd83b127cd196894d87028"
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
          "reports/equals/junit.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-equals",
    "profile_id": "239fd0fc3a8238dee23e0073d3bc8559809171094a92144183615be66b80870d"
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
          "reports/integrated/junit.xml"
        ],
        "expects": "junit_xml",
        "working_directory": ""
      }
    ],
    "name": "click-integrated",
    "profile_id": "c616929cd0e89580e10d70fd4221159cfd07d94f8751f0b724507e54388cc179"
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
