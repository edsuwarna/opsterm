# 🎯 OpsTerm Features — Complete

This document explains **all features** available in OpsTerm, complete with usage examples and explanations.

---

## 📋 Feature Overview

| # | Feature | CLI Command | Category |
|---|---------|-------------|----------|
| 1 | 🤖 **AI Chat** | `ai <prompt>` | Core |
| 2 | 🔑 **Smart SSH** | `ai ssh <server>` | Core |
| 3 | 🔗 **Multi-hop SSH** | `ai ssh <srv> --via <proxy>` | Core |
| 4 | 📁 **SCP File Transfer** | `ai scp <src> <dst>` | Core |
| 5 | ⚡ **Workflow** | `ai run <name>` | Core |
| 6 | 🔐 **Vault** | `ai vault` | Core |
| 7 | 🔗 **Pipe Mode** | `cmd \| ai <prompt>` | Core |
| 8 | 💻 **Shell Integration** | `ai explain-last` | Shell |
| 9 | ⌨️ **Tab Completion** | `ai completion bash\|zsh` | Utility |
| 10 | 🛠️ **Server Manager** | `ai servers` | Management |
| 11 | 📋 **Workflow Manager** | `ai workflows` | Management |
| 12 | ⚙️ **Config Manager** | `ai config` | Management |
| 13 | 📖 **History** | `ai history` | Management |
| 14 | 🚀 **Init** | `ai init` | Setup |

---

## 1️⃣ 🤖 AI Chat

Ask anything to AI directly from your terminal.

```bash
# Ask for a shell command
ai find log files larger than 1GB
# Output: $ find /var/log -type f -size +1G

# Ask for an explanation
ai explain what is a reverse proxy

# Generate a docker compose
ai create docker compose for nginx + postgres

# General question
ai how to check disk usage in linux
```

**How it works:**
1. Load config (API key, model, URL from config.yaml)
2. Build prompt + system message
3. HTTP POST to AI provider (OpenAI-compatible API)
4. Parse response JSON
5. Print to terminal
6. Save to history (SQLite)
7. Detect `$` prefix → offer auto-exec

**Provider support:** DeepSeek, OpenAI, OpenRouter, Ollama, vLLM, or anything that is OpenAI-compatible.

---

## 2️⃣ 🔑 Smart SSH

SSH into servers without memorizing IP addresses.

```bash
# Direct connect
ai ssh vps-main

# Fuzzy match — partial name is enough
ai ssh vps

# List servers first
ai servers list
```

**Server configuration in `~/.ai-workflows/servers.yaml`:**
```yaml
servers:
  vps-main:
    host: "203.0.113.1"
    user: "ubuntu"
    port: 22
    key: "~/.ssh/id_ed25519"
    desc: "Main Tencent Cloud VPS"
```

**Configurable fields:**
- `host` — IP or domain
- `user` — SSH username
- `port` — SSH port (default: 22)
- `key` — path to private key
- `proxy` — jump host (see multi-hop feature)
- `desc` — description

---

## 3️⃣ 🔗 Multi-hop SSH

SSH into internal servers that are only accessible through a jump host / bastion.

```bash
# Via CLI (per-call)
ai ssh internal-server --via bastion

# Via config (permanent)
ai ssh internal-server  # automatically routes through bastion
```

**Permanent config in servers.yaml:**
```yaml
servers:
  bastion:
    host: "123.123.123.123"
    user: "ubuntu"
    key: "~/.ssh/id_ed25519"

  internal-server:
    host: "10.0.0.5"
    user: "ubuntu"
    key: "~/.ssh/internal-key"
    proxy: "bastion"           # <-- automatically routes through bastion
```

**How it works:**
- Uses SSH `-J` (ProxyJump) flag
- Chains can be long: `ssh -J jump1,jump2 server`
- Proxy servers are resolved from servers.yaml as well

---

## 4️⃣ 📁 SCP File Transfer

Upload/download files between local and remote servers using `server:path` syntax.

```bash
# Upload from local to server
ai scp ./config.yaml vps-main:/home/ubuntu/

# Download from server to local
ai scp vps-main:logs/app.log .

# Through a jump host
ai scp file.txt internal-server:/tmp/ --via bastion
```

