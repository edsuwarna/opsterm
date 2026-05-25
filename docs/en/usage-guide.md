# 🚀 Usage Guide

How to use OpsTerm day-to-day, from basic AI queries to advanced workflows.

## AI Chat

The core feature — ask questions, get answers in your terminal:

```bash
# Simple question
opsterm "how to find large files"

# With context from pipe
docker logs my-app | opsterm "what do these errors mean?"

# System info query
opsterm "check disk space on this machine"
```

## SSH Mode

Connect to servers without losing AI access:

```bash
# Direct SSH
opsterm ssh my-server

# With proxy/bastion host
opsterm ssh internal-server --via bastion

# Multi-hop
opsterm ssh app-3 --via bastion --via jump-box
```

Once connected, you can still use `opsterm "query"` — the AI runs on your local machine, not the server.

## Pipe Mode

Explain command output or ask questions about it:

```bash
# Analyze logs
journalctl -u nginx | opsterm "find error patterns"

# Check configs
cat /etc/nginx/nginx.conf | opsterm "any security issues?"

# Debug builds
make 2>&1 | opsterm "what went wrong?"
```

## SCP File Transfer

Transfer files between servers:

```bash
# Upload
opsterm scp ./config.yaml my-server:/etc/app/

# Download
opsterm scp my-server:/var/log/app.log ./logs/

# Between servers
opsterm scp server-a:/data/dump.sql server-b:/backup/
```

## Vault (Credential Management)

Store and retrieve secrets:

```bash
# Add a credential
opsterm vault add db-pass mysecret123

# List entries
opsterm vault list

# Get a credential
opsterm vault get db-pass

# Remove
opsterm vault remove db-pass
```

## Workflows

Run predefined automation:

```bash
# List workflows
opsterm workflows

# Run a workflow
opsterm run health-check

# Run with params
opsterm run deploy --env staging
```

Workflows are defined in `~/.ai-workflows/workflows.yaml`.

## Server Manager

Manage SSH connections:

```bash
# List servers
opsterm servers

# Add a server
opsterm servers add prod-1 --host 192.168.1.10 --user root

# Remove
opsterm servers remove prod-1
```

## Shell Integration

If you've enabled the Zsh plugin:

```bash
# Explain last command output
opsterm-explain-last

# Re-run last command with AI enhancement
opsterm-last

# Tab completion for servers
opsterm ssh [TAB]
```

## Tips & Tricks

- **Combine with `watch`:** `watch -n 5 "opsterm 'check load'"` for monitoring
- **Alias frequently used queries:** `alias health='opsterm "run health check"'`
- **Batch queries:** `cat servers.txt | while read srv; do opsterm ssh $srv "check disk"; done`
