# 🚀 OpsTerm — AI Terminal Assistant

**OpsTerm** adalah AI terminal assistant lokal yang nempel di terminal laptop lu. 
Bisa SSH ke server mana pun tanpa kehilangan akses AI — karena AI-nya jalan di **terminal lokal**, bukan di server remote.

> Mirip Warp.dev tapi **bebas pake custom AI provider** (DeepSeek, OpenAI, Ollama, OpenRouter, dll)

---

## ✨ Fitur

| Fitur | Command | Description |
|-------|---------|-------------|
| 🤖 **AI Chat** | `ai how to check disk usage` | Tanya AI apa aja |
| 🔑 **Smart SSH** | `ai ssh vps-utama` | SSH tanpa hafal IP |
| ⚡ **Workflow** | `ai run deploy-app` | Multi-step workflow otomatis |
| 🔗 **Pipe Mode** | `docker ps \| ai "ada error?"` | Explain output command |
| 💾 **Saved Servers** | `ai servers add` | Simpan config server |
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

### 4. Coba!

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

### 🔑 SSH ke Server
```bash
ai ssh vps-utama          # Connect ke VPS utama
ai ssh vps                # Fuzzy match — cukup "vps"
```

### ⚡ Workflow
```bash
# Jalanin workflow tersimpan
ai run deploy-app

# Lihat daftar workflow
ai workflows list

# Tambah workflow baru
ai workflows add
```

### 🔗 Pipe Mode
```bash
# Kirim output command ke AI
kubectl get pods | ai "ada yang error?"
docker logs webapp --tail 50 | ai "analisa error ini"
free -h | ai "apakah memory cukup?"
```

### 🛠️ Manajemen Server
```bash
ai servers list           # Lihat semua server
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
├── servers.yaml      # Daftar server
├── workflows.yaml    # Daftar workflow
└── history.db        # Riwayat (SQLite, auto)
```

Atau bisa di-override dengan env var:
```bash
export OPSTERM_DIR="/path/to/custom/config"
export OPSTERM_API_KEY="sk-..."
```

---

## 🧪 Example Workflows

### deploy-app
```yaml
workflows:
  deploy-app:
    desc: "Deploy ke VPS utama"
    steps:
      - ssh: vps-utama
        command: "cd /home/ubuntu/app && git pull && docker compose restart"
        desc: "Pull & restart"
      - command: "echo '✅ Deploy selesai!'"
```

### cek-server
```yaml
  cek-server:
    desc: "Cek status server"
    steps:
      - ssh: vps-utama
        command: |
          echo "=== UPTIME ===" && uptime
          echo "=== DISK ===" && df -h /
          echo "=== DOCKER ===" && docker ps
        desc: "System check"
```

---

## 🗺️ Roadmap

- [x] AI chat dengan custom provider
- [x] Smart SSH connector
- [x] Saved workflows
- [x] Pipe mode
- [x] History & riwayat
- [ ] Tab completion untuk server/workflow names
- [ ] AI-aware shell integration (zsh plugin)
- [ ] Multi-hop SSH (SSH lewat jump host)
- [ ] SCP/file transfer via workflow
- [ ] Tmux/screen session manager
- [ ] Vault/encrypted credentials

---

## 📝 License

MIT
