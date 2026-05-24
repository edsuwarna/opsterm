# 🎯 Fitur OpsTerm — Lengkap

Dokumen ini menjelaskan **semua fitur** yang tersedia di OpsTerm, lengkap dengan contoh penggunaan dan penjelasan.

---

## 📋 Daftar Semua Fitur

| # | Fitur | CLI Command | Kategori |
|---|-------|------------|----------|
| 1 | 🤖 **AI Chat** | `opsterm <prompt>` | Core |
| 2 | 🔑 **Smart SSH** | `opsterm ssh <server>` | Core |
| 3 | 🔗 **Multi-hop SSH** | `opsterm ssh <srv> --via <proxy>` | Core |
| 4 | 📁 **SCP File Transfer** | `opsterm scp <src> <dst>` | Core |
| 5 | ⚡ **Workflow** | `opsterm run <name>` | Core |
| 6 | 🔐 **Vault** | `opsterm vault` | Core |
| 7 | 🔗 **Pipe Mode** | `cmd \| opsterm <prompt>` | Core |
| 8 | 💻 **Shell Integration** | `opsterm explain-last` | Shell |
| 9 | ⌨️ **Tab Completion** | `opsterm completion bash\|zsh` | Utility |
| 10 | 🛠️ **Server Manager** | `opsterm servers` | Management |
| 11 | 📋 **Workflow Manager** | `opsterm workflows` | Management |
| 12 | ⚙️ **Config Manager** | `opsterm config` | Management |
| 13 | 📖 **History** | `opsterm history` | Management |
| 14 | 🚀 **Init** | `opsterm init` | Setup |

---

## 1️⃣ 🤖 AI Chat

Bertanya apa pun ke AI langsung dari terminal.

```bash
# Minta command shell
opsterm cari file log lebih dari 1GB
# Output: $ find /var/log -type f -size +1G

# Minta penjelasan
opsterm explain apa itu reverse proxy

# Generate docker compose
opsterm buat docker compose untuk nginx + postgres

# Tanya general
opsterm how to check disk usage in linux
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
opsterm ssh vps-utama

# Fuzzy match — cukup sebagian nama
opsterm ssh vps

# Lihat daftar server dulu
opsterm servers list
```

**Konfigurasi server di `~/.ai-workflows/servers.yaml`:**
```yaml
servers:
  vps-utama:
    host: "203.0.113.1"
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
opsterm ssh internal-server --via bastion

# Via config (permanen)
opsterm ssh internal-server  # otomatis lewat bastion
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
opsterm scp ./config.yaml vps-utama:/home/ubuntu/

# Download dari server ke lokal
opsterm scp vps-utama:logs/app.log .

# Lewat jump host
opsterm scp file.txt internal-server:/tmp/ --via bastion
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
opsterm run deploy-app

# Lihat daftar workflow
opsterm workflows list
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
opsterm vault init

# Simpan credential
opsterm vault set db_password "supersecret"
opsterm vault set github_token "ghp_..."

# Ambil credential
opsterm vault get db_password    # Output: supersecret

# List keys
opsterm vault list

# Hapus key
opsterm vault rm db_password

# Kunci vault (clear password dari memory)
opsterm vault lock
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
kubectl get pods | opsterm "ada yang error?"
docker logs webapp --tail 100 | opsterm "analisa error ini"
free -h | opsterm "apakah memory cukup?"
netstat -tlnp | opsterm "port apa aja yang terbuka?"

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
opsterm last

# Explain output command terakhir pake AI
opsterm explain-last
```

**Fitur:**
- **`opsterm-last`** — alias ke `opsterm last`
- **`opsterm-explain`** — alias ke `opsterm explain-last`
- **`opsterm-ti`** — AI + Terminal Integration: tanya AI, extract command, auto-execute

**Cara kerja:**
- Zsh `preexec` hook → simpen command sebelum jalan
- Output command terakhir disimpan di `~/.ai-workflows/last_output.txt`
- `opsterm explain-last` → baca file → kirim ke AI

---

## 9️⃣ ⌨️ Tab Completion

Auto-complete buat bash dan zsh — ga perlu hafal nama server/workflow.

```bash
# Bash
source <(opsterm completion bash)

# Zsh
source <(opsterm completion zsh)

# Atau permanen:
echo 'source <(opsterm completion bash)' >> ~/.bashrc
echo 'source <(opsterm completion zsh)' >> ~/.zshrc
```

