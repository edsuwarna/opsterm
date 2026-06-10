# 🔧 Tech Stack

This document explains the technology used in OpsTerm — from the programming language to the communication protocol.

---

## 🎯 Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| **Language** | Python 3 | >= 3.7+ |
| **CLI Parser** | `argparse` (stdlib) | Built-in |
| **Config Format** | YAML (custom parser) | Zero dep |
| **HTTP Client** | `urllib` (stdlib) | Built-in |
| **Database** | SQLite via `sqlite3` | Built-in |
| **Encryption** | `cryptography` (optional) | >= 3.0 |
| **SSH/SCP** | System `ssh` / `scp` | OS default |
| **Shell** | Zsh plugin (zsh hooks) | Zsh only |

> **Zero mandatory dependencies** — just Python 3 stdlib. Everything is built-in.
> No optional dependencies needed — all features work with Python 3 stdlib.

---

## 🐍 Language: Python 3

### Why Python?

| Factor | Reason |
|--------|--------|
| **Availability** | Present on every Linux/macOS, no installation needed |
| **Full stdlib** | JSON, SQLite, HTTP, argparse, hashlib — all built-in |
| **Cross-platform** | Works on Linux & macOS without changes |
| **Rapid development** | Fast to prototype and build new features |

### Why NOT Go / Rust?

| Language | Issue |
|--------|---------|
| **Go** | Needs cross-platform compilation, binary size >10MB |
| **Rust** | High learning curve, slow compilation times |
| **Node.js** | Heavy dependency (node_modules), not available on default systems |
| **Bash** | Hard to maintain beyond 1000 lines, painful JSON parsing |

Python is the **most practical** choice for a CLI tool that must be zero-dependency and portable.

---

## 📦 Zero-Dependency Strategy

This is **OpsTerm's main selling point**. How is it done?

### What Typically Uses Third-Party Libraries:

| Requirement | Typical Library | OpsTerm Solution |
|-----------|------------|----------------|
| **YAML Parsing** | PyYAML | Custom minimal parser (~80 lines) |
| **HTTP Requests** | requests | `urllib.request` (stdlib) |
| **Arg Parsing** | click, typer | `argparse` (stdlib) |
| **Database** | SQLAlchemy | `sqlite3` (stdlib) |
| **Encryption** | cryptography | `hashlib` + `hmac` (stdlib) + optional cryptography |

### Custom YAML Parser

OpsTerm's YAML parser is **minimal — it only supports the YAML subset that OpsTerm uses**:

**Supported:**
- Key-value: `key: value`
- Nested mapping via indentation
- Lists: `- item`
- Nested objects in lists
- Comments (`#`)
- Strings, numbers, booleans, null

**NOT supported:**
- YAML anchors (`&anchor`, `*alias`)
- Multi-line strings (`|`, `>`)
- Inline JSON (`{key: value}`)
- Complex types (timestamps, sets)

**Why not use PyYAML?**
1. **Dependency** — users would need to `pip install` it first
2. **Overkill** — we only use a small YAML subset
3. **Maintainable** — the parser is only ~80 lines, easy to understand

---

## 🗄️ SQLite History

### Schema:
```sql
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now','localtime')),
    mode TEXT,        -- 'ai', 'ssh', 'workflow', 'pipe', 'shell', 'scp'
    input TEXT,       -- command/question (max 500 chars)
    output TEXT       -- response (max 2000 chars)
);
```

### Why SQLite?
- **Built into Python** (`import sqlite3`)
- **Zero config** — database file created automatically
- **Permanent** — history persists even after closing the terminal
- **Searchable** — can be queried using SQL

---

## 🔗 Protocol: OpenAI-Compatible API

The AI client uses a format that is **compatible with OpenAI**.

### Request:
```json
POST /v1/chat/completions
Authorization: Bearer ***
Content-Type: application/json

{
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are a terminal assistant..."},
        {"role": "user", "content": "how to check disk usage"}
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

### Supported Providers:
| Provider | Base URL | Auth |
|----------|----------|------|
| **DeepSeek** | `https://api.deepseek.com/v1` | API Key |
| **OpenAI** | `https://api.openai.com/v1` | API Key |
| **OpenRouter** | `https://openrouter.ai/api/v1` | API Key |
| **Ollama** (local) | `http://localhost:11434/v1` | None |
| **vLLM** (self-hosted) | `http://your-server:8000/v1` | Optional |
| **Any OpenAI-compat** | Configurable | API Key / None |

---

## 📡 SSH/SCP Communication

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
- **SSH**: `os.execvp()` → replaces the process, interactive
- **SCP**: `subprocess.run()` → blocking until complete
- **Workflow SSH**: `subprocess.run()` → non-interactive, command via SSH

---

## 🐚 Zsh Plugin Integration

### Hooks Used:

| Hook | Timing | Function |
|------|--------|--------|
| `preexec` | Before command runs | Save command to `last_command.txt` |
| `precmd` | After command finishes | (reserved for future use) |

### Aliases:

```zsh
alias opsterm-last='ai last'
alias opsterm-explain='ai explain-last'
```

### How `opsterm-ti` (AI + Terminal Integration) works:
```zsh
opsterm-ti() {
    # 1. Ask AI
    opsterm "$*"
    
    # 2. Extract command from response (lines starting with $)
    # 3. Ask user: run it?
    # 4. If yes, execute
}
```

---

## 🎯 Comparison with Alternatives

| Aspect | OpsTerm | Warp.dev | ShellGPT | Claude Code |
|-------|---------|----------|----------|-------------|
| **Dependencies** | ✅ Zero | ❌ Binary | ⚠️ pip | ❌ Binary |
| **Custom AI** | ✅ Any provider | ❌ Vendor lock | ✅ Many providers | ❌ Claude only |
| **SSH Multi-hop** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Workflow** | ✅ Multi-step | ❌ No | ❌ No | ❌ No |
| **Tab Completion** | ✅ bash+zsh | ✅ built-in | ❌ No | ❌ No |
| **Platform** | Linux + macOS | macOS only | Linux + macOS | Linux + macOS |
| **Weight** | ~50KB (script) | ~200MB+ | ~10MB | ~500MB+ |
| **Zero Dep** | ✅ Python stdlib | ❌ | ✅ (stdin/out) | ❌ |

---

Next: [🤔 Design Decisions →](design-decisions.md)
