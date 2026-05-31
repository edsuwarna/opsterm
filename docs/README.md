# 📚 OpsTerm Documentation

Welcome to the OpsTerm documentation! Here you'll understand how OpsTerm works, the technologies it uses, and why it's designed the way it is.

---

## 📖 Document Index

| Document | Description | Also available in |
|----------|-------------|-------------------|
| [📐 Architecture & System Design](architecture.md) | **How OpsTerm works** — the flow from user typing a command to execution | [🇮🇩 Bahasa Indonesia](../id/architecture.md) |
| [🔧 Tech Stack](tech-stack.md) | **Technologies used** — languages, libraries, protocols, formats | [🇮🇩 Bahasa Indonesia](../id/tech-stack.md) |
| [🤔 Design Decisions](design-decisions.md) | **Why it's designed this way** — rationale behind every technical decision | [🇮🇩 Bahasa Indonesia](../id/design-decisions.md) |
| [🎯 Features](features.md) | **All features** — complete list with usage examples and use-case matrix | [🇮🇩 Bahasa Indonesia](../id/features.md) |
| [📊 Architecture Diagram](../ops-term-architecture.excalidraw) | **Excalidraw diagram** — open at [excalidraw.com](https://excalidraw.com) | — |
| [🖼️ Architecture Diagram (PNG)](../ops-term-architecture.png) | **Image version** — view directly without opening Excalidraw | — |

---

## 🚀 Quick Overview

```
┌─────────────────────────────────────────────────────┐
│                  USER LAPTOP                         │
│  ┌───────────────────────────────────────────────┐  │
│  │  $ opsterm ssh vps-utama                           │  │
│  │  $ opsterm "how to check disk"                     │  │
│  │  $ docker ps | opsterm "error?"                    │  │
│  └───────────────┬───────────────────────────────┘  │
│                  │                                   │
│  ┌───────────────▼───────────────────────────────┐  │
│  │           OpsTerm (bin/opsterm)                     │  │
│  │  ┌─────────┐ ┌────────┐ ┌────────┐ ┌──────┐  │  │
│  │  │ AI      │ │ SSH    │ │ SCP    │ │       │  │  │
│  │  │ Client  │ │ Runner │ │ Transfer│ │      │  │  │
│  │  └────┬────┘ └───┬────┘ └───┬────┘ └──┬───┘  │  │
│  └───────┼──────────┼──────────┼─────────┼───────┘  │
│          │          │          │         │           │
└──────────┼──────────┼──────────┼─────────┼───────────┘
           │          │          │         │
     ┌─────▼──┐ ┌────▼───┐ ┌───▼────┐ ┌──▼────────┐
     │AI API  │ │SSH     │ │Server  │ │Local File  │
     │Provider│ │ Server │ │Filesys │ │System      │
     └────────┘ └────────┘ └────────┘ └────────────┘
```

**Core principle:** OpsTerm runs on your **local laptop**. The AI lives in your terminal, not on the remote server. So when you SSH into any server, the AI is still available.

---

## 📁 Project Structure

```
~/opsterm/
├── bin/
│   └── opsterm                    ← Main script (single file, ~1500 lines)
├── completions/
│   ├── opsterm.bash          ← Bash tab completion
│   └── opsterm.zsh           ← Zsh tab completion
├── zsh/
│   └── opsterm.plugin.zsh    ← Zsh shell integration plugin
├── docs/                     ← This documentation
│   ├── README.md             ← Index
│   ├── architecture.md       ← Architecture & system design
│   ├── tech-stack.md         ← Tech stack details
│   ├── design-decisions.md   ← Design rationale
│   ├── features.md           ← All features
│   ├── installation.md       ← Installation guide
│   ├── configuration.md      ← Configuration reference
│   ├── usage-guide.md        ← Usage examples
│   ├── quick-start.md        ← Quick start
│   ├── development.md        ← Contributing
│   ├── security.md           ← Security notes
│   ├── troubleshooting.md    ← Common issues
│   ├── index.html            ← Web landing page
│   ├── docs.html             ← Web documentation viewer
│   ├── ops-term-architecture.excalidraw ← Excalidraw diagram
│   └── ops-term-architecture.png        ← PNG architecture diagram
├── setup.sh                  ← Install script
├── README.md                 ← English README
├── README.id.md              ← Indonesian README
└── .gitignore
```

**User config** (gitignored, stored at `~/.opsterm/`):
```
~/.opsterm/
├── config.yaml       ← AI provider settings
├── servers.yaml      ← Server list + proxy config
├── workflows.yaml    ← Workflow definitions

├── history.db        ← SQLite history
└── last_*.txt        ← Last command output
```

> 📦 Changed from `~/.ai-workflows` → `~/.opsterm/` (auto-migrates on first run)

---

## 🧠 Design Philosophy

1. **Zero dependencies** — just Python 3 stdlib, no `pip install` needed
2. **Single file** — `bin/opsterm` can be copied to any server and run immediately
3. **Local-first** — AI runs on your local terminal, not on the server. SSH without losing AI access
4. **Config as code** — server & workflow configs use YAML, version-control friendly
5. **Progressive disclosure** — simple features are easy to use, complex features are available when needed

---

## 🎯 Recommended Reading Order

1. [📐 Architecture & System Design](architecture.md) — understand the workflow flow
2. [🔧 Tech Stack](tech-stack.md) — technologies used
3. [🤔 Design Decisions](design-decisions.md) — why these choices were made
4. [📊 Architecture Diagram](../ops-term-architecture.excalidraw) — visual overview (open at excalidraw.com)

---

Next: [📐 Architecture & System Design →](architecture.md)
