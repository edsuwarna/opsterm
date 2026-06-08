# OpsTerm — Product Requirements Document

> **Version:** 1.0
> **Status:** Final Draft
> **Date:** June 2026
> **Author:** Endang Suwarna

---

## Table of Contents

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

OpsTerm is an **AI Terminal Assistant** CLI tool that lets developers and sysadmins interact with AI directly from their terminal — no installation required beyond a single Python file.

**Core value proposition:**
- **Zero dependency** — pure Python 3 stdlib, one `opsterm` file, runs immediately
- **Any AI provider** — free to choose AI providers (DeepSeek, OpenAI, Ollama, OpenRouter, etc.)
- **SSH-first** — all SSH features built-in, including multi-hop ProxyJump, SCP, and SSH Escape
- **Workflow automation** — multi-step automation (SSH/SCP/local) via YAML
- **Lightweight** — ~50KB file, no node_modules, no pip install, no 200MB+ binaries

**Current stage:** v0.8.0 — core features are mature (AI Chat, Smart SSH, SCP, Workflow, Web Dashboard, Connect, SSH Escape). Some advanced features remain in separate branches.

---

## 2. Product Overview

### 2.1 Product Vision

> "A terminal AI assistant that works anywhere — any server, any AI provider — with zero complex setup."

### 2.2 Positioning

OpsTerm is a **free, open-source, provider-agnostic alternative to Warp.dev** for Linux — with additional SSH automation and workflow capabilities that competitors lack.

### 2.3 Core Philosophy

1. **Local-first** — AI runs on your local terminal, not on remote servers
2. **Zero friction** — download one file, run it. No `pip install`, no `npm i`
3. **Provider freedom** — no lock-in to a single AI vendor
4. **SSH native** — not an afterthought, SSH is a first-class citizen
5. **Transparent** — all code is readable, zero hidden dependencies

---

## 3. Target Audience & User Personas

### Persona 1: DevOps / Sysadmin (Primary)

| Attribute | Description |
|-----------|-------------|
| **Role** | DevOps Engineer, System Administrator, SRE |
| **Tools** | Terminal, SSH, Docker, Kubernetes, Ansible |
| **Pain points** | Memorizing server IPs, SSH-ing into many servers, troubleshooting errors |
| **Needs** | Quick command execution across servers, error debugging assistance, workflow automation |
| **OpsTerm appeal** | Smart SSH, Multi-hop, Workflow automation, AI-assisted troubleshooting |

### Persona 2: Full-stack Developer (Secondary)

| Attribute | Description |
|-----------|-------------|
| **Role** | Software Engineer, Full-stack Developer |
| **Tools** | Terminal, Git, Docker, VS Code |
| **Pain points** | Forgets Linux commands, needs quick help without switching to browser |
| **Needs** | AI chat in terminal, command generation, error explanation |
| **OpsTerm appeal** | AI Chat, Pipe Mode, Explain-last, zero setup |

### Persona 3: Homelab / Self-hoster (Tertiary)

| Attribute | Description |
|-----------|-------------|
| **Role** | Hobbyist, Self-hoster, Tech enthusiast |
| **Tools** | Terminal, Docker, Proxmox, budget VPS |
| **Pain points** | Many small servers, needs simple tools without overhead |
| **Needs** | Manage multiple servers without bloat, simple deployment workflows |
| **OpsTerm appeal** | Lightweight (~50KB), zero dependency, workflow automation, SCP |

---

## 4. Problem Statement

### 4.1 Core Problems

| # | Problem | Impact | OpsTerm Solution |
|---|---------|--------|------------------|
| 1 | Developers must switch context to browser to ask AI | Lost productivity, broken flow | AI directly in terminal |
| 2 | SSH to many servers = memorizing IPs and configs | High mental load, human error | Smart SSH (fuzzy match, YAML config) |
| 3 | Internal servers only accessible through jump hosts | SSH commands become long and complex | Built-in multi-hop SSH (`--via`) |
| 4 | Troubleshooting requires manual copy-paste to ChatGPT | Slow, impractical | Pipe mode + explain-last + RTK |
| 5 | AI provider vendor lock-in | Can't switch without changing tools | Provider-agnostic (OpenAI-compatible) |
| 6 | AI terminal tools are heavy with many dependencies | Complex setup, unsuitable for minimal servers | Zero dependency, single 50KB file |
| 7 | Repetitive automation tasks (deploy, health check) done manually | Repetitive, error-prone | Workflow automation via YAML |

