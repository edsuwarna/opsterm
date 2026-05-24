# 🎯 Fitur OpsTerm — Lengkap

Dokumen ini menjelaskan **semua fitur** yang tersedia di OpsTerm, lengkap dengan contoh penggunaan dan penjelasan.

---

## 📋 Daftar Semua Fitur

| # | Fitur | CLI Command | Kategori |
|---|-------|------------|----------|
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

Bertanya apa pun ke AI langsung dari terminal.

```bash
# Minta command shell
ai cari file log lebih dari 1GB
# Output: $ find /var/log -type f -size +1G

# Minta penjelasan
ai explain apa itu reverse proxy

# Generate docker compose
ai buat docker compose untuk nginx + postgres

# Tanya general
ai how to check disk usage in linux
```

**Cara kerja:**
1. Load config (API key, model, URL dari config.yaml)
2. Build prompt + system message
3. HTTP POST ke AI provider (OpenAI-compatible API)
4. Parse response JSON
5. Print ke terminal
6. Simpan ke history (SQLite)
7. Deteksi `$` prefix → offer auto-exec

**Provider support:** DeepSeek, OpenAI, OpenRouter, Ollama, vLLM, atau apapun yang OpenAI-compatible.

---

## 2️⃣ 🔑 Smart SSH

SSH ke server tanpa perlu hafal IP address.

```bash
# Langsung connect
ai ssh vps-utama

# Fuzzy match — cukup sebagian nama
ai ssh vps

# Lihat daftar server dulu
ai servers list
```

**Konfigurasi server di `~/.ai-workflows/servers.yaml`:**
```yaml
servers:
  vps-utama:
    host: "43.157.204.199"
    user: "ubuntu"
    port: 22
    key: "~/.ssh/id_ed25519"
    desc: "Tencent Cloud VPS utama"
```

**Yang bisa di-configure:**
- `host` — IP atau domain
- `user` — SSH username
- `port` — port SSH (default: 22)
- `key` — path ke private key
- `proxy` — jump host (lihat fitur multi-hop)
- `desc` — deskripsi

---

## 3️⃣ 🔗 Multi-hop SSH

SSH ke server internal yang cuma bisa diakses lewat jump host/bastion.

```bash
# Via CLI (per-call)
ai ssh internal-server --via bastion

# Via config (permanen)
ai ssh internal-server  # otomatis lewat bastion
```

**Config permanen di servers.yaml:**
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
    proxy: "bastion"           # <-- otomatis lewat bastion
```

**Cara kerja:**
- Pake SSH `-J` (ProxyJump) flag
- Chain bisa panjang: `ssh -J jump1,jump2 server`
- Proxy server di-resolve dari servers.yaml juga

---

## 4️⃣ 📁 SCP File Transfer

Upload/download file antara lokal dan server — pakai syntax `server:path`.

```bash
# Upload dari lokal ke server
ai scp ./config.yaml vps-utama:/home/ubuntu/

# Download dari server ke lokal
ai scp vps-utama:logs/app.log .

# Lewat jump host
ai scp file.txt internal-server:/tmp/ --via bastion
```

**Cara kerja:**
- Parse `server:path` → resolve ke user@host:path
- Sama kaya SSH: support proxy jump, key file, custom port
- Pake `scp` system command via subprocess

---

## 5️⃣ ⚡ Workflow

Multi-step automation yang jalanin beberapa command secara berurutan.

```bash
# Jalanin workflow
ai run deploy-app

# Lihat daftar workflow
ai workflows list
```

**Contoh workflow:**
```yaml
workflows:
  deploy-full:
    desc: "Full deployment dengan file transfer"
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

**Step types:**
| Type | Format | Fungsi |
|------|--------|--------|
| `ssh` | `ssh: <server>` + `command:` | Jalanin command di server remote |
| `scp` | `scp: <src>` + `to: <dst>` + `ssh: <server>` | Transfer file ke server |
| `command` | `command:` | Jalanin command lokal |
| `confirm` | `confirm: true` | Minta konfirmasi user sebelum lanjut |
| `wait` | `wait: <detik>` | Tunggu beberapa detik |

