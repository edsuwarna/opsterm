# ⚙️ Configuration

OpsTerm is configured through YAML files in `~/.ai-workflows/`.

## Config Directory

All config files live in `~/.ai-workflows/`:

```
~/.ai-workflows/
├── config.yaml       ← AI provider, model, defaults
├── servers.yaml      ← SSH server definitions
├── workflows.yaml    ← Workflow definitions
├── vault.json        ← Encrypted credentials
├── history.db        ← SQLite query history
└── last_*.txt        ← Last command output cache
```

## config.yaml — AI Provider

```yaml
# Required
provider: openai         # openai | anthropic | deepseek | openrouter | custom
api_key: sk-xxx          # Your API key
model: gpt-4o            # Model name

# Optional
temperature: 0.7         # Default: 0.7
max_tokens: 4096         # Max response length
timeout: 60              # API timeout in seconds

# Custom provider endpoint
# provider: custom
# api_base: https://your-endpoint.com/v1
# model: your-model
```

## servers.yaml — SSH Servers

```yaml
servers:
  web-01:
    host: 192.168.1.10
    user: root
    port: 22
    key: ~/.ssh/id_ed25519

  db-master:
    host: db.internal
    user: admin
    port: 2222
    via: bastion       # Proxy/bastion host

  bastion:
    host: bastion.example.com
    user: jumpuser
    key: ~/.ssh/bastion-key
```

## workflows.yaml — Automation

```yaml
workflows:
  health-check:
    steps:
      - run: "uptime"
      - run: "df -h /"
      - run: "free -h"
      - run: "docker ps --format 'table {{.Names}}\t{{.Status}}'"
    description: "Quick system health overview"

  deploy:
    params:
      - name: env
        type: string
        default: staging
    steps:
      - run: "cd /opt/{{env}} && git pull"
      - run: "docker compose up -d --build"
      - run: "docker compose ps"
    description: "Deploy to environment"
```

## Vault

Credentials are stored encrypted in `vault.json`. The encryption key is derived from a master password you set on first use.

```bash
# Set master password (first time)
opsterm vault init

# Add credential
opsterm vault add db-password mysecret123

# Use in workflow
# workflows.yaml can reference vault entries
```

## Environment Variables

Override config settings at runtime:

```bash
export OPSTERM_PROVIDER=anthropic
export OPSTERM_MODEL=claude-sonnet-4
export OPSTERM_API_KEY=sk-ant-xxx
opsterm "check server"
```

| Variable | Overrides |
|----------|-----------|
| `OPSTERM_PROVIDER` | config.yaml `provider` |
| `OPSTERM_MODEL` | config.yaml `model` |
| `OPSTERM_API_KEY` | config.yaml `api_key` |
| `OPSTERM_CONFIG_DIR` | Default `~/.ai-workflows` |
| `OPSTERM_SSH_TIMEOUT` | SSH connection timeout (s) |
