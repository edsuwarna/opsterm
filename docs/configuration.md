# ⚙️ Configuration

OpsTerm is configured through YAML files in `~/.opsterm/`.

> 📦 Changed from `~/.ai-workflows` → `~/.opsterm/` (auto-migrates on first run)

## Config Directory

All config files live in `~/.opsterm/`:

```
~/.opsterm/
├── config.yaml       ← AI provider, model, settings
├── servers.yaml      ← SSH server definitions
├── workflows.yaml    ← Workflow definitions
├── vault.json        ← Encrypted credentials (AES-128 + PBKDF2)
├── history.db        ← SQLite command history
└── last_*.txt        ← Last command/output cache
```

## config.yaml — AI Provider

```yaml
ai:
  provider: opencode       # Provider label (informational)
  api_url: "https://opencode.ai/zen/go/v1/chat/completions"
  api_key: ""              # Set via env var: OPSTERM_API_KEY
  model: deepseek-v4-flash
  temperature: 0.3
  max_tokens: 1024

shell:
  confirm_before_exec: true
  auto_exec_patterns:
    - "^ssh "
    - "^kubectl "
    - "^docker "
    - "^cd "
```

### Config Keys

| Key | Default | Description |
|-----|---------|-------------|
| `ai.api_url` | `https://api.deepseek.com/...` | OpenAI-compatible API endpoint |
| `ai.api_key` | `""` | API key (set via env var for safety) |
| `ai.model` | `deepseek-chat` | Model name |
| `ai.temperature` | `0.3` | Response creativity (0-1) |
| `ai.max_tokens` | `1024` | Max response length |
| `shell.confirm_before_exec` | `true` | Ask before executing suggested commands |
| `shell.auto_exec_patterns` | — | Regex patterns for auto-execution |

### Supported Providers

| Provider | API URL | Model |
|----------|---------|-------|
| OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-4o`, `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/v1/chat/completions` | `deepseek-chat`, `deepseek-coder` |
| OpenRouter | `https://openrouter.ai/api/v1/chat/completions` | `anthropic/claude-sonnet-4` |
| Ollama (local) | `http://localhost:11434/v1/chat/completions` | `llama3`, `qwen2.5` |
| OpenCode | `https://opencode.ai/zen/go/v1/chat/completions` | `deepseek-v4-flash` |

## servers.yaml — SSH Servers

```yaml
servers:
  vps-utama:
    host: "43.157.204.199"
    user: "ubuntu"
    port: 22
    key: "~/.ssh/id_ed25519"
    desc: "Production VPS"

  internal-server:
    host: "10.0.0.5"
    user: "admin"
    port: 2222
    proxy: "bastion"         # Route through bastion host
    desc: "Internal via jump host"
```

### Server Keys

| Key | Required | Description |
|-----|----------|-------------|
| `host` | ✅ | IP or hostname |
| `user` | ✅ | SSH user (default: root) |
| `port` | ❌ | SSH port (default: 22) |
| `key` | ❌ | SSH key path (default: ~/.ssh/id_ed25519) |
| `proxy` | ❌ | Jump host server name (multi-hop) |
| `desc` | ❌ | Description/label |

## workflows.yaml — Automation

```yaml
workflows:
  cek-server:
    desc: "Cek status server"
    steps:
      - ssh: vps-utama
        command: "uptime && df -h / && free -h"
        desc: "System health check"

  deploy-full:
    desc: "Full deployment"
    steps:
      - scp: "./docker-compose.yml"
        to: "/opt/app/docker-compose.yml"
        ssh: vps-utama
        desc: "Upload config"
      - ssh: vps-utama
        command: "cd /opt/app && docker compose restart"
        desc: "Restart containers"
      - command: "echo '✅ Done!'"
        desc: "Notification"
```

### Step Types

| Type | Fields | Description |
|------|--------|-------------|
| `ssh` | `ssh`, `command`, `desc` | Run command on remote server |
| `command` | `command`, `desc` | Run command locally |
| `scp` | `scp` (src), `to` (dst), `ssh` (server) | Transfer file to server |

Optional: `confirm: true` (ask before running), `wait: N` (pause N seconds after)

## Vault

Encrypted credential store using AES-128 + PBKDF2:

```bash
# Init vault (set master password)
opsterm vault init

# Store credentials
opsterm vault set db_password "supersecret"
opsterm vault set gh_token "ghp_..."

# Retrieve
opsterm vault get db_password

# List & manage
opsterm vault list
opsterm vault rm db_password
opsterm vault lock
```

> 💡 Set `OPSTERM_VAULT_PASSWORD` env var to avoid re-entering password.

## Environment Variables

| Variable | Overrides | Default |
|----------|-----------|---------|
| `OPSTERM_API_KEY` | `ai.api_key` | — |
| `OPSTERM_DIR` | Config dir | `~/.opsterm/` |
| `OPSTERM_VAULT_PASSWORD` | Vault master password | — |

```bash
# Override config directory
export OPSTERM_DIR="/path/to/custom/config"

# Set API key (prevents storing in plaintext config)
export OPSTERM_API_KEY="sk-..."

# Vault auto-unlock
export OPSTERM_VAULT_PASSWORD="master-password"
```
