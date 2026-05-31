# 🚀 OpsTerm — AI Terminal Assistant

> 🌍 [README.id.md](README.id.md) — Baca versi Bahasa Indonesia

**OpsTerm** is a local AI terminal assistant that lives in your terminal.
SSH into any server without losing AI access — because the AI runs on your **local terminal**, not on the remote server.

> Inspired by [Warp.dev](https://warp.dev) — but **free to use any custom AI provider** (DeepSeek, OpenAI, Ollama, OpenRouter, etc.)

---

## ✨ Features

| Feature | Command | Description |
|---------|---------|-------------|
| 🤖 **AI Chat** | `opsterm how to check disk` | Ask AI anything |
| 💬 **Chat REPL** | `opsterm chat` | Interactive chat mode with history |
| 🔑 **Smart SSH** | `opsterm ssh vps-utama` | SSH without remembering IPs |
| 🔗 **Multi-hop SSH** | `opsterm ssh internal --via bastion` | SSH through jump host |
| 📁 **SCP File Transfer** | `opsterm scp file.txt server:/path` | Upload/download via server |
| ⚡ **Workflow** | `opsterm run deploy-app` | Multi-step automation (SSH/SCP/local) |

| 🔗 **Pipe Mode** | `docker ps \| opsterm "any errors?"` | Explain command output with AI |
| 🗜️ **RTK AI** | `auto` | Compress command output 60-95% before AI (saves tokens) |
| 💻 **Shell Integration** | `opsterm explain-last` | Explain previous command output |
| 🏓 **Server Ping** | `opsterm servers ping vps` | Check SSH connectivity & latency |
| 🔌 **Provider Test** | `opsterm provider test openai` | Test AI provider connection |
| 📡 **Provider Models** | `opsterm provider models openai` | List available models for a provider |
| ⌨️ **Tab Completion** | `source <(opsterm completion bash)` | Auto-complete servers/workflows |
| 📋 **History** | `opsterm history` | Command history |
| 🔄 **Self-Update** | `opsterm update` | Check & install latest version |
| 🛠️ **Custom Provider** | `opsterm provider add <name> --api-key KEY` | Choose any AI provider |
| 🖥️ **Web Dashboard** | `opsterm web [--port <port>] [--open]` | Browser UI to manage servers/workflows/config |
| 🏥 **Diagnostics** | `opsterm doctor` | Check config & diagnose issues |
| 📋 **Server Details** | `opsterm servers show <name>` | View server connection details |
| 🔄 **Server Rename** | `opsterm servers rename <old> <new>` | Rename a server |
| 📥 **Import SSH Config** | `opsterm servers import-ssh-config` | Import servers from ~/.ssh/config |
| ⚙️ **Custom System Prompt** | `opsterm config set ai.system_prompt <text>` | Customize AI personality |
| ✅ **Config Validate** | `opsterm config validate` | Validate all YAML config files |
| 📚 **Search History** | `opsterm search <query>` | Search chat history by keyword |
| 🔄 **Chat Resume** | `opsterm chat --continue` | Resume last chat session |
| 📦 **Config Export** | `opsterm export [<file>]` | Export config to tar.gz (keys masked) |
| 📥 **Config Import** | `opsterm import <file>` | Import config from tar.gz |
| 🗑️ **Config Reset** | `opsterm reset` | Reset config to defaults |
| 📋 **Workflow Init** | `opsterm workflows init` | Create sample workflows |
| 🌐 **Batch SSH** | `opsterm ssh --all <command>` | Run command on all servers |

> 💡 All list commands (`provider list`, `servers list`, `history`) support `--json` flag for scripting.

---

## 🚀 Quick Start

### Install

**Linux/macOS** — single curl command, no repo needed:

```bash
# Install latest release
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/LATEST -o /tmp/opsterm_latest
OPSTERM_VER=$(cat /tmp/opsterm_latest)
curl -L "https://raw.githubusercontent.com/edsuwarna/opsterm/${OPSTERM_VER}/bin/opsterm" -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
rm -f /tmp/opsterm_latest
```

Or pin to a **specific release version** (recommended for stability):

```bash
# Install v0.7.0
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/v0.7.0/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
```

Check the [Releases page](https://github.com/edsuwarna/opsterm/releases) for the latest version.

Make sure `~/.local/bin` is in your `PATH`:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Configure your AI provider (one-time)

```bash
# Add OpenAI (you can switch to any provider later)
opsterm provider add default --api-key 'sk-...' --model gpt-4o

# See all available providers
opsterm provider supported

# See what you've configured
opsterm provider list
```

### Verify

```bash
opsterm --help
```

### Updating

OpsTerm has a built-in self-updater:

```bash
# Check for updates & install
opsterm update
```

This will:
1. Check the latest version from GitHub
2. Download and compile-verify the new script
3. Backup your current version as `opsterm.bak`
4. Replace with the new version

> 💡 OpsTerm also checks for updates automatically once per 24 hours on startup — you'll see a notification if a new version is available.

---

## 💡 What Can I Do With It?

### 🎯 Just ask AI

```bash
# Ask for a command
opsterm how to find large files

# Explain system output
opsterm explain-last

# In pipe mode
docker ps | opsterm "any errors?"
```

### 🌐 SSH — no more IP juggling

Save your servers once, then SSH by name:

```yaml
# ~/.opsterm/servers.yaml
servers:
  - name: vps-utama
    host: 203.0.113.10
    user: root
    proxy:                    # optional jump host
      host: 198.51.100.5
      user: ubuntu
  - name: db-server
    host: 10.0.0.5
    user: admin
```

```bash
opsterm ssh vps-utama             # Direct SSH
opsterm ssh internal --via bastion # Via proxy/jump host
opsterm scp file.txt server:/path  # File transfer
opsterm servers ping vps-utama    # Check connectivity
```

### ⚡ Workflows — automate multi-step tasks

Define reusable workflows in YAML:

```yaml
# ~/.opsterm/workflows.yaml
workflows:
  - name: deploy-app
    steps:
      - command: "cd /opt/app && git pull && docker compose restart"
      - ssh: vps-utama
        command: "cd /opt/app && docker compose up -d --build"
  - name: check-all
    steps:
      - local: "echo '=== Checking all servers ==='"
      - ssh: vps-utama
        command: "df -h && free -h && uptime"
      - ssh: db-server
        command: "pg_isready && systemctl status postgresql --no-pager"
```

```bash
opsterm run deploy-app
opsterm run check-all
```
## 🧠 AI Features

### Custom AI Providers

OpsTerm works with **any OpenAI-compatible API** — bring your own provider:

```bash
opsterm provider supported                 # List all supported providers
opsterm provider add openai --api-key sk-... --model gpt-4o
opsterm provider add deepseek --api-key sk-... --model deepseek-chat \
  --api-url https://api.deepseek.com/v1/chat/completions
opsterm provider add ollama --api-url http://localhost:11434/v1  # local (no key needed)

opsterm provider default deepseek           # Switch default
opsterm provider test openai                # Test connection
opsterm provider models openai              # List available models
opsterm provider list                       # See all configured
```

Auto-compress command output by **60-95%** before sending to AI — saves tokens, speeds up responses, lowers cost.

### Token Compression via RTK

```
# Before RTK: pytest output = 597 chars → AI
# After RTK:  pytest output =   18 chars → AI (-96% 🚀)
```

| Feature | Benefit |
|---------|---------|
| 🔌 **Auto-detect** | RTK identifies output type (git diff, pytest, docker, logs, etc.) |
| 🎯 **Smart compression** | Keeps relevant lines, removes noise |
| ⚡ **Fast** | Sub-second compression, even for large outputs |
| 🟢 **Status** | Shows `🟢 RTK x.x.x` in `opsterm provider list` |

### Session Context

OpsTerm maintains **conversation context** throughout a session (30-min window). Every prompt includes previous exchanges so you can ask follow-ups:

```bash
# Ask a follow-up — OpsTerm remembers what you just did!
opsterm how to check disk usage
# → Responds with df -h / du -sh

opsterm what about inodes?
# → Understands you're still talking about disk commands
```

### Custom System Prompt

Set a custom system prompt to tailor the AI's behavior and personality:

```bash
# Be concise and technical
opsterm config set ai.system_prompt "You are a senior DevOps engineer. Answer in short, actionable commands."

# Speak in a specific language
opsterm config set ai.system_prompt "Answer in Indonesian. Use casual friendly tone."

# Be educational
opsterm config set ai.system_prompt "Explain concepts like I'm a beginner. Include examples."
```

> 💡 The system prompt is prepended to every AI request. Use it to set context, tone, or expertise level.

---

## 💻 Usage

```bash
opsterm <command> [options]

# Ask for a command
opsterm how to check disk usage

# Generate a command
opsterm generate docker compose restart postgres
```

### Smart SSH

```bash
opsterm ssh vps-utama                    # Fuzzy match server name
opsterm ssh vps                          # "vps" matches "vps-utama"
opsterm ssh internal --via bastion       # Multi-hop via ProxyJump
opsterm scp file.txt vps-utama:/home/ubuntu/
opsterm scp vps-utama:/var/log/syslog .
opsterm scp file.txt vps-utama:/tmp --via bastion
opsterm servers ping vps-utama           # Check SSH connectivity
opsterm servers show vps-utama           # Show server details
```

### Workflows

```bash
opsterm run <name>
opsterm run deploy-app
```

### Tab Completion

```bash
# Temporary (current session only)
source <(opsterm completion bash)   # or: opsterm completion zsh

# Permanent (auto-detect shell, adds to .bashrc/.zshrc)
opsterm completion install
```

After install, tab-complete server names, workflows, and subcommands:
  `opsterm ssh [Tab]` → server names
  `opsterm run [Tab]` → workflow names
  `opsterm servers [Tab]` → subcommands

### Diagnostics

Check your OpsTerm installation and configuration:

```bash
opsterm doctor
```

This checks:
- ✅ Config file exists and is valid
- ✅ API key is configured (with masked preview)
- ✅ Provider URL is reachable
- ✅ Version status (latest vs installed)
- ✅ PATH includes `~/.local/bin`

Use it when setting up OpsTerm for the first time or troubleshooting issues.

Or add to your shell config:

opsterm ssh [Tab]    # List server names
opsterm run [Tab]    # List workflow names
```

### 🛠️ Server Management
```bash
opsterm servers list           # List all servers (with PROXY column)
opsterm servers show vps       # View server details
opsterm servers add            # Add new server
opsterm servers edit vps       # Edit server
opsterm servers rm vps         # Remove server
opsterm servers ping vps       # Check SSH connectivity & latency
```

### ⚙️ Configuration
```bash
opsterm config list            # View all config
opsterm config set ai.model deepseek-chat
opsterm config set ai.api_url https://api.deepseek.com/v1/chat/completions
opsterm config set shell.confirm_before_exec true
```

---

## 🔧 Config Files

Config is stored in `~/.opsterm/`:

```
~/.opsterm/
├── config.yaml       # AI provider & shell settings
├── servers.yaml      # Server list (+ proxy jump)
├── workflows.yaml    # Workflow list (SSH/SCP/local)

├── history.db        # History (SQLite, auto)
├── last_output.txt   # Last command output
└── last_command.txt  # Last command
```

> ⚡ Changed from `~/.ai-workflows` to `~/.opsterm/` — auto-migrates on first run.

Environment variables:
```bash
export OPSTERM_DIR="/path/to/custom/config"   # Override config dir
export OPSTERM_API_KEY="sk-..."                # AI API key

```

---

## 🧪 Example Workflows

### Basic Deploy
```yaml
# ~/.opsterm/workflows.yaml
workflows:
  - name: deploy-app
    steps:
      - command: "cd /home/ubuntu/app && docker compose pull && docker compose up -d"
      - command: "echo '✅ Deploy complete!'"
```

### Multi-Server Health Check
```yaml
workflows:
  - name: health-check
    steps:
      - local: "echo '=== Health Check Report ==='"
      - ssh: web-server
        command: |
          echo "--- Uptime ---"
          uptime
          echo "--- Disk ---"
          df -h /
      - ssh: db-server
        command: "pg_isready && echo 'PostgreSQL OK'"
      - local: "echo '✅ Done!'"
```

### Deploy from CI
```yaml
workflows:
  - name: deploy-ci
    steps:
      - command: "cd /opt/app && git pull && systemctl restart app"
```

---

## 📋 Roadmap

- [x] AI chat with custom provider
- [x] Smart SSH (fuzzy name match, ProxyJump)
- [x] SCP file transfer (local ↔ server ↔ server)
- [x] Multi-step workflows (SSH/SCP/local)

- [x] Command history (SQLite)
- [x] Pipe mode (send command output to AI)
- [x] SSH via jump host (--via)
- [x] Tab completion (bash/zsh)

- [x] Shell operators (`&&`, `|`, `>`) in local commands
- [x] Multi-hop SCP (file transfer through bastion)
- [x] RTK token compression
- [x] Provider management (add, list, test, models)
- [x] Server ping (connectivity check)
- [x] Chat REPL (interactive mode)
- [x] JSON output (`--json` flag)
- [x] Config validation
- [x] Import SSH config (~/.ssh/config)
- [x] Web dashboard (browser UI for servers/workflows/config)
- [ ] Multi-language AI responses
- [ ] Plugin system

---

<p align="center">
  <sub>Built with ❤️ for developers who manage too many servers.</sub>
  <br>
  <sub>Inspired by <a href="https://warp.dev">Warp.dev</a> — AI in your terminal, your own provider.</sub>
</p>