**How it works:**
- Parse `server:path` → resolve to `user@host:path`
- Same as SSH: supports proxy jump, key file, custom port
- Uses the system `scp` command via subprocess

---

## 5️⃣ ⚡ Workflow

Multi-step automation that runs several commands sequentially.

```bash
# Run a workflow
ai run deploy-app

# List workflows
ai workflows list
```

**Example workflow:**
```yaml
workflows:
  deploy-full:
    desc: "Full deployment with file transfer"
    steps:
      - scp: "./docker-compose.yml"
        to: "/home/ubuntu/app/docker-compose.yml"
        ssh: vps-main
        desc: "Upload compose file"
      - ssh: vps-main
        command: "cd /home/ubuntu/app && docker compose pull && docker compose up -d"
        desc: "Pull images & restart"
      - command: "echo '✅ Deploy complete!'"
        desc: "Notification"
```

**Step types:**
| Type | Format | Function |
|------|--------|----------|
| `ssh` | `ssh: <server>` + `command:` | Run command on remote server |
| `scp` | `scp: <src>` + `to: <dst>` + `ssh: <server>` | Transfer file to server |
| `command` | `command:` | Run local command |
| `confirm` | `confirm: true` | Request user confirmation before proceeding |
| `wait` | `wait: <seconds>` | Wait for a specified number of seconds |

---

## 6️⃣ 🔐 Vault — Encrypted Credentials

Store credentials (API keys, passwords, tokens) in encrypted form.

```bash
# Init vault (set master password)
ai vault init

# Store a credential
ai vault set db_password "supersecret"
ai vault set github_token "ghp_..."

# Retrieve a credential
ai vault get db_password    # Output: supersecret

# List keys
ai vault list

# Delete a key
ai vault rm db_password

# Lock vault (clear password from memory)
ai vault lock
```

**Technical details:**
- **Encryption:** AES-128-CBC via `cryptography.fernet.Fernet`
- **Key derivation:** PBKDF2-HMAC-SHA256, 600,000 iterations
- **Master password:** from `OPSTERM_VAULT_PASSWORD` env or prompt
- **Fallback:** if `cryptography` is not installed → HMAC + XOR (less secure)
- **Storage:** encrypted JSON at `~/.ai-workflows/vault.json`

---

## 7️⃣ 🔗 Pipe Mode

Send command output to AI for analysis.

```bash
# Explain output
kubectl get pods | ai "are there any errors?"
docker logs webapp --tail 100 | ai "analyze these errors"
free -h | ai "is there enough memory?"
netstat -tlnp | ai "what ports are open?"

# Pipe without a specific prompt
df -h | ai
# AI auto-prompt: "Explain this output"
```

**How it works:**
1. Detect stdin (`sys.stdin.isatty() == False`)
2. Read stdin → store as `stdin_data`
3. Build prompt: "Output from command:\n```\n{stdin_data}\n```\nQuestion: {prompt}"
4. Send to AI → print response

---

## 8️⃣ 💻 Shell Integration (Zsh Plugin)

Integration with Zsh shell for viewing and explaining the last command's output.

```bash
# Load in .zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh

# View last command output
ai last

# Explain last command output using AI
ai explain-last
```

**Features:**
- **`ai-last`** — alias for `ai last`
- **`ai-explain`** — alias for `ai explain-last`
- **`ai-ti`** — AI + Terminal Integration: ask AI, extract command, auto-execute

**How it works:**
- Zsh `preexec` hook → saves command before it runs
- Last command output is stored in `~/.ai-workflows/last_output.txt`
- `ai explain-last` → reads file → sends to AI

---

## 9️⃣ ⌨️ Tab Completion

Auto-complete for bash and zsh — no need to memorize server/workflow names.

```bash
# Bash
source <(ai completion bash)

# Zsh
source <(ai completion zsh)

# Or permanently:
echo 'source <(ai completion bash)' >> ~/.bashrc
echo 'source <(ai completion zsh)' >> ~/.zshrc
```

**Completion contexts:**
| Context | Completion |
|---------|------------|
| `ai [Tab]` | All subcommands |
| `ai ssh [Tab]` | Server names |
| `ai run [Tab]` | Workflow names |
| `ai scp [Tab]` | `server:` prefix |
| `ai servers [Tab]` | `add`, `edit`, `rm`, `list` |
| `ai vault [Tab]` | `init`, `set`, `get`, `list`, `rm`, `lock` |
| `ai --via [Tab]` | Proxy server names |

