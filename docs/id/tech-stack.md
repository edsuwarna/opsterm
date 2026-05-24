# 🔧 Tech Stack

Dokumen ini menjelaskan teknologi yang dipake di OpsTerm — dari bahasa pemrograman sampai protocol komunikasi.

---

## 🎯 Ringkasan

| Layer | Teknologi | Versi |
|-------|-----------|-------|
| **Bahasa** | Python 3 | >= 3.7+ |
| **CLI Parser** | `argparse` (stdlib) | Built-in |
| **Config Format** | YAML (custom parser) | Zero dep |
| **HTTP Client** | `urllib` (stdlib) | Built-in |
| **Database** | SQLite via `sqlite3` | Built-in |
| **Encryption** | `cryptography` (optional) | >= 3.0 |
| **SSH/SCP** | System `ssh` / `scp` | OS default |
| **Shell** | Zsh plugin (zsh hooks) | Zsh only |

> **Zero dependencies wajib** — cukup Python 3 stdlib. Semuanya built-in.
> Satu-satunya optional dep: `pip install cryptography` (buat vault).

---

## 🐍 Bahasa: Python 3

### Kenapa Python?

| Faktor | Alasan |
|--------|--------|
| **Availability** | Ada di setiap Linux/macOS, ga perlu install |
| **Stdlib lengkap** | JSON, SQLite, HTTP, argparse, hashlib — semua built-in |
| **Cross-platform** | Works on Linux & macOS tanpa perubahan |
| **Rapid development** | Cepet bikin prototype & fitur baru |

### Kenapa BUKAN Go / Rust?

| Bahasa | Masalah |
|--------|---------|
| **Go** | Perlu compile cross-platform, binary size >10MB |
| **Rust** | Learning curve tinggi, compile time lama |
| **Node.js** | Heavy dependency (node_modules), ga ada di default system |
| **Bash** | Susah maintain >1000 baris, parsing JSON susah |

Python adalah **paling praktis** untuk CLI tool yang harus zero-dep dan portable.

---

## 📦 Zero-Dependency Strategy

Ini adalah **nilai jual utama** OpsTerm. Gimana caranya?

### Yang Biasanya Pake Library Pihak Ketiga:

| Kebutuhan | Lib Pilihan | Solusi OpsTerm |
|-----------|------------|----------------|
| **YAML Parsing** | PyYAML | Custom minimal parser (~80 baris) |
| **HTTP Requests** | requests | `urllib.request` (stdlib) |
| **Arg Parsing** | click, typer | `argparse` (stdlib) |
| **Database** | SQLAlchemy | `sqlite3` (stdlib) |
| **Encryption** | cryptography | `hashlib` + `hmac` (stdlib) + optional cryptography |

### Custom YAML Parser

Parser YAML di OpsTerm itu **minimal — cuma support subset YAML yang dipake**:

**Supported:**
- Key-value: `key: value`
- Nested mapping via indent
- Lists: `- item`
- Nested objects in lists
- Comments (`#`)
- Strings, numbers, booleans, null

**NOT supported:**
- YAML anchors (`&anchor`, `*alias`)
- Multi-line strings (`|`, `>`)
- Inline JSON (`{key: value}`)
- Complex types (timestamps, sets)

**Kenapa ga pake PyYAML?**
1. **Dependency** — user harus `pip install` dulu
2. **Overkill** — kita cuma pake subset kecil YAML
3. **Maintainable** — parser cuma 80 baris, mudah dipahami

---

## 🗄️ SQLite History

### Schema:
```sql
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now','localtime')),
    mode TEXT,        -- 'ai', 'ssh', 'workflow', 'pipe', 'shell', 'scp', 'vault'
    input TEXT,       -- command/pertanyaan (max 500 chars)
    output TEXT       -- response (max 2000 chars)
);
```

### Kenapa SQLite?
- **Built-in Python** (`import sqlite3`)
- **Zero config** — file db otomatis dibuat
- **Permanent** — riwayat gak ilang meski terminal ditutup
- **Searchable** — bisa query pake SQL

---

## 🔗 Protocol: OpenAI-Compatible API

AI Client pake format yang **kompatibel dengan OpenAI**.

### Request:
```json
POST /v1/chat/completions
Authorization: Bearer <api_key>
Content-Type: application/json

{
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "Kamu adalah asisten terminal..."},
        {"role": "user", "content": "cara check disk usage"}
    ],
    "temperature": 0.3,
    "max_tokens": 1024
}
```

