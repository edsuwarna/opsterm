# OpsTerm — Product Requirements Document

> **Versi:** 1.0
> **Status:** Final Draft
> **Tanggal:** Juni 2026
> **Penulis:** Endang Suwarna

---

## Daftar Isi

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [Target Audience & User Personas](#3-target-audience--user-personas)
4. [Problem Statement](#4-problem-statement)
5. [Feature Specification](#5-feature-specification)
6. [Technical Architecture](#6-technical-architecture)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [User Experience](#8-user-experience)
9. [Competitive Analysis](#9-competitive-analysis)
10. [Roadmap & Milestones](#10-roadmap--milestones)
11. [Success Metrics](#11-success-metrics)
12. [Open Questions & Risks](#12-open-questions--risks)
13. [Glossary](#13-glossary)

---

## 1. Executive Summary

OpsTerm adalah **AI Terminal Assistant** berbasis CLI yang memungkinkan developer dan sysadmin berinteraksi dengan AI langsung dari terminal — tanpa perlu install apa-apa selain satu file Python.

**Value proposition inti:**
- **Zero dependency** — cukup Python 3 stdlib, satu file `opsterm`, langsung jalan
- **Any AI provider** — bebas pilih provider AI (DeepSeek, OpenAI, Ollama, OpenRouter, dll)
- **SSH-first** — semua fitur SSH built-in, termasuk multi-hop ProxyJump, SCP, dan SSH Escape
- **Workflow automation** — multi-step automation (SSH/SCP/local) via YAML
- **Ringan** — ~50KB file, no node_modules, no pip install, no binary 200MB+

**Tahap saat ini:** v0.8.0 — fitur core sudah matang (AI Chat, Smart SSH, SCP, Workflow, Web Dashboard, Connect, SSH Escape). Beberapa fitur advanced masih di branch terpisah.

---

## 2. Product Overview

### 2.1 Product Vision

> "Terminal AI assistant yang bekerja di mana pun — server mana pun, provider AI mana pun — tanpa instalasi rumit."

### 2.2 Positioning

OpsTerm adalah **alternatif open-source, provider-agnostic dari Warp.dev** untuk Linux — dengan tambahan SSH automation & workflow yang tidak dimiliki kompetitor.

### 2.3 Core Philosophy

1. **Local-first** — AI berjalan di terminal lokal, bukan di remote server
2. **Zero friction** — download satu file, langsung jalan. No `pip install`, no `npm i`
3. **Provider freedom** — tidak lock-in ke satu vendor AI
4. **SSH native** — bukan afterthought, SSH adalah first-class citizen
5. **Transparent** — kode bisa dibaca langsung, zero hidden dependencies

---

## 3. Target Audience & User Personas

### Persona 1: DevOps / Sysadmin (Primary)

| Atribut | Deskripsi |
|---------|-----------|
| **Pekerjaan** | DevOps Engineer, System Administrator, SRE |
| **Tools** | Terminal, SSH, Docker, Kubernetes, Ansible |
| **Pain points** | Hapal IP server, bolak-balik SSH ke banyak server, error troubleshooting |
| **Kebutuhan** | Cepat execute command di banyak server, bantu debug error, workflow automation |
| **Daya tarik OpsTerm** | Smart SSH, Multi-hop, Workflow automation, AI-assisted troubleshooting |

### Persona 2: Full-stack Developer (Secondary)

| Atribut | Deskripsi |
|---------|-----------|
| **Pekerjaan** | Software Engineer, Full-stack Developer |
| **Tools** | Terminal, Git, Docker, VS Code |
| **Pain points** | Males hapal command linux, butuh bantuan cepat tanpa buka browser |
| **Kebutuhan** | AI chat di terminal, bantu generate command, explain error |
| **Daya tarik OpsTerm** | AI Chat, Pipe Mode, Explain-last, zero setup |

### Persona 3: Homelab / Self-hoster (Tertiary)

| Atribut | Deskripsi |
|---------|-----------|
| **Pekerjaan** | Hobbyist, Self-hoster, Tech enthusiast |
| **Tools** | Terminal, Docker, Proxmox, VPS murah |
| **Pain points** | Banyak server kecil-kecil, perlu tool sederhana tanpa overhead |
| **Kebutuhan** | Manage banyak server tanpa jadi berat, workflow deployment simpel |
| **Daya tarik OpsTerm** | Ringan (~50KB), zero dependency, workflow automation, SCP |

---

## 4. Problem Statement

### 4.1 Masalah Utama

| # | Problem | Dampak | Solusi OpsTerm |
|---|---------|--------|----------------|
| 1 | Developer harus switch context ke browser untuk tanya AI | Produktivitas turun, konteks hilang | AI langsung di terminal |
| 2 | SSH ke banyak server = hapal IP & config masing-masing | Mental load tinggi, human error | Smart SSH (fuzzy match, YAML config) |
| 3 | Server internal cuma bisa lewat jump host | SSH command jadi panjang & ribet | Multi-hop SSH built-in (`--via`) |
| 4 | Troubleshooting error perlu copy-paste manual ke ChatGPT | Lambat, ga praktis | Pipe mode + explain-last + RTK |
| 5 | Vendor lock-in AI provider | Ga bisa ganti provider tanpa ganti tool | Provider-agnostic (OpenAI-compatible) |
| 6 | Tool AI terminal berat & dependency banyak | Ribet setup, ga cocok buat server minimal | Zero dependency, satu file 50KB |
| 7 | Automation task berulang (deploy, health check) manual | Repetitif, rawan lupa langkah | Workflow automation via YAML |

### 4.2 Use Case Matrix

| Skenario | Tool Sebelumnya | Dengan OpsTerm |
|-----------|----------------|----------------|
| Cari command linux | Buka browser → Google → Stack Overflow | `opsterm how to check disk usage` |
| SSH ke server | `ssh ubuntu@203.0.113.10 -i key.pem` | `opsterm ssh vps-utama` |
| SSH lewat bastion | `ssh -J user@bastion user@internal` | `opsterm ssh internal --via bastion` |
| Upload file ke server | `scp file user@203.0.113.10:/path/` | `opsterm scp file.txt vps-utama:/path/` |
| Diagnosa error dari log | Copy log → buka ChatGPT → paste → tunggu | `docker logs -n50 \| opsterm "any errors?"` |
| Deploy app multi-step | Buka tmux → SSH → git pull → docker compose | `opsterm run deploy-app` |
| Cek kesehatan semua server | SSH satu-satu ke setiap server | `opsterm run health-check` |

---

## 5. Feature Specification

### 5.1 Feature Taxonomy

Fitur dikelompokkan dalam 5 kategori:

```
CORE        — AI + SSH + SCP + Workflow (wajib ada)
SHELL       — Integrasi dengan shell (Zsh plugin, explain-last)
MANAGEMENT  — CRUD servers, workflows, config, history
UTILITY     — Dashboard, completion, export/import, diagnostics
SETUP       — Init, provider config, import SSH config
```

### 5.2 Current Features (v0.8.0)

#### 5.2.1 Core Features

| Fitur | Command | Prioritas | Status |
|-------|---------|-----------|--------|
| AI Chat | `opsterm <prompt>` | P0 | ✅ Live |
| Chat REPL | `opsterm chat` | P0 | ✅ Live |
| Smart SSH | `opsterm ssh <server>` | P0 | ✅ Live |
| Multi-hop SSH | `opsterm ssh <srv> --via <proxy>` | P0 | ✅ Live |
| SCP File Transfer | `opsterm scp <src> <dst>` | P0 | ✅ Live |
| Workflow Run | `opsterm run <name>` | P0 | ✅ Live |
| Pipe Mode | `cmd \| opsterm "question"` | P0 | ✅ Live |
| SSH Escape | `Ctrl+B` during SSH | P0 | ✅ Live |
| Connect (AI REPL) | `opsterm connect <server>` | P1 | ✅ Live |
| Batch SSH | `opsterm ssh --all <cmd>` | P1 | ✅ Live |
| Chat Resume | `opsterm chat --continue` | P1 | ✅ Live |
| History Search | `opsterm search <query>` | P1 | ✅ Live |
| RTK Token Compression | Auto (pipe/explain-last) | P1 | ✅ Live |

#### 5.2.2 Management Features

| Fitur | Command | Prioritas | Status |
|-------|---------|-----------|--------|
| Server Manager (CRUD) | `opsterm servers add/edit/rm/list` | P0 | ✅ Live |
| Server Ping | `opsterm servers ping <name>` | P1 | ✅ Live |
| Server Show | `opsterm servers show <name>` | P1 | ✅ Live |
| Server Rename | `opsterm servers rename <old> <new>` | P1 | ✅ Live |
| Import SSH Config | `opsterm servers import-ssh-config` | P2 | ✅ Live |
| Workflow Manager (CRUD) | `opsterm workflows add/edit/rm/list` | P0 | ✅ Live |
| Workflow Init | `opsterm workflows init` | P2 | ✅ Live |
| Config Manager | `opsterm config get/set/list` | P0 | ✅ Live |
| Config Validate | `opsterm config validate` | P1 | ✅ Live |
| Config Export | `opsterm export [file]` | P2 | ✅ Live |
| Config Import | `opsterm import <file>` | P2 | ✅ Live |
| Config Reset | `opsterm reset` | P2 | ✅ Live |
| History | `opsterm history [n]` | P1 | ✅ Live |
| Provider Add/List/Test/Models | `opsterm provider ...` | P0 | ✅ Live |

#### 5.2.3 Utility & Setup

| Fitur | Command | Prioritas | Status |
|-------|---------|-----------|--------|
| Web Dashboard | `opsterm web [--port] [--open]` | P1 | ✅ Live |
| Tab Completion (bash/zsh) | `opsterm completion bash\|zsh` | P1 | ✅ Live |
| JSON Output | `--json` flag on list commands | P2 | ✅ Live |
| Diagnostics | `opsterm doctor` | P1 | ✅ Live |
| Self-Update | `opsterm update` | P1 | ✅ Live |
| Init | `opsterm init` | P1 | ✅ Live |
| Zsh Plugin | Shell hooks (preexec/precmd) | P1 | ✅ Live |
| Custom System Prompt | `opsterm config set ai.system_prompt` | P2 | ✅ Live |

### 5.3 Future Features (Planned)

| Fitur | Priority | Target | Keterangan |
|-------|----------|--------|------------|
| Plugin System | P2 | v0.9+ | Sistem plugin/extensions untuk third-party integrations |
| Multi-language AI Responses | P2 | v0.9+ | AI bisa jawab sesuai bahasa yang diminta |
| Tmux/Screen Session Manager | P2 | v1.0 | Manage multi-sessions dari OpsTerm |
| Docker Exec Shortcut | P2 | v1.0 | `opsterm exec <container>` langsung masuk container |
| SSH Config Parser | P2 | v1.0 | Parse `~/.ssh/config` lebih advanced |
| Fish Shell Support | P3 | v1.0+ | Completion & plugin untuk Fish shell |
| Multi-hop Chain | P1 | Backlog | `opsterm ssh server --via jump1,jump2` |

### 5.4 Feature Detail: Core Features

#### 5.4.1 AI Chat

**Behavior:**
- Input tanpa subcommand → otomatis masuk mode AI Chat
- Mengirim prompt + system message ke provider AI (OpenAI-compatible)
- Mendeteksi apakah output mengandung command (diawali `$`) → offer auto-exec
- Menyimpan history ke SQLite

**Edge cases:**
- **No API key configured:** Tampilkan error message dengan instruksi setup
- **Provider timeout:** Timeout 30 detik, tampilkan error + saran retry
- **Very long output:** Potong di 2000 chars untuk display, tetap simpan full di DB
- **Network error:** Retry 2x, lalu fallback ke error message yang jelas

#### 5.4.2 Smart SSH

**Behavior:**
- Fuzzy match nama server dari servers.yaml
- Resolve server config (host, user, port, key, proxy)
- Multi-hop via `-J` (ProxyJump) flag
- Untuk SSH interactive: `os.execvp()` → replace proses
- Untuk command via SSH (workflow): `subprocess.run()`

**Edge cases:**
- **Server not found:** Fuzzy match ke nama terdekat + suggestion, atau error
- **Server name ambiguous:** Tampilkan list server yang cocok, minta user pilih
- **Connection timeout:** Timeout 10 detik, tampilkan error
- **Key file not found:** Fallback ke key default (~/.ssh/id_rsa, id_ed25519)
- **Proxy unreachable:** Error jelas bahwa proxy server yang bermasalah, bukan target

#### 5.4.3 SSH Escape Mode (`Ctrl+B`)

**Behavior:**
- Selama SSH session aktif, `Ctrl+B` meng-intercept input dan drop ke AI prompt
- Natural language → AI deteksi apakah perlu command → execute via SSH kedua → explain
- `!<command>` → execute langsung tanpa AI
- `resume` → balik ke SSH session
- `exit` → terminate SSH session
- Bisa di-disable via config: `opsterm config set ssh.escape_key_enabled false`

**Technical:**
- Menggunakan pseudoterminal (PTY) untuk intercept input
- Membuka SSH connection kedua dari local untuk eksekusi command
- Nonaktifkan key echo ke PTY selama escape mode

#### 5.4.4 Workflow Automation

**Behavior:**
- Step types: `ssh`, `command`, `scp`, `confirm`, `wait`
- Sequential execution: step gagal → workflow berhenti dengan error
- Output tiap step ditampilkan real-time

**Edge cases:**
- **Empty workflow:** Error message, jangan crash
- **Server in step not found:** Error di step itu, stop workflow
- **SCP to nonexistent path:** SCP error ditampilkan, workflow berhenti
- **`confirm` step in non-interactive mode:** Auto-skip dengan warning

#### 5.4.5 RTK Token Compression

**Behavior:**
- Otomatis kompres output command sebelum dikirim ke AI
- Threshold: skip kompresi untuk output <200 chars
- Auto-detect tipe output (git diff, pytest, docker ps, logs, journalctl)
- Graceful fallback jika RTK binary tidak terinstall

**Compression targets:**
| Output Type | Avg Raw | Avg Compressed | Savings |
|-------------|---------|----------------|---------|
| pytest results | 597 chars | 18 chars | 96% |
| git diff | ~500 chars | ~150 chars | 70% |
| docker ps | ~400 chars | ~100 chars | 75% |
| journalctl logs | ~1000 chars | ~200 chars | 80% |

---

## 6. Technical Architecture

### 6.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ CLI Terminal  │  │ Zsh Plugin   │  │ Pipe (stdin)     │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
└─────────┼─────────────────┼────────────────────┼────────────┘
          ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   CLI ROUTER (argparse)                      │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────┐ ┌───────┐  │
│  │ AI Chat  │ │ SSH      │ │ SCP    │ │ Run  │ │ Config│  │
│  └────┬─────┘ └────┬─────┘ └───┬────┘ └──┬───┘ └───┬───┘  │
└───────┼────────────┼───────────┼─────────┼──────────┼──────┘
        ▼            ▼           ▼         ▼          ▼
┌────────────────────────────────────────────────────────────┐
│                      ENGINES                                │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────────┐  │
│  │ AI Client    │  │ SSH Runner │  │ SCP Transfer       │  │
│  │ (urllib)     │  │ (subproc)  │  │ (subprocess)       │  │
│  └──────┬───────┘  └─────┬──────┘  └────────┬───────────┘  │
│  ┌──────▼────────────────▼───────────────────▼──────────┐  │
│  │              Workflow Executor                        │  │
│  └──────────────────────┬───────────────────────────────┘  │
│  ┌──────────────┐  ┌──────────────────────────────────┐    │
│  │ Config Loader│  │ History DB (SQLite)               │    │
│  └──────┬───────┘  └────────────────┬─────────────────┘    │
└─────────┼──────────────────────────┼───────────────────────┘
          ▼                          ▼
┌────────────────────────────────────────────────────────────┐
│                    EXTERNAL SYSTEMS                         │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ AI Provider API  │  │ SSH Servers  │  │ Local File    │ │
│  │ (DeepSeek,OpenAI,│  │ (VPS, cloud, │  │ System        │ │
│  │  Ollama, etc)    │  │  instances)  │  │ (config)      │ │
│  └─────────────────┘  └──────────────┘  └───────────────┘ │
└────────────────────────────────────────────────────────────┘
```

### 6.2 Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Language** | Python 3 | ≥ 3.7 |
| **CLI Parser** | `argparse` (stdlib) | Built-in |
| **Config Format** | YAML (custom parser) | Zero dep |
| **HTTP Client** | `urllib` (stdlib) | Built-in |
| **Database** | SQLite via `sqlite3` | Built-in |
| **Encryption** | `hashlib` + `hmac` (stdlib) | Built-in |
| **SSH/SCP** | System `ssh` / `scp` | OS default |
| **Shell Integration** | Zsh plugin (zsh hooks) | Zsh only |
| **File size** | ~50KB (single file) | — |

### 6.3 Design Decisions

Keputusan arsitektural yang sudah diambil (detail lengkap di `docs/design-decisions.md`):

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | **Language** | Python 3 | Ada di setiap Linux/macOS, full stdlib |
| 2 | **Architecture** | Single-file CLI | Portable, zero setup, mudah di-audit |
| 3 | **Dependencies** | Zero (stdlib only) | No pip install, no version conflicts |
| 4 | **Config format** | YAML | Human-readable, cocok buat config |
| 5 | **AI Protocol** | OpenAI-compatible API | Universal, banyak provider support |
| 6 | **SSH Method** | Subprocess + system SSH | Zero dep, support semua fitur SSH |
| 7 | **State** | File-based (no daemon) | Simpel, ga perlu service management |

---

## 7. Non-Functional Requirements

### 7.1 Performance

| Requirement | Target | Notes |
|-------------|--------|-------|
| Startup time | <200ms | Dari command di-exec sampai siap |
| AI response time | Tergantung provider | OpsTerm sendiri <50ms overhead |
| SSH connect | <5s | Timeout default 10s |
| RTK compression | <1s | Bahkan untuk output 50KB+ |
| Config load | <50ms | YAML parsing minimal |
| Web dashboard startup | <2s | Python HTTP server |
| Memory usage | <30MB | Peak saat AI request |
| Disk usage | <1MB | Binary + DB + config |

### 7.2 Security

| Requirement | Implementation |
|-------------|----------------|
| **API key storage** | File-based (`~/.opsterm/config.yaml`) with `chmod 600` |
| **Alternative** | Environment variable `OPSTERM_API_KEY` |
| **Export** | API keys masked in exported tar.gz |
| **SSH keys** | Menggunakan system SSH key yang sudah ada |
| **No remote agent** | Tidak install apapun di remote server |
| **Config encryption** | Optional via `cryptography` library |
| **Input sanitization** | Semua user input di-escape untuk shell |

### 7.3 Reliability

| Requirement | Target |
|-------------|--------|
| Uptime | N/A (CLI tool, no daemon) |
| Error handling | Semua error punya user-friendly message |
| Graceful degradation | RTK tidak terinstall → jalan normal tanpa error |
| Network timeout | 30s untuk AI, 10s untuk SSH |
| Config fallback | Jika YAML corrupt → fallback ke default + warning |

### 7.4 Compatibility

| Platform | Status |
|----------|--------|
| **Linux** | ✅ Primary target |
| **macOS** | ✅ Tested and supported |
| **Windows (WSL)** | ⚠️ Community-supported, belum di-test resmi |
| **Shell bash** | ✅ Completion tersedia |
| **Shell zsh** | ✅ Completion + plugin tersedia |
| **Shell fish** | ❌ Belum support |

### 7.5 Maintainability

| Requirement | Target |
|-------------|--------|
| **Code size** | <4000 lines (target di branch feat/versioning: ~2300) |
| **Documentation** | docs/ folder dengan 15+ dokumen |
| **Test coverage** | Belum ada automated test — target adopsi TDD di masa depan |
| **Release process** | Git tag → GitHub Release → single file distribution |

---

## 8. User Experience

### 8.1 User Flow: First-time Setup

```
User download opsterm
    │
    ▼
opsterm init → creates ~/.opsterm/ with default config
    │
    ▼
opsterm provider add default --api-key <key> --model <model>
    │
    ▼
opsterm doctor → verifikasi semuanya OK
    │
    ▼
opsterm servers add → tambah server pertama
    │
    ▼
Siap digunakan!
```

**Target time-to-value:** <5 menit dari download sampai bisa SSH pake AI.

### 8.2 User Flow: Daily Use

```
# Morning check
opsterm run health-check

# SSH + troubleshoot
opsterm ssh vps-utama
    └─ Ctrl+B → AI Escape Mode
        ├─ "cek disk usage"
        └─ resume

# Deploy
opsterm run deploy-app

# Quick question
opsterm how to check which ports are listening
```

### 8.3 UX Principles

1. **Zero surprise** — Setiap command punya output yang predictable
2. **Fuzzy everything** — Server names, commands, workflows — semua fuzzy match
3. **Fail gracefully** — Error messages yang actionable, bukan stack trace
4. **Progressive disclosure** — Fitur dasar mudah, fitur advanced ada tapi tidak wajib
5. **Keyboard-first** — Semua interaksi dari keyboard, no mouse needed
6. **Dark theme by default** — Web dashboard dark-themed, terminal natural

### 8.4 CLI Design Conventions

| Convention | Example |
|------------|---------|
| `opsterm <verb> <object>` | `opsterm ssh server`, `opsterm run workflow` |
| `opsterm <object> <verb>` | `opsterm servers list`, `opsterm servers add` |
| `--flag` for options | `--via`, `--port`, `--json` |
| `\--` untuk long flags | `--all`, `--continue`, `--open` |
| Single char flags | Hanya yang umum: `-v` (verbose) |

---

## 9. Competitive Analysis

### 9.1 Direct Competitors

| Aspek | OpsTerm | Warp.dev | Shell-GPT (sgpt) | Claude Code |
|-------|---------|----------|-------------------|-------------|
| **Platform** | Linux + macOS | macOS only | Linux + macOS | Linux + macOS |
| **Dependencies** | ✅ Zero | ❌ Binary ~200MB | ⚠️ pip + banyak | ❌ Binary ~500MB+ |
| **Custom AI Provider** | ✅ Any provider | ❌ Vendor lock (Warp AI) | ✅ Banyak | ❌ Claude only |
| **SSH** | ✅ Smart SSH + multi-hop | ❌ No | ❌ No | ❌ No |
| **SCP** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Workflows** | ✅ Multi-step YAML | ❌ No | ❌ No | ❌ No |
| **SSH Escape Mode** | ✅ Ctrl+B | ✅ Warp AI (macOS only) | ❌ No | ❌ No |
| **Tab Completion** | ✅ bash + zsh | ✅ built-in | ❌ No | ❌ No |
| **File size** | ~50KB | ~200MB+ | ~10MB | ~500MB+ |
| **Price** | Free (your own API key) | Free tier limited, Pro $20/mo | Free + OpenAI cost | $20/mo bundled |
| **Open Source** | ✅ ya | ❌ proprietary | ✅ ya | ❌ proprietary |

### 9.2 Indirect Competitors

| Tool | Strengths | Weaknesses vs OpsTerm |
|------|-----------|----------------------|
| **Tabby (Eugeny/tabby)** | Terminal emulator + AI | Berat (Electron), Windows-focused, no workflow |
| **Warp** | UI keren, native macOS | macOS only, vendor lock-in AI |
| **Fig** | Autocomplete canggih | macOS only, di-akuisisi, no SSH features |
| **iTerm2 + AI plugins** | Mature terminal emulator | macOS only, plugin ecosystem fragmented |
| **tmux + scripts** | Powerful, self-contained | No AI, manual scripting |

### 9.3 OpsTerm's Competitive Advantage

1. **SSH + AI combo** — Tidak ada kompetitor yang punya Smart SSH + AI langsung di terminal
2. **Zero dependency** — Satu file Python, langsung jalan — unique selling point
3. **Multi-hop SSH built-in** — DevOps daily necessity, tidak ada kompetitor yang support
4. **Workflow automation** — YAML-based multi-step automation, alternatif simpel dari Ansible
5. **Provider freedom** — Bebas ganti AI provider kapan aja

---

## 10. Roadmap & Milestones

### 10.1 Version History

| Version | Tanggal | Highlights |
|---------|---------|------------|
| v0.1.0 | — | Inisialisasi project |
| v0.2.0 | — | AI Chat, Smart SSH |
| v0.3.0 | — | SCP, Workflow dasar |
| v0.4.0 | — | Multi-hop SSH, Pipe mode |
| v0.5.0 | — | Config export/import, Zsh plugin |
| v0.6.0 | — | RTK, Provider management, JSON output |
| v0.7.0 | — | Web Dashboard, SSH Escape mode |
| **v0.8.0** | **June 2026** | **Connect (AI REPL), SSH Escape fix** |

### 10.2 Planned Roadmap

| Version | Target | Features |
|---------|--------|----------|
| **v0.8.x** | Q3 2026 | Bug fixes, polish, performance improvements |
| **v0.9.0** | Q3 2026 | Plugin system prototype, multi-language AI, multi-hop chain |
| **v1.0.0** | Q4 2026 | Stable release, Tmux/session manager, Docker exec |
| **v1.1+** | 2027 | Fish shell, plugin marketplace, SSH config deep parser |

### 10.3 Current Branches

| Branch | Status | Description |
|--------|--------|-------------|
| `main` | ✅ Stable (v0.8.0) | Production-ready |
| `feat/ssh-escape-ai` | 🔄 Ready to merge | Connect feature (AI REPL) |
| `feat/versioning` | 🔄 In progress | Code refactor (3784→2323 lines), proper self-update, docs restructure |

---

## 11. Success Metrics

### 11.1 Product Metrics

| Metric | Target | Cara Ukur |
|--------|--------|-----------|
| **GitHub Stars** | >500 di 2027 | GitHub |
| **Downloads** | >1000 unique download | GitHub Releases count |
| **GitHub Issues** | <10 open bugs | GitHub |
| **PR merge time** | <7 hari | GitHub |
| **Release cadence** | 1 release / 2 bulan | GitHub Releases |

### 11.2 Quality Metrics

| Metric | Target |
|--------|--------|
| **CLI response time** | <200ms startup |
| **Error rate** | <1% dari total command |
| **CRITICAL bugs** | 0 di production |
| **Documentation coverage** | 100% fitur punya docs |
| **Code size** | <3000 lines untuk main script |

### 11.3 User Satisfaction

| Metric | Method |
|--------|--------|
| **Issue response time** | <24 jam |
| **Feature request adoption** | Track via GitHub Discussions |
| **User feedback** | GitHub Issues + direct feedback |

---

## 12. Open Questions & Risks

### 12.1 Open Questions

| # | Question | Decision Needed By |
|---|----------|-------------------|
| 1 | Apakah perlu binary distribution (PyInstaller) untuk user tanpa Python? | v1.0 |
| 2 | Apakah perlu package manager (Homebrew, apt) untuk distribusi? | v1.0 |
| 3 | Apakah plugin system perlu WASM atau cukup Python-based? | v0.9 planning |
| 4 | Bagaimana strategi monetisasi (jika ada)? Donation? Pro features? | TBD |
| 5 | Perlu GitHub Actions untuk automated testing? | Saat mulai TDD |

### 12.2 Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Python version fragmentation** | Medium | Medium | Target Python 3.7+, dokumentasi minimum version |
| **SSH key compatibility** | Medium | Low | Gunakan system SSH, user manage sendiri |
| **AI provider API changes** | High | Low | OpenAI-compatible API sudah de facto standard |
| **Single-file maintenance** | Medium | Medium | Refactor ke modular structure di v1.0 (feat/versioning) |
| **Competitor catches up** | Medium | Low | SSH-first + zero dep adalah moat yang kuat |

### 12.3 Product Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Low adoption** | High | Fokus ke DevOps niche yang butuh SSH + AI |
| **Feature bloat** | Medium | Ketat dengan product vision, jangan jadi "super tool" |
| **Dependency on third-party AI** | Medium | Promosiin Ollama untuk local AI, provider freedom |
| **Maintenance burden** | Medium | Keep code small, dokumentasi baik, automated testing |

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **CLI** | Command Line Interface |
| **SSH** | Secure Shell — protokol untuk remote server access |
| **SCP** | Secure Copy — file transfer via SSH |
| **ProxyJump** | SSH feature untuk koneksi lewat intermediate host (bastion) |
| **REPL** | Read-Eval-Print Loop — interactive command prompt |
| **RTK** | Rust Token Killer — tool kompresi output untuk AI |
| **Provider** | AI service (OpenAI, DeepSeek, Ollama, dll) |
| **Workflow** | Multi-step automation dalam YAML |
| **Fuzzy Match** | Partial string matching untuk server names |
| **PTY** | Pseudo-terminal — virtual terminal untuk process interaction |
| **Stdlib** | Python Standard Library |
| **Bastion Host** | Jump server untuk akses ke internal network |

---

*— End of PRD —*