---

## 🔟 🛠️ Server Manager

CRUD for servers — save, edit, and delete server configurations.

```bash
# List all servers (with PROXY column)
ai servers list
# Output:
# NAME       HOST            USER    PORT  PROXY  DESCRIPTION
# vps-main   203.0.113.1  ubuntu  22    —      Tencent Cloud VPS

# Add a new server (interactive)
ai servers add

# Edit a server
ai servers edit vps-main

# Delete a server
ai servers rm vps-main
```

Data stored in `~/.ai-workflows/servers.yaml`.

---

## 1️⃣1️⃣ 📋 Workflow Manager

CRUD for workflows — save, edit, and delete workflows.

```bash
# List all workflows
ai workflows list

# Add a new workflow (interactive)
ai workflows add

# Edit a workflow (opens editor)
ai workflows edit deploy-app

# Delete a workflow
ai workflows rm deploy-app
```

Data stored in `~/.ai-workflows/workflows.yaml`.

---

## 1️⃣2️⃣ ⚙️ Config Manager

View and set OpsTerm configuration.

```bash
# View all config
ai config list

# Set a value
ai config set ai.model deepseek-chat
ai config set ai.api_url https://api.deepseek.com/v1/chat/completions
ai config set ai.temperature 0.3
ai config set shell.confirm_before_exec true

# Get a specific value
ai config get ai.model
```

Data stored in `~/.ai-workflows/config.yaml`.

---

## 1️⃣3️⃣ 📖 History

History of all commands that have been run.

```bash
# View last 20 entries
ai history

# View last 50 entries
ai history 50
```

**Output:**
```
  [1] 🤖 2026-05-24 15:30 [ai] how to check disk usage
  [2] 🔑 2026-05-24 15:35 [ssh] vps-main
  [3] ⚡ 2026-05-24 15:40 [workflow] deploy-app
  [4] 🔗 2026-05-24 15:45 [pipe] docker ps | ai error
```

**Mode icons:**
| Icon | Mode |
|------|------|
| 🤖 | AI chat |
| 🔑 | SSH |
| ⚡ | Workflow |
| 🔗 | Pipe mode |
| 💻 | Shell command |
| 📁 | SCP transfer |
| 🔐 | Vault |

Data stored in SQLite: `~/.ai-workflows/history.db`.

---

## 1️⃣4️⃣ 🚀 Init

First-time setup — creates default configuration files.

```bash
ai init
```

**Created files:**
- `~/.ai-workflows/config.yaml` — AI provider template
- `~/.ai-workflows/servers.yaml` — example server config
- `~/.ai-workflows/workflows.yaml` — example workflow config

---

## 🎯 Use Case Matrix

| What You Want To Do | Command |
|---------------------|---------|
| **SSH into a server** | `ai ssh vps-main` |
| **SSH through a bastion** | `ai ssh internal --via bastion` |
| **Upload a file** | `ai scp file.txt server:/path/` |
| **Download a file** | `ai scp server:log.txt .` |
| **Deploy an app** | `ai run deploy-app` |
| **Check server health** | `ai run check-server` |
| **Ask for a command** | `ai how to check disk` |
| **Explain an error** | `docker logs -n50 \| ai "error?"` |
| **Explain last command** | `ai explain-last` |
| **Store a password** | `ai vault set db_pass` |
| **Retrieve a password** | `ai vault get db_pass` |
| **Auto-complete** | `ai [Tab]` |
| **View history** | `ai history` |
| **Setup from scratch** | `ai init` |

---

## 🔜 Future Roadmap

- [ ] **Tmux/screen session manager** — manage multi-sessions from OpsTerm
- [ ] **Docker exec shortcut** — `ai exec <container>` to jump directly into a container
- [ ] **SSH config parser** — import from `~/.ssh/config`
- [ ] **Fish shell support** — completion & plugin for Fish
- [ ] **Multi-hop chain** — `ai ssh server --via jump1,jump2`
- [ ] **Vault auto-unlock** — unlock vault using fingerprint/keychain