### Response:
```json
{
    "id": "chatcmpl-...",
    "choices": [{
        "message": {
            "role": "assistant",
            "content": "$ df -h /"
        }
    }]
}
```

### Provider yang Didukung:
| Provider | URL Base | Auth |
|----------|----------|------|
| **DeepSeek** | `https://api.deepseek.com/v1` | API Key |
| **OpenAI** | `https://api.openai.com/v1` | API Key |
| **OpenRouter** | `https://openrouter.ai/api/v1` | API Key |
| **Ollama** (local) | `http://localhost:11434/v1` | None |
| **vLLM** (self-host) | `http://your-server:8000/v1` | Optional |
| **Any OpenAI-compat** | Configurable | API Key / None |

---

## 🔐 Enkripsi Vault

### Primary (recommended): `cryptography.fernet.Fernet`

```
Master Password
       │
       ▼
   PBKDF2 (SHA-256, 600k iterations, salt)
       │
       ▼
   AES-128-CBC (Fernet)
       │
       ▼
   Base64-encoded token
       │
       ▼
   vault.json
```

### Fallback (no cryptography): HMAC + XOR

Kalo `cryptography` gak terinstall, OpsTerm pake fallback encryption:
1. **Key derivation**: PBKDF2 from `hashlib` (stdlib)
2. **Encryption**: XOR cipher dengan random IV
3. **Integrity**: HMAC-SHA256

⚠️ Fallback ini **kurang aman** dibanding AES. Recommended: `pip install cryptography`

---

## 📡 Komunikasi SSH/SCP

### SSH Command Building:

```python
# Direct SSH
ssh -i ~/.ssh/id_ed25519 -p 22 ubuntu@203.0.113.1 -t

# Multi-hop via ProxyJump
ssh -J ubuntu@10.0.0.1:22 ubuntu@203.0.113.1 -t
```

### SCP Command Building:

```python
# Upload
scp -i ~/.ssh/id_ed25519 local.txt ubuntu@host:/remote/path/

# Download
scp -i ~/.ssh/id_ed25519 ubuntu@host:/remote/path/ local.txt

# Via jump host
scp -o ProxyJump=ubuntu@bastion:22 file.txt ubuntu@internal:/path/
```

### Interaction:
- **SSH**: `os.execvp()` → replace proses, interactive
- **SCP**: `subprocess.run()` → blocking sampai selesai
- **Workflow SSH**: `subprocess.run()` → non-interactive, command via SSH

---

## 🐚 Zsh Plugin Integration

### Hooks yang dipake:

| Hook | Timing | Fungsi |
|------|--------|--------|
| `preexec` | Sebelum command jalan | Simpan command ke `last_command.txt` |
| `precmd` | Setelah command selesai | (reserved untuk future use) |

### Aliases:

```zsh
alias opsterm-last='ai last'
alias opsterm-explain='ai explain-last'
```

### Cara kerja `opsterm-ti` (AI + Terminal Integration):
```zsh
opsterm-ti() {
    # 1. Tanya AI
    opsterm "$*"
    
    # 2. Ekstrak command dari response (yang mulai dengan $)
    # 3. Tanya user: jalanin?
    # 4. Kalo ya, execute
}
```

---

## 🎯 Perbandingan dengan Alternatif

| Aspek | OpsTerm | Warp.dev | ShellGPT | Claude Code |
|-------|---------|----------|----------|-------------|
| **Dependencies** | ✅ Zero | ❌ Binary | ⚠️ pip | ❌ Binary |
| **Custom AI** | ✅ Bebas | ❌ Vendor lock | ✅ Banyak | ❌ Claude only |
| **SSH Multi-hop** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Workflow** | ✅ Multi-step | ❌ No | ❌ No | ❌ No |
| **Vault** | ✅ Encrypted | ❌ No | ❌ No | ❌ No |
| **Tab Completion** | ✅ bash+zsh | ✅ built-in | ❌ No | ❌ No |
| **Platform** | Linux + macOS | macOS only | Linux + macOS | Linux + macOS |
| **Weight** | ~50KB (script) | ~200MB+ | ~10MB | ~500MB+ |
| **Zero Dep** | ✅ Python stdlib | ❌ | ✅ (stdin/out) | ❌ |

---

Selanjutnya: [🤔 Design Decisions →](design-decisions.md)
