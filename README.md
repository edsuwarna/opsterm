# 🚀 OpsTerm — AI Terminal Assistant

> 🌍 [README.id.md](README.id.md) — Baca versi Bahasa Indonesia

**OpsTerm** is a local AI terminal assistant that lives in your terminal.
SSH into any server without losing AI access — because the AI runs on your **local terminal**, not on the remote server.

> Think Warp.dev but **free to use any custom AI provider** (DeepSeek, OpenAI, Ollama, OpenRouter, etc.)

---

## ✨ Features

| Feature | Command | Description |
|---------|---------|-------------|
| 🤖 **AI Chat** | `ai how to check disk` | Ask AI anything |
| 🔑 **Smart SSH** | `ai ssh vps-utama` | SSH without remembering IPs |
| 🔗 **Multi-hop SSH** | `ai ssh internal --via bastion` | SSH through jump host |
| 📁 **SCP File Transfer** | `ai scp file.txt server:/path` | Upload/download via server |
| ⚡ **Workflow** | `ai run deploy-app` | Multi-step automation (SSH/SCP/local) |
| 🔐 **Vault** | `ai vault set db_pass` | Encrypted credentials (AES-128) |
| 🔗 **Pipe Mode** | `docker ps \| ai "any errors?"` | Explain command output with AI |
| 💻 **Shell Integration** | `ai explain-last` | Explain previous command output |
| ⌨️ **Tab Completion** | `source <(ai completion bash)` | Auto-complete servers/workflows |
| 📋 **History** | `ai history` | Command history |
| 🛠️ **Custom Provider** | `ai config set ai.model gpt-4` | Choose any AI provider |

---

## ⚡ Installation

### 🐧 Linux

```bash
# 1. Clone repo
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm

# 2. Setup (creates symlink + init config)
./setup.sh

# 3. Set API key
export OPSTERM_API_KEY='sk-deepseek-...'

# 4. Tab completion (bash)
echo 'source <(ai completion bash)' >> ~/.bashrc
source ~/.bashrc

# 5. Try it
ai --help
```

### 🍎 macOS

```bash
# 1. Clone repo
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm

# 2. Setup (creates symlink + init config)
./setup.sh

# 3. Set API key
export OPSTERM_API_KEY='sk-deepseek-...'

# 4. Tab completion — macOS uses Zsh by default
echo 'source <(ai completion zsh)' >> ~/.zshrc
source ~/.zshrc

# 5. Zsh plugin (optional — for ai-last, ai-explain)
echo 'source ~/opsterm/zsh/opsterm.plugin.zsh' >> ~/.zshrc

# 6. Try it
ai --help
```

> **macOS Note**: Make sure Python 3 is available (`python3 --version`).
> macOS Ventura/Sonoma/Sequoia ships with Python 3 built-in.
> If missing: `brew install python@3`

### ⚙️ Post-Install (Linux & macOS)

```bash
# Set API key permanently in ~/.bashrc or ~/.zshrc
echo 'export OPSTERM_API_KEY="sk-..."' >> ~/.bashrc

# Add your first server
ai servers add

# Or edit the config file directly
nano ~/.ai-workflows/servers.yaml
```

---

## 📖 Usage

### 🤖 AI Mode (Default)
```bash
# Ask for a command
ai find log files larger than 1GB
# → $ find /var/log -type f -size +1G

# Ask for an explanation
ai explain what is kubernetes

# Generate a command
ai create docker compose for nginx + postgres
```

### 🔑 SSH — Multi-hop Support
```bash
ai ssh vps-utama                        # Direct SSH
ai ssh internal-server --via bastion    # SSH via jump host
ai ssh vps                              # Fuzzy match — just "vps" is enough
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
ai scp ./config.yaml vps-utama:/home/ubuntu/

# Download file from server
ai scp vps-utama:logs/app.log .

# Through jump host
ai scp file.txt internal-server:/tmp/ --via bastion
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
ai vault init

# Store credentials
ai vault set db_password "supersecret"
ai vault set api_key "sk-..."

# Retrieve credentials
ai vault get db_password    # Output: supersecret

# List keys
ai vault list

# Delete key
ai vault rm db_password

# Lock vault
ai vault lock
```

Use env var to avoid re-entering password:
```bash
export OPSTERM_VAULT_PASSWORD='master-password'
```

### 🔗 Pipe Mode
```bash
kubectl get pods | ai "any errors?"
docker logs webapp --tail 50 | ai "analyze these errors"
free -h | ai "is memory sufficient?"
netstat -tlnp | ai "what ports are open?"
```

### 💻 Shell Integration (Zsh Plugin)
```bash
# Load plugin in .zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh

# Features:
ai last               # View last command output
ai explain-last       # Explain last output using AI
```

### ⌨️ Tab Completion
```bash
ai [Tab]        # List subcommands
ai ssh [Tab]    # List server names
ai run [Tab]    # List workflow names
```

### 🛠️ Server Management
```bash
ai servers list           # List all servers (with PROXY column)
ai servers add            # Add new server
ai servers edit vps       # Edit server
ai servers rm vps         # Remove server
```

### ⚙️ Configuration
```bash
ai config list            # View all config
ai config set ai.model deepseek-chat
ai config set ai.api_url https://api.deepseek.com/v1/chat/completions
ai config set shell.confirm_before_exec true
```

---

## 🔧 Config Files

Config is stored in `~/.ai-workflows/`:

```
~/.ai-workflows/
├── config.yaml       # AI provider & shell settings
├── servers.yaml      # Server list (+ proxy jump)
├── workflows.yaml    # Workflow list (SSH/SCP/local)
├── vault.json        # Encrypted credentials (AES-128)
├── history.db        # History (SQLite, auto)
├── last_output.txt   # Last command output
└── last_command.txt  # Last command
```

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
- [x] Pipe mode
- [x] Command history
- [x] Tab completion (bash + zsh)
- [x] Shell integration (zsh plugin)
- [x] Multi-hop SSH (jump host)
- [x] SCP/file transfer in workflows
- [x] Vault encrypted credentials (AES-128 + PBKDF2)
- [ ] Tmux/screen session manager
- [ ] Docker exec shortcut (`ai exec <container>`)
- [ ] SSH config parser (import from ~/.ssh/config)

---

## 📝 License

MIT

---

## 📚 Dokumentasi Lengkap

Untuk penjelasan detail tentang arsitektur, tech stack, dan design decisions:

👉 [docs/](docs/README.md) — 📐 Arsitektur | 🔧 Tech Stack | 🤔 Design Decisions | 🎯 Fitur | 📊 Diagram

🖼️ **Architecture Diagram:** [docs/ops-term-architecture.png](docs/ops-term-architecture.png)