### 4.2 Use Case Matrix

| Scenario | Before | With OpsTerm |
|----------|--------|--------------|
| Find a Linux command | Open browser → Google → Stack Overflow | `opsterm how to check disk usage` |
| SSH into a server | `ssh ubuntu@203.0.113.10 -i key.pem` | `opsterm ssh vps-utama` |
| SSH through bastion | `ssh -J user@bastion user@internal` | `opsterm ssh internal --via bastion` |
| Upload file to server | `scp file user@203.0.113.10:/path/` | `opsterm scp file.txt vps-utama:/path/` |
| Diagnose errors from logs | Copy log → open ChatGPT → paste → wait | `docker logs -n50 \| opsterm "any errors?"` |
| Deploy app with multiple steps | Open tmux → SSH → git pull → docker compose | `opsterm run deploy-app` |
| Check health of all servers | SSH one-by-one to each server | `opsterm run health-check` |

---

## 5. Feature Specification

### 5.1 Feature Taxonomy

Features are grouped into 5 categories:

```
CORE        — AI + SSH + SCP + Workflow (must-have)
SHELL       — Shell integration (Zsh plugin, explain-last)
MANAGEMENT  — CRUD servers, workflows, config, history
UTILITY     — Dashboard, completion, export/import, diagnostics
SETUP       — Init, provider config, import SSH config
```

### 5.2 Current Features (v0.8.0)

#### 5.2.1 Core Features

| Feature | Command | Priority | Status |
|---------|---------|----------|--------|
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

| Feature | Command | Priority | Status |
|---------|---------|----------|--------|
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

| Feature | Command | Priority | Status |
|---------|---------|----------|--------|
| Web Dashboard | `opsterm web [--port] [--open]` | P1 | ✅ Live |
| Tab Completion (bash/zsh) | `opsterm completion bash\|zsh` | P1 | ✅ Live |
| JSON Output | `--json` flag on list commands | P2 | ✅ Live |
| Diagnostics | `opsterm doctor` | P1 | ✅ Live |
| Self-Update | `opsterm update` | P1 | ✅ Live |
| Init | `opsterm init` | P1 | ✅ Live |
| Zsh Plugin | Shell hooks (preexec/precmd) | P1 | ✅ Live |
| Custom System Prompt | `opsterm config set ai.system_prompt` | P2 | ✅ Live |

### 5.3 Future Features (Planned)

| Feature | Priority | Target | Description |
|---------|----------|--------|-------------|
| Plugin System | P2 | v0.9+ | Plugin/extensions system for third-party integrations |
| Multi-language AI Responses | P2 | v0.9+ | AI responds in the same language as the query |
| Tmux/Screen Session Manager | P2 | v1.0 | Manage multi-sessions from OpsTerm |
| Docker Exec Shortcut | P2 | v1.0 | `opsterm exec <container>` to jump directly into a container |
| SSH Config Parser | P2 | v1.0 | Advanced `~/.ssh/config` parsing |
| Fish Shell Support | P3 | v1.0+ | Completion & plugin for Fish shell |
| Multi-hop Chain | P1 | Backlog | `opsterm ssh server --via jump1,jump2` |

### 5.4 Feature Detail: Core Features

#### 5.4.1 AI Chat

**Behavior:**
- Input without a subcommand → automatically enters AI Chat mode
- Sends prompt + system message to AI provider (OpenAI-compatible)
- Detects if output contains a command (starting with `$`) → offers auto-execution
- Saves all interactions to SQLite history

**Edge cases:**
- **No API key configured:** Display friendly error with setup instructions
- **Provider timeout:** 30-second timeout, show error with retry suggestion
- **Very long output:** Truncate display at 2000 chars, still store full output in DB
- **Network error:** Retry 2x, then fall back to a clear error message

#### 5.4.2 Smart SSH