---

## 6️⃣ 🔐 Vault — Encrypted Credentials

Nyimpen credentials (API key, password, token) secara terenkripsi.

```bash
# Init vault (set master password)
ai vault init

# Simpan credential
ai vault set db_password "supersecret"
ai vault set github_token "ghp_..."

# Ambil credential
ai vault get db_password    # Output: supersecret

# List keys
ai vault list

# Hapus key
ai vault rm db_password

# Kunci vault (clear password dari memory)
ai vault lock
```

**Teknis:**
- **Encryption:** AES-128-CBC via `cryptography.fernet.Fernet`
- **Key derivation:** PBKDF2-HMAC-SHA256, 600.000 iterasi
- **Master password:** dari `OPSTERM_VAULT_PASSWORD` env atau prompt
- **Fallback:** kalo `cryptography` gak terinstall → HMAC + XOR (kurang aman)
- **Data:** encrypted JSON di `~/.ai-workflows/vault.json`

---

## 7️⃣ 🔗 Pipe Mode

Kirim output command ke AI untuk dianalisa.

```bash
# Explain output
kubectl get pods | ai "ada yang error?"
docker logs webapp --tail 100 | ai "analisa error ini"
free -h | ai "apakah memory cukup?"
netstat -tlnp | ai "port apa aja yang terbuka?"

# Pipe tanpa prompt spesifik
df -h | ai
# AI otomatis: "Jelaskan output ini"
```

**Cara kerja:**
1. Deteksi stdin (`sys.stdin.isatty() == False`)
2. Baca stdin → simpen sebagai `stdin_data`
3. Build prompt: "Output dari command:\n```\n{stdin_data}\n```\nPertanyaan: {prompt}"
4. Kirim ke AI → print response

---

## 8️⃣ 💻 Shell Integration (Zsh Plugin)

Integrasi dengan Zsh shell untuk ngeliat & explain output command terakhir.

```bash
# Load di .zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh

# Lihat output command terakhir
ai last

# Explain output command terakhir pake AI
ai explain-last
```

**Fitur:**
- **`ai-last`** — alias ke `ai last`
- **`ai-explain`** — alias ke `ai explain-last`
- **`ai-ti`** — AI + Terminal Integration: tanya AI, extract command, auto-execute

**Cara kerja:**
- Zsh `preexec` hook → simpen command sebelum jalan
- Output command terakhir disimpan di `~/.ai-workflows/last_output.txt`
- `ai explain-last` → baca file → kirim ke AI

---

## 9️⃣ ⌨️ Tab Completion

Auto-complete buat bash dan zsh — ga perlu hafal nama server/workflow.

```bash
# Bash
source <(ai completion bash)

# Zsh
source <(ai completion zsh)

# Atau permanen:
echo 'source <(ai completion bash)' >> ~/.bashrc
echo 'source <(ai completion zsh)' >> ~/.zshrc
```

**Yang bisa di-complete:**
| Context | Completion |
|---------|-----------|
| `ai [Tab]` | Semua subcommand |
| `ai ssh [Tab]` | Nama server |
| `ai run [Tab]` | Nama workflow |
| `ai scp [Tab]` | `server:` prefix |
| `ai servers [Tab]` | `add`, `edit`, `rm`, `list` |
| `ai vault [Tab]` | `init`, `set`, `get`, `list`, `rm`, `lock` |
| `ai --via [Tab]` | Nama proxy server |

---

## 🔟 🛠️ Server Manager

CRUD untuk server — simpan, edit, hapus konfigurasi server.

```bash
# Lihat semua server (dengan kolom PROXY)
ai servers list
# Output:
# NAMA       HOST            USER    PORT  PROXY  DESKRIPSI
# vps-utama  43.157.204.199  ubuntu  22    —      Tencent Cloud VPS

# Tambah server baru (interaktif)
ai servers add

# Edit server
ai servers edit vps-utama

# Hapus server
ai servers rm vps-utama
```

