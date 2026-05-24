# 📐 Arsitektur & System Design

Dokumen ini menjelaskan secara detail gimana OpsTerm bekerja — dari mulai user ngetik command sampai hasilnya keluar.

---

## 🏗️ Arsitektur Umum

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ CLI Terminal  │  │ Zsh Plugin   │  │ Pipe (stdin)     │  │
│  │ ai <command>  │  │ ai-last      │  │ cmd | ai <prompt>│  │
│  │ ai ssh <svr>  │  │ ai-explain   │  │                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
└─────────┼─────────────────┼────────────────────┼────────────┘
          │                 │                    │
          ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   CLI ROUTER (argparse)                     │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────┐ ┌───────┐  │
│  │ ai <ask> │ │ ai ssh   │ │ai scp  │ │ai run│ │ai vault│  │
│  │ (default)│ │          │ │        │ │      │ │        │  │
│  └────┬─────┘ └────┬─────┘ └───┬────┘ └──┬───┘ └───┬───┘  │
└───────┼────────────┼───────────┼─────────┼──────────┼──────┘
        │            │           │         │          │
        ▼            ▼           ▼         ▼          ▼
┌────────────────────────────────────────────────────────────┐
│                      ENGINES                                │
│                                                             │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────────┐  │
│  │ AI Client    │  │ SSH Runner │  │ SCP Transfer       │  │
│  │ (urllib)     │  │ (subproc)  │  │ (subprocess)       │  │
│  │ OpenAI-compat│  │ multi-hop  │  │ local ↔ remote     │  │
│  └──────┬───────┘  └─────┬──────┘  └────────┬───────────┘  │
│         │                │                   │              │
│  ┌──────▼────────────────▼───────────────────▼──────────┐  │
│  │              Workflow Executor                       │  │
│  │  Step: SSH → SCP → Local → Confirm → Wait           │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              Vault (Encrypted)                      │  │
│  │  AES-128-CBC + PBKDF2 (via cryptography)            │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────┐  ┌────────────┐                          │
│  │ Config Loader│  │ History    │                          │
│  │ (YAML/JSON)  │  │ (SQLite)   │                          │
│  └──────┬───────┘  └─────┬──────┘                          │
└─────────┼────────────────┼──────────────────────────────────┘
          │                │
          ▼                ▼
┌────────────────────────────────────────────────────────────┐
│                    EXTERNAL SYSTEMS                         │
│                                                             │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ AI Provider API  │  │ SSH Servers  │  │ Local File    │ │
│  │ (DeepSeek,OpenAI,│  │ (VPS, cloud, │  │ System        │ │
│  │  Ollama, etc)    │  │  instances)  │  │ (config, vault)│ │
│  └─────────────────┘  └──────────────┘  └───────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Alur Eksekusi

### Flow 1: AI Chat (`ai how to check disk`)

```
User input: "ai how to check disk"
             │
             ▼
    ┌─────────────────┐
    │ 1. Parse args    │ ← argparse: subcmd=None (default AI mode)
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 2. Load config   │ ← config.yaml (API key, model, URL)
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. Build prompt  │ ← + stdin_data if piped
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ 4. AI Chat (ai_chat())          │
    │    POST ke /v1/chat/completions  │
    │    Headers: Authorization Bearer │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. Parse response│ ← JSON: choices[0].message.content
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 6. Print output  │ ← stdout
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 7. Auto-exec?    │ ← Kalo response ada $, tanya user
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 8. Save history  │ ← SQLite (mode, input, output)
    └──────────────────┘
```

### Flow 2: SSH (`ai ssh vps-utama --via bastion`)

```
User input: "ai ssh vps-utama --via bastion"
             │
             ▼
    ┌───────────────────────┐
    │ 1. Parse args          │ ← subcmd="ssh", server="vps-utama"
    └──────────┬─────────────┘    proxy="bastion"
               │
               ▼
    ┌───────────────────────┐
    │ 2. Load servers.yaml   │ ← get_servers()
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 3. Lookup server       │ ← _server_lookup("vps-utama")
    │    vps-utama:          │
    │      host: 43.157..    │
    │      user: ubuntu      │
    │      key: ~/.ssh/...   │
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 4. Resolve proxy      │ ← _resolve_proxy("bastion")
    │    → "ubuntu@10.0.0.1"│    → format: user@host[:port]
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 5. Build SSH command   │ ← ["ssh", "-J", proxy, "-i", key,
    │                          "ubuntu@43.157..", "-t"]
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 6. execvp()            │ ← Replace proses dengan SSH interaktif
    │    → Interactive SSH   │
    └───────────────────────┘
```

### Flow 3: Workflow (`ai run deploy-app`)

```
User input: "ai run deploy-app"
             │
             ▼
    ┌──────────────────────┐
    │ 1. Parse args         │ ← subcmd="run", workflow="deploy-app"
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 2. Load workflows    │ ← workflows.yaml
    │    deploy-app:       │
    │      steps: [...]    │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 3. Iterate steps     │
    │                       │
    │  Step 1: ssh          │────→ SSH ke server + execute command
    │  Step 2: scp          │────→ SCP file ke server
    │  Step 3: local        │────→ Local shell command
    │  Step 4: confirm      │────→ Prompt user Y/n
    │  Step 5: wait         │────→ time.sleep(n)
    │                       │
    └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 4. Done              │ ← "✅ Workflow selesai!"
    └──────────────────────┘
```