**Behavior:**
- Fuzzy match server name from servers.yaml
- Resolve server config (host, user, port, key, proxy)
- Multi-hop via `-J` (ProxyJump) flag
- For interactive SSH: `os.execvp()` → replaces the process
- For command-based SSH (workflow): `subprocess.run()`

**Edge cases:**
- **Server not found:** Fuzzy match to nearest name + suggestion, or clear error
- **Server name ambiguous:** Show list of matching servers, prompt user to choose
- **Connection timeout:** 10-second timeout, display appropriate error
- **Key file not found:** Fall back to default keys (~/.ssh/id_rsa, id_ed25519)
- **Proxy unreachable:** Clear error that the proxy server is the issue, not the target

#### 5.4.3 SSH Escape Mode (`Ctrl+B`)

**Behavior:**
- During an active SSH session, `Ctrl+B` intercepts input and drops into AI prompt
- Natural language → AI detects if a command is needed → executes via second SSH → explains
- `!<command>` → runs directly without AI processing
- `resume` → returns to the SSH session
- `exit` → terminates the SSH session
- Can be disabled via config: `opsterm config set ssh.escape_key_enabled false`

**Technical:**
- Uses pseudo-terminal (PTY) to intercept input
- Opens a second SSH connection from local machine for command execution
- Disables key echo to PTY during escape mode

#### 5.4.4 Workflow Automation

**Behavior:**
- Step types: `ssh`, `command`, `scp`, `confirm`, `wait`
- Sequential execution: step fails → workflow stops with error
- Each step's output is displayed in real-time

**Edge cases:**
- **Empty workflow:** Error message, no crash
- **Server in step not found:** Error at that step, stop workflow
- **SCP to nonexistent path:** SCP error displayed, workflow stops
- **`confirm` step in non-interactive mode:** Auto-skip with warning

#### 5.4.5 RTK Token Compression

**Behavior:**
- Automatically compresses command output before sending to AI
- Threshold: skip compression for output <200 chars
- Auto-detect output type (git diff, pytest, docker ps, logs, journalctl)
- Graceful fallback if RTK binary is not installed

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

Key architectural decisions already made (full details in `docs/design-decisions.md`):

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | **Language** | Python 3 | Present on every Linux/macOS, full stdlib |
| 2 | **Architecture** | Single-file CLI | Portable, zero setup, easy to audit |
| 3 | **Dependencies** | Zero (stdlib only) | No pip install, no version conflicts |
| 4 | **Config format** | YAML | Human-readable, ideal for config files |
| 5 | **AI Protocol** | OpenAI-compatible API | Universal, supported by most providers |
| 6 | **SSH Method** | Subprocess + system SSH | Zero dep, supports all SSH features |
| 7 | **State** | File-based (no daemon) | Simple, no service management needed |

---

## 7. Non-Functional Requirements

### 7.1 Performance

| Requirement | Target | Notes |
|-------------|--------|-------|
| Startup time | <200ms | From command exec to ready |
| AI response time | Provider-dependent | OpsTerm adds <50ms overhead |
| SSH connect | <5s | Default timeout 10s |
| RTK compression | <1s | Even for 50KB+ output |
| Config load | <50ms | Minimal YAML parsing |
| Web dashboard startup | <2s | Python HTTP server |
| Memory usage | <30MB | Peak during AI request |
| Disk usage | <1MB | Binary + DB + config |

### 7.2 Security

| Requirement | Implementation |
|-------------|----------------|
| **API key storage** | File-based (`~/.opsterm/config.yaml`) with `chmod 600` |
| **Alternative** | Environment variable `OPSTERM_API_KEY` |
| **Export** | API keys masked in exported tar.gz |
| **SSH keys** | Uses existing system SSH keys |
| **No remote agent** | Nothing installed on remote servers |
| **Config encryption** | Optional via `cryptography` library |
| **Input sanitization** | All user input escaped for shell |

### 7.3 Reliability

| Requirement | Target |
|-------------|--------|
| Uptime | N/A (CLI tool, no daemon) |
| Error handling | All errors have user-friendly messages |
| Graceful degradation | RTK not installed → runs normally, no errors |
| Network timeout | 30s for AI, 10s for SSH |
| Config fallback | Corrupted YAML → fallback to defaults + warning |

### 7.4 Compatibility

