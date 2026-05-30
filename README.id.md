# 🚀 OpsTerm — AI Terminal Assistant

> 🌍 [README.md](README.md) — Read in English

**OpsTerm** adalah asisten AI terminal lokal yang nempel di terminal laptop lu.
Bisa SSH ke server mana pun tanpa kehilangan akses AI — karena AI-nya jalan di **terminal lokal**, bukan di server remote.

> Terinspirasi dari [Warp.dev](https://warp.dev) — tapi **bebas pake custom AI provider** (DeepSeek, OpenAI, Ollama, OpenRouter, dll)

---

## ✨ Fitur

| Fitur | Command | Description |
|-------|---------|-------------|
| 🤖 **AI Chat** | `opsterm how to check disk` | Tanya AI apa aja |
| 🔑 **Smart SSH** | `opsterm ssh vps-utama` | SSH tanpa hafal IP |
| 🔗 **Multi-hop SSH** | `opsterm ssh internal --via bastion` | SSH lewat jump host |
| 📁 **SCP File Transfer** | `opsterm scp file.txt server:/path` | Upload/download lewat server |
| ⚡ **Workflow** | `opsterm run deploy-app` | Multi-step otomatis (SSH/SCP/local) |
| 🔐 **Vault** | `opsterm vault set db_pass` | Simpan credential terenkripsi (AES-128) |
| 🔗 **Pipe Mode** | `docker ps \| opsterm \"error?\"` | Explain output command pake AI |
| 🗜️ **RTK AI** | `auto` | Kompres output command 60-95% sebelum ke AI (irit token) |
| 💻 **Shell Integration** | `opsterm explain-last` | Explain output command sebelumnya |
| ⌨️ **Tab Completion** | `source <(opsterm completion bash)` | Auto-complete nama server/workflow |
| 📋 **History** | `opsterm history` | Riwayat semua command |
| 🛠️ **Custom Provider** | `opsterm config set ai.model gpt-4` | Bebas pilih provider AI |

---

## ⚡ Instalasi

### 🐧 Linux

```bash
# 1. Clone repo
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm

# 2. Setup (bikin symlink + init config)
./setup.sh

# 3. Set API key
export OPSTERM_API_KEY='sk-deepseek-...'

# 4. Tab completion (bash)
echo 'source <(opsterm completion bash)' >> ~/.bashrc
source ~/.bashrc

# 5. Coba
opsterm --help
```

### 🍎 macOS

```bash
# 1. Clone repo
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm

# 2. Setup (bikin symlink + init config)
./setup.sh

# 3. Set API key
export OPSTERM_API_KEY='sk-deepseek-...'

# 4. Tab completion — macOS default pake Zsh
echo 'source <(opsterm completion zsh)' >> ~/.zshrc
source ~/.zshrc

# 5. Zsh plugin (opsional — buat ai-last, ai-explain)
echo 'source ~/opsterm/zsh/opsterm.plugin.zsh' >> ~/.zshrc

# 6. Coba
opsterm --help
```

> **Catatan macOS**: Pastikan Python 3 tersedia (`python3 --version`).
> macOS Ventura/Sonoma/Sequoia udah include Python 3.
> Kalo belum ada: `brew install python@3`

### 🔧 Setelah Install

```bash
# Tambah provider AI
opsterm provider add default --api-key 'sk-...' --model gpt-4o

# Lihat daftar provider
opsterm provider list

# Ganti provider
opsterm provider default openai
```

### 🔄 Update

OpsTerm punya **self-update** bawaan:

```bash
# Cek & install update
opsterm update
```

Auto-check tiap 24 jam dan ngasih notif:

```
╭─ ⚡ OpsTerm Update ──────────────────────────────────────
│  Version 1.0.0 → 1.1.0 available!
│  Run: opsterm update
╰──────────────────────────────────────────────────────────
```

Cek version sekarang:

```bash
opsterm --version
```

> **Note:** Install version spesifik pake tag:
> ```bash
> curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/v1.0.0/bin/opsterm -o ~/.local/bin/opsterm
>```

---

## 📖 Pemakaian

### 🤖 AI Mode (Default)
```bash
# Minta command
opsterm cari file log lebih dari 1GB
# → $ find /var/log -type f -size +1G

# Minta penjelasan
opsterm explain apa itu kubernetes

# Generate command
opsterm buat docker compose untuk nginx + postgres
```

### 🔑 SSH — Multi-hop Support
```bash
opsterm ssh vps-utama                        # SSH langsung
opsterm ssh internal-server --via bastion    # SSH lewat jump host
opsterm ssh vps                              # Fuzzy match — cukup "vps"
```

Bisa set jump host permanen di config server:
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
opsterm scp ./config.yaml vps-utama:/home/ubuntu/

# Download file dari server
opsterm scp vps-utama:logs/app.log .

# Lewat jump host
opsterm scp file.txt internal-server:/tmp/ --via bastion
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

### 🔐 Vault — Credential Terenkripsi
```bash
# Init vault (set master password)
opsterm vault init

# Simpan credential
opsterm vault set db_password "supersecret"
opsterm vault set api_key "sk-..."

# Ambil credential
opsterm vault get db_password    # Output: supersecret

# Lihat daftar key
opsterm vault list

# Hapus key
opsterm vault rm db_password

# Kunci vault
opsterm vault lock
```

Bisa pake env var biar ga perlu input password tiap kali:
```bash
export OPSTERM_VAULT_PASSWORD='master-password'
```

### 🔗 Pipe Mode
```bash
kubectl get pods | opsterm "ada yang error?"
docker logs webapp --tail 50 | opsterm "analisa error ini"
free -h | opsterm "apakah memory cukup?"
netstat -tlnp | opsterm "port apa aja yang terbuka?"
```

### 🗜️ RTK AI — Kompresi Token

Auto-kompres output command **60-95%** sebelum dikirim ke AI — irit token, respon lebih cepet, biaya lebih murah.

```
# Sebelum RTK: output pytest = 597 chars → AI
# Setelah RTK: output pytest =   18 chars → AI (-96% 🚀)
```

| Fitur | Detail |
|-------|--------|
| 🔌 **Auto-detect** | RTK deteksi tipe output (git diff, pytest, docker, logs, dll) |
| 📐 **Smart threshold** | Skip kompresi kalo <200 chars (ga worth it) |
| 🔄 **Graceful fallback** | RTK gak terinstall? Jalan normal. Gak ada error. |
| ⚙️ **Config** | `opsterm config set rtk.enabled false` untuk matiin |
| 🟢 **Status** | Nampil `🟢 RTK x.x.x` di `opsterm provider list` |

**Kompatibel dengan:** Pipe mode, `opsterm explain-last`, auto-exec mode.

> 💡 RTK opsional — install: `curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh`

### 💻 Shell Integration (Zsh Plugin)
```bash
# Load plugin di .zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh

# Fitur:
opsterm last               # Lihat output command terakhir
opsterm explain-last       # Explain output pake AI
```

### ⌨️ Tab Completion
```bash
opsterm [Tab]        # Daftar subcommand
opsterm ssh [Tab]    # Daftar nama server
opsterm run [Tab]    # Daftar nama workflow
```

### 🛠️ Manajemen Server
```bash
opsterm servers list           # Lihat semua server (dengan kolom PROXY)
opsterm servers add            # Tambah server baru
opsterm servers edit vps       # Edit server
opsterm servers rm vps         # Hapus server
```

### ⚙️ Konfigurasi
```bash
opsterm config list            # Lihat semua config
opsterm config set ai.model deepseek-chat
opsterm config set ai.api_url https://api.deepseek.com/v1/chat/completions
opsterm config set shell.confirm_before_exec true
```

---

## 🔧 File Konfigurasi

Config disimpan di `~/.opsterm/`:

> 📦 Pindah dari `~/.ai-workflows` → `~/.opsterm/` (auto-migrasi pas pertama jalan)

```
~/.opsterm/
├── config.yaml       # AI provider & shell settings
├── servers.yaml      # Daftar server (+ proxy jump)
├── workflows.yaml    # Workflow (SSH/SCP/local)
├── vault.json        # Credential terenkripsi (AES-128)
├── history.db        # Riwayat (SQLite, otomatis)
├── last_output.txt   # Output command terakhir
└── last_command.txt  # Command terakhir
```

Environment variables:
```bash
export OPSTERM_DIR="/path/to/custom/config"   # Override direktori config
export OPSTERM_API_KEY="sk-..."                # AI API key
export OPSTERM_VAULT_PASSWORD="..."            # Vault master password
```

---

## 🧪 Contoh Workflow

### deploy-full — Deployment dengan file transfer
```yaml
workflows:
  deploy-full:
    desc: "Upload config + pull + restart"
    steps:
      - scp: "./docker-compose.yml"
        to: "/home/ubuntu/app/docker-compose.yml"
        ssh: vps-utama
        desc: "Upload file compose"
      - ssh: vps-utama
        command: "cd /home/ubuntu/app && docker compose pull && docker compose up -d"
        desc: "Pull images & restart"
      - command: "echo '✅ Deploy selesai!'"
        desc: "Notifikasi"
```

### cek-server — Cek kesehatan server
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

### multi-hop-deploy — Deploy lewat bastion
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
- [x] RTK AI — kompresi token (auto-detect, hemat 60-95%)
- [ ] Tmux/screen session manager
- [ ] Docker exec shortcut (`opsterm exec <container>`)
- [ ] SSH config parser (import dari ~/.ssh/config)

---

## 📝 Lisensi

MIT

---

## 📚 Dokumentasi Lengkap

Untuk penjelasan detail tentang arsitektur, tech stack, dan design decisions:

👉 [docs/](docs/id/README.md) — 📐 Arsitektur | 🔧 Tech Stack | 🤔 Design Decisions | 🎯 Fitur | 📊 Diagram

🖼️ **Diagram Arsitektur:** [docs/ops-term-architecture.png](docs/ops-term-architecture.png)

> Terinspirasi dari [Warp.dev](https://warp.dev) — AI di terminal lu, pake provider sendiri.
