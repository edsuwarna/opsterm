# 🚀 OpsTerm — AI Terminal Assistant

**OpsTerm** adalah AI terminal assistant lokal yang nempel di terminal laptop lu.
Bisa SSH ke server mana pun tanpa kehilangan akses AI — karena AI-nya jalan di **terminal lokal**, bukan di server remote.

> Mirip Warp.dev tapi **bebas pake custom AI provider** (DeepSeek, OpenAI, Ollama, OpenRouter, dll)

---

## ✨ Fitur

| Fitur | Command | Description |
|-------|---------|-------------|
| 🤖 **AI Chat** | `ai how to check disk` | Tanya AI apa aja |
| 🔑 **Smart SSH** | `ai ssh vps-utama` | SSH tanpa hafal IP |
| 🔗 **Multi-hop SSH** | `ai ssh internal --via bastion` | SSH lewat jump host |
| 📁 **SCP File Transfer** | `ai scp file.txt server:/path` | Upload/download via server |
| ⚡ **Workflow** | `ai run deploy-app` | Multi-step auto (SSH/SCP/local) |
| 🔐 **Vault** | `ai vault set db_pass` | Encrypted credentials (AES-128) |
| 🔗 **Pipe Mode** | `docker ps \| ai "error?"` | Explain output command |
| 💻 **Shell Integration** | `ai explain-last` | Explain output command sebelumnya |
| ⌨️ **Tab Completion** | `source <(ai completion bash)` | Auto-complete nama server/workflow |
| 📋 **History** | `ai history` | Riwayat semua command |
| 🛠️ **Custom Provider** | `ai config set ai.model gpt-4` | Bebas pilih AI |

---

## ⚡ Installasi

### 1. Clone & Setup

```bash
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm
./setup.sh
```

### 2. Set API Key

```bash
# Export key (recommended — ga ke-track git)
export OPSTERM_API_KEY='sk-deepseek-...'

# Atau langsung di config
ai config set ai.api_key "sk-..."
```

### 3. Tambah Server Pertama

```bash
ai servers add
```

Atau edit langsung file: `~/.ai-workflows/servers.yaml`

### 4. Set Tab Completion (opsional)

```bash
# Bash
echo 'source <(ai completion bash)' >> ~/.bashrc

# Zsh
echo 'source <(ai completion zsh)' >> ~/.zshrc
```

### 5. Coba!

```bash
ai ssh vps-utama          # SSH tanpa hafal IP
ai "how to check disk"    # Tanya AI
ai run cek-server         # Workflow cek server
docker ps | ai explain    # Pipe output ke AI
```

---

## 📖 Usage

### 🤖 AI Mode (Default)
```bash
# Tanya command
ai cari file log lebih dari 1GB
# → $ find /var/log -type f -size +1G

# Minta explain
ai explain what is kubernetes

# Generate command
ai buat docker compose untuk nginx + postgres
```

### 🔑 SSH — Multi-hop Support
```bash
ai ssh vps-utama                        # Direct SSH
ai ssh internal-server --via bastion    # SSH via jump host
ai ssh vps                              # Fuzzy match
```

Proxy jump host bisa di-set permanent di config server:
```yaml
servers:
  internal-server:
    host: "10.0.0.5"
    user: "ubuntu"
    key: "~/.ssh/id_ed25519"
    proxy: "bastion"        # Lewat server "bastion" dulu
```

### 📁 SCP File Transfer
```bash
# Upload file ke server
ai scp ./config.yaml vps-utama:/home/ubuntu/

# Download file dari server
ai scp vps-utama:logs/app.log .

# Lewat jump host
ai scp file.txt internal-server:/tmp/ --via bastion
```

### ⚡ Workflow dengan SCP
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

# Simpan credential
ai vault set db_password "supersecret"
ai vault set api_key "sk-..."

# Ambil credential
ai vault get db_password    # Output: supersecret

# List keys
ai vault list

# Hapus key
ai vault rm db_password

# Lock vault
ai vault lock
```

Bisa pake env var biar ga perlu input password tiap kali:
```bash
export OPSTERM_VAULT_PASSWORD='master-password'
```

### 🔗 Pipe Mode
```bash
kubectl get pods | ai "ada yang error?"
docker logs webapp --tail 50 | ai "analisa error ini"
free -h | ai "apakah memory cukup?"
netstat -tlnp | ai "port apa aja yang terbuka?"
```

### 💻 Shell Integration (Zsh Plugin)
```bash
# Load plugin di .zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh

# Fitur:
ai last               # Lihat output command terakhir
ai explain-last       # Explain output pake AI
```

### ⌨️ Tab Completion
```bash
ai [Tab]        # List subcommands
ai ssh [Tab]    # List server names
ai run [Tab]    # List workflow names
```

### 🛠️ Manajemen Server
```bash
ai servers list           # Lihat semua server (dengan kolom PROXY)
ai servers add            # Tambah server baru
ai servers edit vps       # Edit server
ai servers rm vps         # Hapus server
```

### ⚙️ Konfigurasi
```bash
ai config list            # Lihat semua config
ai config set ai.model deepseek-chat
ai config set ai.api_url https://api.deepseek.com/v1/chat/completions
ai config set shell.confirm_before_exec true
```

---

## 🔧 Konfigurasi File

Config disimpan di `~/.ai-workflows/`:

```
~/.ai-workflows/
├── config.yaml       # AI provider & shell settings
├── servers.yaml      # Daftar server (+ proxy jump)
├── workflows.yaml    # Daftar workflow (SSH/SCP/local)
├── vault.json        # Encrypted credentials (AES-128)
├── history.db        # Riwayat (SQLite, auto)
├── last_output.txt   # Output command terakhir
└── last_command.txt  # Command terakhir
```

Env vars:
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
      - command: "echo '✅ Deploy selesai!'"
        desc: "Notifikasi"
```

### cek-server — Quick health check
```yaml
  cek-server:
    desc: "Cek status server"
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
    desc: "Deploy ke internal server lewat bastion"
    steps:
      - ssh: internal-server
        command: "cd /opt/app && git pull && systemctl restart app"
        desc: "Restart app"
```

---

## 🗺️ Roadmap

- [x] AI chat dengan custom provider
- [x] Smart SSH connector
- [x] Saved workflows (SSH/local/SCP)
- [x] Pipe mode
- [x] History & riwayat
- [x] Tab completion (bash + zsh)
- [x] Shell integration (zsh plugin)
- [x] Multi-hop SSH (jump host)
- [x] SCP/file transfer via workflow
- [x] Vault encrypted credentials (AES-128 + PBKDF2)
- [ ] Tmux/screen session manager
- [ ] Docker exec shortcut (`ai exec <container>`)
- [ ] SSH config parser (import from ~/.ssh/config)

---

## 📝 License

MIT