| Platform | Status |
|----------|--------|
| **Linux** | ✅ Primary target |
| **macOS** | ✅ Tested and supported |
| **Windows (WSL)** | ⚠️ Community-supported, not officially tested |
| **Shell bash** | ✅ Completion available |
| **Shell zsh** | ✅ Completion + plugin available |
| **Shell fish** | ❌ Not yet supported |

### 7.5 Maintainability

| Requirement | Target |
|-------------|--------|
| **Code size** | <4000 lines (feat/versioning target: ~2300) |
| **Documentation** | docs/ folder with 15+ documents |
| **Test coverage** | No automated tests yet — target TDD adoption in future |
| **Release process** | Git tag → GitHub Release → single file distribution |

---

## 8. User Experience

### 8.1 User Flow: First-time Setup

```
User downloads opsterm
    │
    ▼
opsterm init → creates ~/.opsterm/ with default config
    │
    ▼
opsterm provider add default --api-key <key> --model <model>
    │
    ▼
opsterm doctor → verifies everything is OK
    │
    ▼
opsterm servers add → add first server
    │
    ▼
Ready to use!
```

**Target time-to-value:** <5 minutes from download to SSH with AI.

### 8.2 User Flow: Daily Use

```
# Morning check
opsterm run health-check

# SSH + troubleshoot
opsterm ssh vps-utama
    └─ Ctrl+B → AI Escape Mode
        ├─ "check disk usage"
        └─ resume

# Deploy
opsterm run deploy-app

# Quick question
opsterm how to check which ports are listening
```

### 8.3 UX Principles

1. **Zero surprise** — Every command produces predictable output
2. **Fuzzy everything** — Server names, commands, workflows — all fuzzy-matched
3. **Fail gracefully** — Actionable error messages, not stack traces
4. **Progressive disclosure** — Basic features are simple, advanced features exist but aren't required
5. **Keyboard-first** — All interactions from keyboard, no mouse needed
6. **Dark theme by default** — Web dashboard is dark-themed, terminal is natural

### 8.4 CLI Design Conventions

| Convention | Example |
|------------|---------|
| `opsterm <verb> <object>` | `opsterm ssh server`, `opsterm run workflow` |
| `opsterm <object> <verb>` | `opsterm servers list`, `opsterm servers add` |
| `--flag` for options | `--via`, `--port`, `--json` |
| `\--` for long flags | `--all`, `--continue`, `--open` |
| Single char flags | Only common ones: `-v` (verbose) |

---

## 9. Competitive Analysis

### 9.1 Direct Competitors

| Aspect | OpsTerm | Warp.dev | Shell-GPT (sgpt) | Claude Code |
|--------|---------|----------|-------------------|-------------|
| **Platform** | Linux + macOS | macOS only | Linux + macOS | Linux + macOS |
| **Dependencies** | ✅ Zero | ❌ Binary ~200MB | ⚠️ pip + many | ❌ Binary ~500MB+ |
| **Custom AI Provider** | ✅ Any provider | ❌ Vendor lock (Warp AI) | ✅ Many providers | ❌ Claude only |
| **SSH** | ✅ Smart SSH + multi-hop | ❌ No | ❌ No | ❌ No |
| **SCP** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Workflows** | ✅ Multi-step YAML | ❌ No | ❌ No | ❌ No |
| **SSH Escape Mode** | ✅ Ctrl+B | ✅ Warp AI (macOS only) | ❌ No | ❌ No |
| **Tab Completion** | ✅ bash + zsh | ✅ built-in | ❌ No | ❌ No |
| **File size** | ~50KB | ~200MB+ | ~10MB | ~500MB+ |
| **Price** | Free (your own API key) | Free tier limited, Pro $20/mo | Free + OpenAI cost | $20/mo bundled |
| **Open Source** | ✅ Yes | ❌ Proprietary | ✅ Yes | ❌ Proprietary |

### 9.2 Indirect Competitors

| Tool | Strengths | Weaknesses vs OpsTerm |
|------|-----------|----------------------|
| **Tabby (Eugeny/tabby)** | Terminal emulator + AI | Heavy (Electron), Windows-focused, no workflow |
| **Warp** | Great UI, native macOS | macOS only, vendor lock-in AI |
| **Fig** | Advanced autocomplete | macOS only, acquired, no SSH features |
| **iTerm2 + AI plugins** | Mature terminal emulator | macOS only, fragmented plugin ecosystem |
| **tmux + scripts** | Powerful, self-contained | No AI, manual scripting |

