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
| 🔑 **Smart SSH** | `opsterm ssh vps-utama` | SSH without remembering IPs |
| 🔗 **Multi-hop SSH** | `opsterm ssh internal --via bastion` | SSH through jump host |
| 📁 **SCP File Transfer** | `opsterm scp file.txt server:/path` | Upload/download via server |
| ⚡ **Workflow** | `opsterm run deploy-app` | Multi-step automation (SSH/SCP/local) |
| 🔐 **Vault** | `opsterm vault set db_pass` | Encrypted credentials (AES-128) |
| 🔗 **Pipe Mode** | `docker ps \| opsterm "any errors?"` | Explain command output with AI |
| 🗜️ **RTK AI** | `auto` | Compress command output 60-95% before AI (saves tokens) |
| 💻 **Shell Integration** | `opsterm explain-last` | Explain previous command output |
| ⌨️ **Tab Completion** | `source <(opsterm completion bash)` | Auto-complete servers/workflows |
| 📋 **History** | `opsterm history` | Command history |
| 🔄 **Self-Update** | `opsterm update` | Check & install latest version |
| 🛠️ **Custom Provider** | `opsterm provider add <name> --api-key KEY` | Choose any AI provider |

---

## ⚡ Installation

### 🐧 Linux / 🍎 macOS

```bash
# 1. Install (single file, zero deps)
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm

# 2. Init config
opsterm init

# 3. Add your AI provider
opsterm provider add default --api-key 'sk-...' --model gpt-4o

# 4. Tab completion (bash)
echo 'source <(opsterm completion bash)' >> ~/.bashrc
source ~/.bashrc

# 5. Try it!
opsterm --help
```

> 💡 Make sure `~/.local/bin` is in your `PATH`. If using Zsh, add `source ~/opsterm/zsh/opsterm.plugin.zsh` to `~/.zshrc` for `opsterm last` and `opsterm explain-last`.

> **macOS**: Python 3 ships with macOS Ventura+ or `brew install python@3`

### 🔧 Post-Install

```bash
# Add your AI provider (one-time)
opsterm provider add default --api-key 'sk-...' --model gpt-4o

# List providers
opsterm provider list

# Switch provider later
opsterm provider default openai
```

### 🗑️ Uninstall

```bash
# Remove symlink + repo
rm ~/.local/bin/opsterm
rm -rf ~/opsterm

# Remove config (⚠️ deletes servers, workflows, vault, history)
rm -rf ~/.opsterm

# Remove shell integration lines from ~/.bashrc or ~/.zshrc
# then: source ~/.bashrc
```

### 🔄 Updating

OpsTerm has a **built-in self-update** mechanism:

```bash
# Check & install update
opsterm update
```

OpsTerm auto-checks for updates once per day and notifies you when running commands:

```
╭─ ⚡ OpsTerm Update ──────────────────────────────────────
│  Version v0.1.0 → v0.1.1 available!
│  Run: opsterm update
╰──────────────────────────────────────────────────────────
```

You can also check your current version anytime:

```bash
opsterm --version
```

> **Note:** To install a specific version, use a version tag in the download URL:
> ```bash
> curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/v0.1.1/bin/opsterm -o ~/.local/bin/opsterm
>```

---

## 📖 Usage

### 🤖 AI Mode (Default)
```bash
# Ask for a command
opsterm find log files larger than 1GB
# → $ find /var/log -type f -size +1G

# Ask for an explanation
opsterm explain what is kubernetes

# Generate a command
opsterm create docker compose for nginx + postgres
```

### 🔑 SSH — Multi-hop Support
```bash
opsterm ssh vps-utama                        # Direct SSH
opsterm ssh internal-server --via bastion    # SSH via jump host
opsterm ssh vps                              # Fuzzy match — just "vps" is enough
```

You can set a permanent jump host in the server config:
```yaml
servers:
  internal-server:
    host: "10.0.0.5"
    user: "ubuntu"
    key: "~/.ssh/id_ed25519"
    proxy: "bastion"        # Route through "bastion" server
```

### 📁 SCP File Transfer
```bash
# Upload file to server
opsterm scp ./config.yaml vps-utama:/home/ubuntu/

# Download file from server
opsterm scp vps-utama:logs/app.log .

# Through jump host
opsterm scp file.txt internal-server:/tmp/ --via bastion
```

### ⚡ Workflow with SCP
```yaml
workflows:
  deploy-full:
    desc: "Upload config + deploy"
    steps:
      - scp: "deploy/config.yaml"
        to: "/opt/app/config.yaml"
        ssh: vps-utama
        desc: "Upload config"
      - ssh: vps-utama
        command: "cd /opt/app && docker compose restart"
        desc: "Restart container"
```

### 🔐 Vault — Encrypted Credentials
```bash
# Init vault (set master password)
opsterm vault init

# Store credentials
opsterm vault set db_password "supersecret"
opsterm vault set api_key "sk-..."

# Retrieve credentials
opsterm vault get db_password    # Output: supersecret

# List keys
opsterm vault list

# Delete key
opsterm vault rm db_password

# Lock vault
opsterm vault lock
```

