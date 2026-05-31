# 🚀 OpsTerm — AI Terminal Assistant

> 🌍 [README.md](README.md) — Read English version

**OpsTerm** adalah AI terminal assistant yang tinggal di terminal kamu.
SSH ke server mana pun tanpa kehilangan akses AI — karena AI jalan di **terminal lokal**, bukan di server remote.

> Terinspirasi dari [Warp.dev](https://warp.dev) — tapi **gratis pake provider AI apapun** (DeepSeek, OpenAI, Ollama, OpenRouter, dll.)

---

## ✨ Fitur

| Fitur | Command | Description |
|-------|---------|-------------|
| 🤖 **AI Chat** | `opsterm how to check disk` | Tanya AI apa aja |
| 💬 **Chat REPL** | `opsterm chat` | Mode chat interaktif dengan history |
| 🔑 **Smart SSH** | `opsterm ssh vps-utama` | SSH tanpa perlu hapal IP |
| 🔗 **Multi-hop SSH** | `opsterm ssh internal --via bastion` | SSH lewat jump host |
| 📁 **SCP File Transfer** | `opsterm scp file.txt server:/path` | Upload/download lewat server |
| ⚡ **Workflow** | `opsterm run deploy-app` | Otomasi multi-step (SSH/SCP/local) |
| 🔐 **Vault** | `opsterm vault set db_pass` | Kredensial terenkripsi (AES-128) |
| 🔗 **Pipe Mode** | `docker ps \| opsterm "error?"` | Explain output command pake AI |
| 🗜️ **RTK AI** | `auto` | Kompres output command 60-95% sebelum ke AI (irit token) |
| 💻 **Shell Integration** | `opsterm explain-last` | Explain output command sebelumnya |
| 🏓 **Server Ping** | `opsterm servers ping vps` | Cek koneksi SSH & latency |
| 🔌 **Test Provider** | `opsterm provider test openai` | Tes koneksi provider AI |
| 📡 **Model Provider** | `opsterm provider models openai` | Lihat daftar model tersedia |
| ⌨️ **Tab Completion** | `source <(opsterm completion bash)` | Auto-complete servers/workflows |
| 📋 **History** | `opsterm history` | Riwayat semua command |
| 🔄 **Self-Update** | `opsterm update` | Cek & install versi terbaru |
| 🛠️ **Custom Provider** | `opsterm provider add <name> --api-key KEY` | Bebas pilih provider AI |
| 🏥 **Diagnostics** | `opsterm doctor` | Cek konfigurasi & diagnosis masalah |
| 📋 **Detail Server** | `opsterm servers show <name>` | Lihat detail koneksi server |
| ⚙️ **Custom System Prompt** | `opsterm config set ai.system_prompt <text>` | Ubah kepribadian AI |

> 💡 Semua list command (`provider list`, `servers list`, `history`) support `--json` flag buat scripting.

---

## 🚀 Quick Start

### Install

**Linux/macOS** — satu perintah curl, gak perlu clone repo:

```bash
# Install latest (branch main)
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
```

Atau pake **versi release tertentu** (direkomendasiin biar stabil):

```bash
# Install v0.4.0
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/v0.4.0/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
```

Cek [Releases page](https://github.com/edsuwarna/opsterm/releases) buat versi terbaru.

Pastiin `~/.local/bin` ada di `PATH` kamu:

```bash
# Tambah ke ~/.bashrc atau ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Konfigurasi provider AI (sekali doang)

```bash
# Tambah OpenAI (nanti bisa ganti provider kapan aja)
opsterm provider add default --api-key 'sk-...' --model gpt-4o

# Lihat semua provider yang didukung
opsterm provider supported

# Lihat yang udah dikonfigurasi
opsterm provider list
```

### Verifikasi

```bash
opsterm --help
```

### Update

OpsTerm punya fitur update otomatis:

```bash
# Cek update & install
opsterm update
```

Caranya:
1. Cek versi terbaru dari GitHub
2. Download & verifikasi script baru
3. Backup versi lama sebagai `opsterm.bak`
4. Replace dengan versi baru

> 💡 OpsTerm otomatis ngecek update setiap 24 jam sekali — bakal muncul notif kalo ada versi baru.

---

## 💡 Bisa Buat Apa Aja?

### 🎯 Langsung tanya AI

```bash
# Minta command
opsterm how to find large files

# Minta AI jelasin output
opsterm explain-last

# Pipe mode
docker ps | opsterm "error?"
```

### 🌐 SSH — gak perlu hapal IP lagi

Simpen server sekali, SSH pake nama:

```yaml
# ~/.opsterm/servers.yaml
servers:
  - name: vps-utama
    host: 203.0.113.10
    user: root
    proxy:                    # opsional jump host
      host: 198.51.100.5
      user: ubuntu
  - name: db-server
    host: 10.0.0.5
    user: admin
```

```bash
opsterm ssh vps-utama             # SSH langsung
opsterm ssh internal --via bastion # Lewat proxy/jump host
opsterm scp file.txt server:/path  # Transfer file
opsterm servers ping vps-utama    # Cek koneksi
```

### ⚡ Workflows — otomasi multi-step

Bikin workflow reusable pake YAML:

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
      - local: "echo '=== Cek semua server ==='"
      - ssh: vps-utama
        command: "df -h && free -h && uptime"
      - ssh: db-server
        command: "pg_isready && systemctl status postgresql --no-pager"
```

```bash
opsterm run deploy-app
opsterm run check-all
```

### 🔐 Vault — kredensial terenkripsi

Simpen data sensitif (API key, password) lokal pake AES-128:

```bash
opsterm vault init                          # Buat vault (set master password)
opsterm vault set db_password               # Simpen kredensial
opsterm vault get db_password               # Ambil (minta master password)
opsterm vault list                          # Lihat semua key
opsterm vault rm db_password                # Hapus
opsterm vault lock                          # Enkripsi ulang dan bersihin dari memori

# Pake value vault di config
opsterm vault set openai_key
opsterm config set ai.api_key vault://openai_key
```

---

## 🧠 Fitur AI

### Custom AI Provider

OpsTerm work dengan **API apapun yang kompatibel sama OpenAI** — bawa provider sendiri:

```bash
opsterm provider supported                 # Lihat semua provider yang didukung
opsterm provider add openai --api-key sk-... --model gpt-4o
opsterm provider add deepseek --api-key sk-... --model deepseek-chat \
  --api-url https://api.deepseek.com/v1/chat/completions
opsterm provider add ollama --api-url http://localhost:11434/v1  # lokal (gak perlu key)

opsterm provider default deepseek           # Ganti default
opsterm provider test openai                # Tes koneksi
opsterm provider models openai              # Lihat daftar model
opsterm provider list                       # Lihat semua konfigurasi
```

Auto-kompres output command **60-95%** sebelum dikirim ke AI — irit token, respon lebih cepet, biaya lebih murah.

### Token Compression via RTK

```
# Sebelum RTK: output pytest = 597 chars → AI
# Setelah RTK: output pytest =   18 chars → AI (-96% 🚀)
```

| Fitur | Keuntungan |
|-------|------------|
| 🔌 **Auto-detect** | RTK deteksi tipe output (git diff, pytest, docker, logs, dll) |
| 🎯 **Smart compression** | Keep line relevan, buang noise |
| ⚡ **Fast** | Kompresi sub-detik, bahkan untuk output gede |
| 🟢 **Status** | Nampil `🟢 RTK x.x.x` di `opsterm provider list` |

### Session Context

OpsTerm maintain **konteks percakapan** selama session (30-menit window). Setiap prompt termasuk pertukaran sebelumnya jadi lo bisa tanya lanjutan:

```bash
# Tanya lanjutan — OpsTerm inget yang barusan lo lakuin!
opsterm how to check disk usage
# → Jawab pake df -h / du -sh

opsterm what about inodes?
# → Ngerti lo masih bahas disk commands
```

### Custom System Prompt

Sesuaiin system prompt AI sesuai kebutuhan:

```bash
# Biar jawabnya singkat dan teknis
opsterm config set ai.system_prompt "Kamu asisten terminal, jawab pake command langsung."

# Pake bahasa Indonesia
opsterm config set ai.system_prompt "Jawab pake bahasa Indonesia santai."

# Mode edukasi
opsterm config set ai.system_prompt "Jelasin kayak lagi ngajar anak SMA."
```

> 💡 System prompt ditambahin ke setiap request AI. Cocok buat ngatur tone, gaya, atau konteks.

---

## 💻 Pemakaian

```bash
opsterm <command> [options]

# Minta command
opsterm how to check disk usage

# Generate command
opsterm generate docker compose restart postgres
```

### Smart SSH

```bash
opsterm ssh vps-utama                    # Fuzzy match nama server
opsterm ssh vps                          # "vps" cocok sama "vps-utama"
opsterm ssh internal --via bastion       # Multi-hop via ProxyJump
opsterm scp file.txt vps-utama:/home/ubuntu/
opsterm scp vps-utama:/var/log/syslog .
opsterm scp file.txt vps-utama:/tmp --via bastion
opsterm servers ping vps-utama           # Cek koneksi SSH
opsterm servers show vps-utama           # Lihat detail server
```

### Workflows

```bash
opsterm run <name>
opsterm run deploy-app
```

### Tab Completion

```bash
opsterm completion bash > ~/.opsterm/completion.sh
source ~/.opsterm/completion.sh

```

### Diagnostics

Cek instalasi dan konfigurasi OpsTerm:

```bash
opsterm doctor
```

Yang dicek:
- ✅ File konfigurasi ada dan valid
- ✅ API key terisi
- ✅ Provider URL reachable
- ✅ Versi terbaru vs terinstall
- ✅ `~/.local/bin` ada di PATH

```bash
# Atau tambah ke shell config biar permanen:
echo "source ~/.opsterm/completion.sh" >> ~/.bashrc

opsterm ssh [Tab]    # Daftar server
opsterm run [Tab]    # Daftar workflow
```

### 🛠️ Server Management
```bash
opsterm servers list           # Lihat semua server (dengan kolom PROXY)
opsterm servers show vps       # Lihat detail server
opsterm servers add            # Tambah server baru
opsterm servers edit vps       # Edit server
opsterm servers rm vps         # Hapus server
opsterm servers ping vps       # Cek koneksi SSH & latency
```

### ⚙️ Configuration
```bash
opsterm config list            # Lihat semua config
opsterm config set ai.model deepseek-chat
opsterm config set ai.api_url https://api.deepseek.com/v1/chat/completions
opsterm config set shell.confirm_before_exec true
```

---

## 🔧 File Config

Config disimpan di `~/.opsterm/`:

```
~/.opsterm/
├── config.yaml       # Pengaturan AI provider & shell
├── servers.yaml      # Daftar server (+ proxy jump)
├── workflows.yaml    # Daftar workflow (SSH/SCP/local)
├── vault.json        # Kredensial terenkripsi (AES-128)
├── history.db        # Riwayat (SQLite, otomatis)
├── last_output.txt   # Output command terakhir
└── last_command.txt  # Command terakhir
```

> ⚡ Berpindah dari `~/.ai-workflows` ke `~/.opsterm/` — migrasi otomatis pas pertama jalan.

Environment variables:
```bash
export OPSTERM_DIR="/path/to/custom/config"   # Override direktori config
export OPSTERM_API_KEY="sk-..."                # AI API key
export OPSTERM_VAULT_PASSWORD="..."            # Vault master password
```

---

## 🧪 Contoh Workflow

### Deploy Basic
```yaml
# ~/.opsterm/workflows.yaml
workflows:
  - name: deploy-app
    steps:
      - command: "cd /home/ubuntu/app && docker compose pull && docker compose up -d"
      - command: "echo '✅ Deploy selesai!'"
```

### Health Check Multi-Server
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
      - local: "echo '✅ Selesai!'"
```

### Deploy dari CI
```yaml
workflows:
  - name: deploy-ci
    steps:
      - command: "cd /opt/app && git pull && systemctl restart app"
```

---

## 📋 Roadmap

- [x] AI chat dengan custom provider
- [x] Smart SSH (fuzzy name match, ProxyJump)
- [x] SCP file transfer (local ↔ server ↔ server)
- [x] Multi-step workflows (SSH/SCP/local)
- [x] Encrypted vault (AES-128)
- [x] Command history (SQLite)
- [x] Pipe mode (kirim output command ke AI)
- [x] SSH via jump host (--via)
- [x] Tab completion (bash/zsh)
- [x] Vault integration dengan config
- [x] Shell operators (`&&`, `|`, `>`) di local commands
- [x] Multi-hop SCP (transfer file lewat bastion)
- [x] RTK token compression
- [x] Provider management (add, list, test, models)
- [x] Server ping (cek koneksi)
- [x] Chat REPL (mode interaktif)
- [x] JSON output (`--json` flag)
- [x] Config validation
- [ ] Web dashboard (lihat workflows dan servers di browser)
- [ ] SSH config import (dari `~/.ssh/config`)
- [ ] Multi-language AI responses
- [ ] Plugin system

---

<p align="center">
  <sub>Dibuat dengan ❤️ untuk developer yang manage banyak server.</sub>
  <br>
  <sub>Terinspirasi dari <a href="https://warp.dev">Warp.dev</a> — AI di terminal lu, pake provider sendiri.</sub>
</p>