### 9.3 OpsTerm's Competitive Advantage

1. **SSH + AI combo** — No competitor offers Smart SSH + AI directly in the terminal
2. **Zero dependency** — One Python file, runs immediately — unique selling point
3. **Multi-hop SSH built-in** — DevOps daily necessity, no competitor supports this
4. **Workflow automation** — YAML-based multi-step automation, a simpler alternative to Ansible
5. **Provider freedom** — Switch AI providers anytime without changing tools

---

## 10. Roadmap & Milestones

### 10.1 Version History

| Version | Date | Highlights |
|---------|------|------------|
| v0.1.0 | — | Project initialization |
| v0.2.0 | — | AI Chat, Smart SSH |
| v0.3.0 | — | SCP, basic Workflow |
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

| Metric | Target | Measurement |
|--------|--------|-------------|
| **GitHub Stars** | >500 by 2027 | GitHub |
| **Downloads** | >1000 unique downloads | GitHub Releases count |
| **GitHub Issues** | <10 open bugs | GitHub |
| **PR merge time** | <7 days | GitHub |
| **Release cadence** | 1 release / 2 months | GitHub Releases |

### 11.2 Quality Metrics

| Metric | Target |
|--------|--------|
| **CLI response time** | <200ms startup |
| **Error rate** | <1% of total commands |
| **CRITICAL bugs** | 0 in production |
| **Documentation coverage** | 100% of features have docs |
| **Code size** | <3000 lines for main script |

### 11.3 User Satisfaction

| Metric | Method |
|--------|--------|
| **Issue response time** | <24 hours |
| **Feature request adoption** | Track via GitHub Discussions |
| **User feedback** | GitHub Issues + direct feedback |

---

## 12. Open Questions & Risks

### 12.1 Open Questions

| # | Question | Decision Needed By |
|---|----------|-------------------|
| 1 | Should we provide binary distribution (PyInstaller) for users without Python? | v1.0 |
| 2 | Should we support package managers (Homebrew, apt) for distribution? | v1.0 |
| 3 | Should the plugin system use WASM or be Python-based? | v0.9 planning |
| 4 | What is the monetization strategy (if any)? Donation? Pro features? | TBD |
| 5 | Do we need GitHub Actions for automated testing? | When TDD starts |

### 12.2 Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Python version fragmentation** | Medium | Medium | Target Python 3.7+, document minimum version |
| **SSH key compatibility** | Medium | Low | Use system SSH, user manages their own keys |
| **AI provider API changes** | High | Low | OpenAI-compatible API is the de facto standard |
| **Single-file maintenance** | Medium | Medium | Refactor to modular structure at v1.0 (feat/versioning) |
| **Competitor catches up** | Medium | Low | SSH-first + zero dep is a strong moat |

### 12.3 Product Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Low adoption** | High | Focus on DevOps niche that needs SSH + AI |
| **Feature bloat** | Medium | Stay disciplined with product vision, don't become a "super tool" |
| **Dependency on third-party AI** | Medium | Promote Ollama for local AI, provider freedom |
| **Maintenance burden** | Medium | Keep code small, good documentation, automated testing |

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **CLI** | Command Line Interface |
| **SSH** | Secure Shell — protocol for remote server access |
| **SCP** | Secure Copy — file transfer over SSH |
| **ProxyJump** | SSH feature for connecting through an intermediate host (bastion) |
| **REPL** | Read-Eval-Print Loop — interactive command prompt |
| **RTK** | Rust Token Killer — output compression tool for AI |
| **Provider** | AI service (OpenAI, DeepSeek, Ollama, etc.) |
| **Workflow** | Multi-step automation defined in YAML |
| **Fuzzy Match** | Partial string matching for server names |
| **PTY** | Pseudo-terminal — virtual terminal for process interaction |
| **Stdlib** | Python Standard Library |
| **Bastion Host** | Jump server for accessing an internal network |

---

*— End of PRD —*