**Yang bisa di-complete:**
| Context | Completion |
|---------|-----------|
| `opsterm [Tab]` | Semua subcommand |
| `opsterm ssh [Tab]` | Nama server |
| `opsterm run [Tab]` | Nama workflow |
| `opsterm scp [Tab]` | `server:` prefix |
| `opsterm servers [Tab]` | `add`, `edit`, `rm`, `list` |
| `opsterm vault [Tab]` | `init`, `set`, `get`, `list`, `rm`, `lock` |
| `opsterm --via [Tab]` | Nama proxy server |

---

## 🔟 🛠️ Server Manager

CRUD untuk server — simpan, edit, hapus konfigurasi server.

```bash
# Lihat semua server (dengan kolom PROXY)
opsterm servers list
# Output:
# NAMA       HOST            USER    PORT  PROXY  DESKRIPSI
# vps-utama  203.0.113.1  ubuntu  22    —      Tencent Cloud VPS

# Tambah server baru (interaktif)
opsterm servers add

# Edit server
opsterm servers edit vps-utama

# Hapus server
opsterm servers rm vps-utama
```

Data disimpan di `~/.ai-workflows/servers.yaml`.

---

## 1️⃣1️⃣ 📋 Workflow Manager

CRUD untuk workflow — simpan, edit, hapus workflow.

```bash
# Lihat semua workflow
opsterm workflows list

# Tambah workflow baru (interaktif)
opsterm workflows add

# Edit workflow (buka editor)
opsterm workflows edit deploy-app

# Hapus workflow
opsterm workflows rm deploy-app
```

Data disimpan di `~/.ai-workflows/workflows.yaml`.

---

## 1️⃣2️⃣ ⚙️ Config Manager

Lihat dan set konfigurasi OpsTerm.

```bash
# Lihat semua config
opsterm config list

# Set nilai
opsterm config set ai.model deepseek-chat
opsterm config set ai.api_url https://api.deepseek.com/v1/chat/completions
opsterm config set ai.temperature 0.3
opsterm config set shell.confirm_before_exec true

# Get nilai spesifik
opsterm config get ai.model
```

Data disimpan di `~/.ai-workflows/config.yaml`.

---

## 1️⃣3️⃣ 📖 History

Riwayat semua command yang pernah dijalanin.

```bash
# Lihat 20 riwayat terakhir
opsterm history

# Lihat 50 riwayat terakhir
opsterm history 50
```

**Output:**
```
  [1] 🤖 2026-05-24 15:30 [ai] how to check disk usage
  [2] 🔑 2026-05-24 15:35 [ssh] vps-utama
  [3] ⚡ 2026-05-24 15:40 [workflow] deploy-app
  [4] 🔗 2026-05-24 15:45 [pipe] docker ps | opsterm error
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
opsterm init
```

**Yang dibuat:**
- `~/.ai-workflows/config.yaml` — template AI provider
- `~/.ai-workflows/servers.yaml` — contoh server
- `~/.ai-workflows/workflows.yaml` — contoh workflow

---

## 🎯 Use Case Matrix

| Yang Mau Dilakuin | Command |
|-------------------|---------|
| **SSH ke server** | `opsterm ssh vps-utama` |
| **SSH lewat bastion** | `opsterm ssh internal --via bastion` |
| **Upload file** | `opsterm scp file.txt server:/path/` |
| **Download file** | `opsterm scp server:log.txt .` |
| **Deploy app** | `opsterm run deploy-app` |
| **Cek server health** | `opsterm run cek-server` |
| **Tanya command** | `opsterm how to check disk` |
| **Explain error** | `docker logs -n50 \| opsterm "error?"` |
| **Explain last command** | `opsterm explain-last` |
| **Simpan password** | `opsterm vault set db_pass` |
| **Ambil password** | `opsterm vault get db_pass` |
| **Auto-complete** | `opsterm [Tab]` |
| **Lihat riwayat** | `opsterm history` |
| **Setup dari awal** | `opsterm init` |

---

## 🔜 Fitur Mendatang (Roadmap)

- [ ] **Tmux/screen session manager** — manage multi-session dari OpsTerm
- [ ] **Docker exec shortcut** — `opsterm exec <container>` langsung masuk container
- [ ] **SSH config parser** — import dari `~/.ssh/config`
- [ ] **Fish shell support** — completion & plugin buat Fish
- [ ] **Multi-hop chain** — `opsterm ssh server --via jump1,jump2`
- [ ] **Vault auto-unlock** — unlock vault pake fingerprint/keychain
