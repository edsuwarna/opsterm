# 📚 Dokumentasi OpsTerm

Selamat datang di dokumentasi OpsTerm! Di sini lu bakal paham gimana OpsTerm bekerja, teknologi yang dipake, dan kenapa dirancang seperti ini.

---

## 📖 Daftar Dokumen

| Dokumen | Deskripsi | Juga tersedia dalam |
|---------|-----------|---------------------|
| [📐 Arsitektur & System Design](architecture.md) | **Cara kerja OpsTerm** — alur dari user ngetik command sampai eksekusi | [🇬🇧 English](../en/architecture.md) |
| [🔧 Tech Stack](tech-stack.md) | **Teknologi yang dipake** — bahasa, library, protocol, format | [🇬🇧 English](../en/tech-stack.md) |
| [🤔 Design Decisions](design-decisions.md) | **Kenapa dirancang seperti ini** — alasan di balik setiap keputusan teknis | [🇬🇧 English](../en/design-decisions.md) |
| [🎯 Fitur Lengkap](features.md) | **Semua fitur** — daftar lengkap + contoh penggunaan + use case matrix | [🇬🇧 English](../en/features.md) |
| [📊 Architecture Diagram](../ops-term-architecture.excalidraw) | **Diagram Excalidraw** — buka di [excalidraw.com](https://excalidraw.com) | — |
| [🖼️ Architecture Diagram (PNG)](../ops-term-architecture.png) | **Diagram versi gambar** — langsung liat | — |

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
│  │  │ AI      │ │ SSH    │ │ SCP    │ │Vault │  │  │
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

**Prinsip utama:** OpsTerm jalan di **laptop lokal**. AI-nya nempel di terminal, bukan di server remote. Jadi pas SSH ke server mana pun, AI tetep bisa dipake.

---

## 📁 Struktur Project

```
~/opsterm/
├── bin/
│   └── opsterm                    ← Main script (single file, ~1500 baris)
├── completions/
│   ├── opsterm.bash          ← Bash tab completion
│   └── opsterm.zsh           ← Zsh tab completion
├── zsh/
│   └── opsterm.plugin.zsh    ← Zsh shell integration plugin
├── docs/                     ← Dokumentasi ini
│   ├── en/                   ← Dokumentasi English
│   │   ├── README.md         ← Index
│   │   ├── architecture.md   ← Architecture & system design
│   │   ├── tech-stack.md     ← Tech stack details
│   │   ├── design-decisions.md← Design rationale
│   │   └── features.md       ← All features
│   ├── id/                   ← Dokumentasi Indonesia
│   │   ├── README.md         ← Index
│   │   ├── architecture.md   ← Arsitektur & system design
│   │   ├── tech-stack.md     ← Tech stack
│   │   ├── design-decisions.md← Design decisions
│   │   └── features.md       ← Fitur lengkap
│   ├── ops-term-architecture.excalidraw ← Diagram Excalidraw
│   └── ops-term-architecture.png        ← Diagram versi gambar
├── setup.sh                  ← Install script
├── README.md                 ← English README
├── README.id.md              ← Indonesian README
└── .gitignore
```

**Config user** (gitignored, di ~/.ai-workflows/):
```
~/.ai-workflows/
├── config.yaml       ← AI provider settings
├── servers.yaml      ← Daftar server + proxy
├── workflows.yaml    ← Daftar workflow
├── vault.json        ← Credential terenkripsi
├── history.db        ← Riwayat SQLite
└── last_*.txt        ← Output command terakhir
```

---

## 🧠 Filosofi Design

1. **Zero dependencies** — cukup Python 3 stdlib, ga perlu `pip install` apa-apa (kecuali vault)
2. **Single file** — `bin/opsterm` bisa dicopy ke server mana pun dan langsung jalan
3. **Local-first** — AI di terminal lokal, bukan di server. Bisa SSH tanpa kehilangan AI
4. **Config as code** — server & workflow config pake YAML, bisa di-version control
5. **Progressive disclosure** — fitur sederhana gampang dipake, fitur kompleks available kalo butuh

---

## 🎯 Recommended Reading Order

1. [📐 Arsitektur & System Design](architecture.md) — paham alur kerja
2. [🔧 Tech Stack](tech-stack.md) — teknologi yang dipake
3. [🤔 Design Decisions](design-decisions.md) — kenapa milih ini
4. [📊 Architecture Diagram](../ops-term-architecture.excalidraw) — visual overview (buka di excalidraw.com)

---

Selanjutnya: [📐 Arsitektur & System Design →](architecture.md)
