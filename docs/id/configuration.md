# ⚙️ Konfigurasi

Konfigurasi OpsTerm via file YAML di `~/.ai-workflows/`.

## config.yaml — AI Provider

```yaml
provider: openai
api_key: sk-xxx
model: gpt-4o
temperature: 0.7
max_tokens: 4096
```

## servers.yaml — SSH Servers

```yaml
servers:
  web-01:
    host: 192.168.1.10
    user: root
    key: ~/.ssh/id_ed25519
  db-master:
    host: db.internal
    user: admin
    via: bastion
```

## workflows.yaml — Automation

```yaml
workflows:
  health-check:
    steps:
      - run: "uptime"
      - run: "df -h /"
      - run: "free -h"
```

## Environment Variables

```bash
export OPSTERM_PROVIDER=anthropic
export OPSTERM_MODEL=claude-sonnet-4
```

| Variable | Overrides |
|----------|-----------|
| `OPSTERM_PROVIDER` | config.yaml `provider` |
| `OPSTERM_MODEL` | config.yaml `model` |
| `OPSTERM_API_KEY` | config.yaml `api_key` |