Data disimpan di `~/.ai-workflows/servers.yaml`.

---

## 1️⃣1️⃣ 📋 Workflow Manager

CRUD untuk workflow — simpan, edit, hapus workflow.

```bash
# Lihat semua workflow
ai workflows list

# Tambah workflow baru (interaktif)
ai workflows add

# Edit workflow (buka editor)
ai workflows edit deploy-app

# Hapus workflow
ai workflows rm deploy-app
```

Data disimpan di `~/.ai-workflows/workflows.yaml`.

---

## 1️⃣2️⃣ ⚙️ Config Manager

Lihat dan set konfigurasi OpsTerm.

```bash
# Lihat semua config
ai config list

# Set nilai
ai config set ai.model deepseek-chat
ai config set ai.api_url https://api.deepseek.com/v1/chat/completions
ai config set ai.temperature 0.3
ai config set shell.confirm_before_exec true

# Get nilai spesifik
ai config get ai.model
```

Data disimpan di `~/.ai-workflows/config.yaml`.

---

## 1️⃣3️⃣ 📖 History

Riwayat semua command yang pernah dijalanin.

```bash
# Lihat 20 riwayat terakhir
ai history

# Lihat 50 riwayat terakhir
ai history 50
```

**Output:**
```
  [1] 🤖 2026-05-24 15:30 [ai] how to check disk usage
  [2] 🔑 2026-05-24 15:35 [ssh] vps-utama
  [3] ⚡ 2026-05-24 15:40 [workflow] deploy-app
  [4] 🔗 2026-05-24 15:45 [pipe] docker ps | ai error
```

**Ikon mode:**
| Ikon | Mode |
|------|------|
| 🤖 | AI chat |
| 🔑 | SSH |
| ⚡ | Workflow |
| 🔗 | Pipe mode |
| 💻 | Shell command |
| 📁 | SCP transfer |
| 🔐 | Vault |

Data disimpan di SQLite: `~/.ai-workflows/history.db`.

---

## 1️⃣4️⃣ 🚀 Init

Setup awal — bikin file konfigurasi default.

```bash
ai init
```

**Yang dibuat:**
- `~/.ai-workflows/config.yaml` — template AI provider
- `~/.ai-workflows/servers.yaml` — contoh server
- `~/.ai-workflows/workflows.yaml` — contoh workflow

---

## 🎯 Use Case Matrix

| Yang Mau Dilakuin | Command |
|-------------------|---------|
| **SSH ke server** | `ai ssh vps-utama` |
| **SSH lewat bastion** | `ai ssh internal --via bastion` |
| **Upload file** | `ai scp file.txt server:/path/` |
| **Download file** | `ai scp server:log.txt .` |
| **Deploy app** | `ai run deploy-app` |
| **Cek server health** | `ai run cek-server` |
| **Tanya command** | `ai how to check disk` |
| **Explain error** | `docker logs -n50 \| ai "error?"` |
| **Explain last command** | `ai explain-last` |
| **Simpan password** | `ai vault set db_pass` |
| **Ambil password** | `ai vault get db_pass` |
| **Auto-complete** | `ai [Tab]` |
| **Lihat riwayat** | `ai history` |
| **Setup dari awal** | `ai init` |

---

## 🔜 Fitur Mendatang (Roadmap)

- [ ] **Tmux/screen session manager** — manage multi-session dari OpsTerm
- [ ] **Docker exec shortcut** — `ai exec <container>` langsung masuk container
- [ ] **SSH config parser** — import dari `~/.ssh/config`
- [ ] **Fish shell support** — completion & plugin buat Fish
- [ ] **Multi-hop chain** — `ai ssh server --via jump1,jump2`
- [ ] **Vault auto-unlock** — unlock vault pake fingerprint/keychain