### Flow 4: Pipe Mode (`docker ps | ai "any errors?"`)

```
User input: "docker ps | ai any errors?"
             │
             ▼
    ┌──────────────────────────────────┐
    │ 1. stdin detected (not isatty()) │ ← sys.stdin.read()
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │ 2. stdin_data = "CONTAINER ID..."│ ← Output docker ps
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │ 3. Build prompt:                 │
    │    "Output dari command:         │
    │     ```                          │
    │     CONTAINER ID IMAGE...        │
    │     ```                          │
    │                                 │
    │     Pertanyaan: any errors?"    │
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │ 4. Kirim ke AI           ← sama kayak AI Chat flow
    └──────────────────────────────────┘
```

### Flow 5: Vault (`ai vault set db_password`)

```
User input: "ai vault set db_password"
             │
             ▼
    ┌──────────────────────────────┐
    │ 1. Unlock vault              │
    │    - Cek OPSTERM_VAULT_PASSWORD│ ← env var
    │    - Atau prompt password     │ ← getpass()
    │    - Derive key via PBKDF2    │ ← 600k iterations, SHA256
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │ 2. Encrypt value             │
    │    - cryptography.Fernet     │ ← AES-128-CBC
    │    - atau fallback HMAC+XOR   │
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │ 3. Simpan ke vault.json      │
    │    {"keys": {                │
    │      "db_password": {        │
    │        "data": "<encrypted>" │
    │      }                       │
    │    }, "salt": "<base64>"}   │
    └──────────────────────────────┘
```

---

## 📁 Manajemen State

OpsTerm **tidak punya daemon atau background process**. Semua state disimpan di file:

| File | Format | Isi |
|------|--------|-----|
| `config.yaml` | YAML | AI provider, model, api_url, shell settings |
| `servers.yaml` | YAML | Daftar server: host, user, port, key, proxy |
| `workflows.yaml` | YAML | Daftar workflow: steps (ssh/scp/local) |
| `vault.json` | JSON (encrypted) | Credential terenkripsi (AES-128) |
| `history.db` | SQLite | Riwayat command (mode, input, output) |
| `last_output.txt` | Text | Output command terakhir (buat explain-last) |
| `last_command.txt` | Text | Command terakhir |

**Data flow:**

```
Config dibaca setiap kali command jalan → tidak ada caching di memory
History ditulis setelah command selesai → append-only
Vault dibuka pake password → disimpan di memory SAMPAI ai vault lock
Last output ditulis oleh zsh plugin → dibaca oleh ai last/explain-last
```

---

## 🔒 Keamanan

### API Key
- Bisa dari **env var** (`OPSTERM_API_KEY`) — recommended
- Atau di **config.yaml** — tapi hati-hati kalo di-share
- Gitignored (`config.yaml` ada di `.gitignore`)

### Vault
- **AES-128-CBC** via `cryptography.fernet.Fernet`
- **PBKDF2** dengan 600.000 iterasi SHA-256 untuk key derivation
- Master password **tidak pernah disimpan** — cuma di memory selama sesi
- Bisa di-unlock via env var `OPSTERM_VAULT_PASSWORD`
- Fallback encryption (HMAC + XOR) kalo cryptography gak terinstall

### SSH
- Pake **SSH key** dari local filesystem (bukan password)
- ProxyJump via `-J` flag (secure, encrypted)
- Config server bisa specify key path per-server

---

## 🧪 Testing & Error Handling

### Error recovery di workflow:
```python
if result.returncode != 0:
    print(f"❌ Step {i} gagal")
    # Tanya user: lanjut atau stop?
    cont = input("Lanjut? [y/N] ")
    if cont not in ("y", "yes"):
        print("⛔ Workflow dihentikan.")
        return
```

### Fallback strategy:
- **AI call gagal** → print error message, jangan crash
- **File config rusak** → return empty dict, jangan crash
- **Vault password salah** → retry, jangan crash
- **SSH server gak reachable** → SSH sendiri yang handle error

---

## 🚀 Performance

| Operasi | Waktu (approx) | Catatan |
|---------|----------------|---------|
| AI Chat (DeepSeek) | 1-3 detik | Tergantung provider & network |
| SSH Connect | < 1 detik | Langsung execvp, ga ada overhead |
| SCP Transfer | Varies | Tergantung ukuran file & bandwidth |
| Workflow (3 steps) | 5-15 detik | Tergantung step complexity |
| Vault encrypt | < 100ms | PBKDF2 600k iterasi ~50ms |
| Config load | < 10ms | YAML parsing minimal |
| History write | < 5ms | SQLite append |

**Memory footprint:** ~15-30MB (Python interpreter) + overhead sesuai operasi.

---

Selanjutnya: [🔧 Tech Stack →](tech-stack.md)