Use env var to avoid re-entering password:
```bash
export OPSTERM_VAULT_PASSWORD='master-password'
```

### 🔗 Pipe Mode
```bash
kubectl get pods | opsterm "any errors?"
docker logs webapp --tail 50 | opsterm "analyze these errors"
free -h | opsterm "is memory sufficient?"
netstat -tlnp | opsterm "what ports are open?"
```

### 🗜️ RTK AI — Token Compression

Auto-compress command output by **60-95%** before sending to AI — saves tokens, speeds up responses, lowers cost.

```
# Before RTK: pytest output = 597 chars → AI
# After RTK:  pytest output =   18 chars → AI (-96% 🚀)
```

| Feature | Detail |
|---------|--------|
| 🔌 **Auto-detect** | RTK identifies output type (git diff, pytest, docker, logs, etc.) |
| 📐 **Smart threshold** | Skips compression for output <200 chars (overhead not worth it) |
| 🔄 **Graceful fallback** | No RTK installed? Runs normally. No errors. |
| ⚙️ **Config** | `opsterm config set rtk.enabled false` to disable |
| 🟢 **Status** | Shows `🟢 RTK x.x.x` in `opsterm provider list` |

**Works with:** Pipe mode, `opsterm explain-last`, auto-exec mode.

> 💡 RTK is optional — install with: `curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh`

### 💻 Shell Integration (Zsh Plugin)
```bash
# Load plugin in .zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh

# Features:
opsterm last               # View last command output
opsterm explain-last       # Explain last output using AI
```

### ⌨️ Tab Completion
```bash
opsterm [Tab]        # List subcommands
opsterm ssh [Tab]    # List server names
opsterm run [Tab]    # List workflow names
```

### 🛠️ Server Management
```bash
opsterm servers list           # List all servers (with PROXY column)
opsterm servers add            # Add new server
opsterm servers edit vps       # Edit server
opsterm servers rm vps         # Remove server
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
├── vault.json        # Encrypted credentials (AES-128)
├── history.db        # History (SQLite, auto)
├── last_output.txt   # Last command output
└── last_command.txt  # Last command
```

> ⚡ Changed from `~/.ai-workflows` to `~/.opsterm/` — auto-migrates on first run.

Environment variables:
```bash
export OPSTERM_DIR="/path/to/custom/config"   # Override config dir
export OPSTERM_API_KEY="sk-..."                # AI API key
export OPSTERM_VAULT_PASSWORD="..."            # Vault master password
```

---

## 🧪 Example Workflows

### deploy-full — Full deployment with file transfer
```yaml
workflows:
  deploy-full:
    desc: "Upload config + pull + restart"
    steps:
      - scp: "./docker-compose.yml"
        to: "/home/ubuntu/app/docker-compose.yml"
        ssh: vps-utama
        desc: "Upload compose file"
      - ssh: vps-utama
        command: "cd /home/ubuntu/app && docker compose pull && docker compose up -d"
        desc: "Pull images & restart"
      - command: "echo '✅ Deploy complete!'"
        desc: "Notification"
```

### cek-server — Quick health check
```yaml
  cek-server:
    desc: "Server health check"
    steps:
      - ssh: vps-utama
        command: |
          echo "=== UPTIME ===" && uptime
          echo "=== DISK ===" && df -h /
          echo "=== MEMORY ===" && free -h
          echo "=== DOCKER ===" && docker ps
        desc: "System check"
```

### multi-hop-deploy — Deploy via bastion
```yaml
  internal-deploy:
    desc: "Deploy to internal server via bastion"
    steps:
      - ssh: internal-server
        command: "cd /opt/app && git pull && systemctl restart app"
        desc: "Restart app"
```

---

## 🗺️ Roadmap

- [x] AI chat with custom provider
- [x] Smart SSH connector
- [x] Saved workflows (SSH/local/SCP)
- [x] Pipe mode (stdin + AI prompt)
- [x] Command history (SQLite)
- [x] Tab completion (bash + zsh)
- [x] Shell integration (zsh plugin)
- [x] Multi-hop SSH (jump host)
- [x] SCP/file transfer in workflows
- [x] Vault encrypted credentials (AES-128 + PBKDF2)
- [x] Shell operators (`&&`, `|`, `>`) in local commands
- [x] Auto-migrate config `~/.ai-workflows` → `~/.opsterm/`
- [x] EOFError-safe auto-exec prompt
- [x] RTK AI — token compression (auto-detect, 60-95% savings)
- [ ] Tmux/screen session manager
- [ ] Docker exec shortcut (`opsterm exec <container>`)
- [ ] SSH config parser (import from ~/.ssh/config)
- [ ] Web dashboard (see workflows and servers in browser)

---

> Inspired by [Warp.dev](https://warp.dev) — AI in your terminal, your way.

## 📝 License

MIT

---

## 📚 Full Documentation

For detailed explanations of architecture, tech stack, and design decisions:

👉 [docs/en/](docs/en/README.md) — 📐 Architecture | 🔧 Tech Stack | 🤔 Design Decisions | 🎯 Features | 📊 Diagram

🖼️ **Architecture Diagram:** [docs/ops-term-architecture.png](docs/ops-term-architecture.png)
