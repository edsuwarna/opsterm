# 📖 Usage Guide

## AI Assistant

Ask anything:

```bash
opsterm "How to check disk space"
opsterm "explain this: docker ps | grep exited"
```

Pipe mode — pipe command output to AI:

```bash
docker logs -n50 | opsterm "any errors?"
df -h | opsterm "is disk usage okay?"
```



Launch a browser-based UI to manage everything:

```bash
# Start dashboard on default port (8765)
opsterm web

# Custom port
opsterm web --port 8080

# Open browser automatically
opsterm web --open
```

The dashboard provides 4 tabs:
- **🖥️ Servers** — Add, edit, delete, ping servers
- **⚡ Workflows** — Add, edit, run, delete workflows
- **🤖 Providers** — Add, edit, test, delete AI providers
- **⚙️ Config** — View all configuration (read-only)

## Config Management

```bash
# View all config
opsterm config list

# Get a specific key
opsterm config get ai

# Set a value
opsterm config set ai.temperature 0.3

# Validate config files
opsterm config validate
```

## Export/Import Config

Backup or transfer your configuration (API keys are masked in export):

```bash
# Export to default file
opsterm export

# Export to specific path
opsterm export ~/backups/opsterm-config.tar.gz

# Import from file
opsterm import ~/backups/opsterm-config.tar.gz

# Reset config to defaults
opsterm reset
```

> **Note:** Exported API keys are masked. Update them after import with `opsterm provider add <name> --api-key '...'`

## Workflows

Run predefined automation:

```bash
# List workflows
opsterm workflows list

# Run a workflow
opsterm run health-check

# Init sample workflows
opsterm workflows init
```

## Servers

```bash
# List servers
opsterm servers list

# Add a server (interactive)
opsterm servers add

# Add via flags
opsterm servers add my-server --host 1.2.3.4 --user root

# Edit a server
opsterm servers edit my-server

# Ping a server
opsterm servers ping my-server

# Show details
opsterm servers show my-server

# Rename
opsterm servers rename my-server my-vps

# Delete
opsterm servers rm my-server

# Import from SSH config
opsterm servers import-ssh-config
```

> All `list` commands support `--json` for scripting.

## SSH

```bash
# SSH with fuzzy name matching
opsterm ssh my-server

# Multi-hop via proxy
opsterm ssh internal --via bastion

# Run command on all servers
opsterm ssh --all uptime
```

## SCP

```bash
# Upload
opsterm scp ./config.yaml my-server:/etc/app/

# Download
opsterm scp my-server:/var/log/app.log ./logs/

# Between servers
opsterm scp server-a:/data/dump.sql server-b:/backup/

# Through proxy
opsterm scp ./file.txt internal-server:/tmp/ --via bastion
```

## Provider Management

```bash
# Add a provider (interactive — pick type, enter key, choose model)
opsterm provider add

# One-liner
opsterm provider add openai --api-key sk-... --model gpt-4o

# List providers
opsterm provider list

# Test a provider
opsterm provider test openai

# Set default
opsterm provider default openai

# See supported provider types
opsterm provider supported

# Delete
opsterm provider rm openai
```

## Tab Completion

```bash
# Bash
source <(opsterm completion bash)

# Zsh
source <(opsterm completion zsh)
```

## Maintenance

```bash
# Check for updates
opsterm update

# Diagnose installation
opsterm doctor

# View history
opsterm history

# Search history
opsterm search "docker"

# Resume last chat session
opsterm chat --continue

# View last command output
opsterm last

# Explain last command output
opsterm explain-last
```
