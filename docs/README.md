# 📚 Dokumentasi OpsTerm

Selamat datang di dokumentasi OpsTerm! Di sini lu bakal paham gimana OpsTerm bekerja, teknologi yang dipake, dan kenapa dirancang seperti ini.

---

## 📖 Daftar Dokumen

| Dokumen | Deskripsi |
|---------|-----------|
| [📐 Arsitektur & System Design](architecture.md) | **Cara kerja OpsTerm** — alur dari user ngetik command sampai eksekusi |
| [🔧 Tech Stack](tech-stack.md) | **Teknologi yang dipake** — bahasa, library, protocol, format |
| [🤔 Design Decisions](design-decisions.md) | **Kenapa dirancang seperti ini** — alasan di balik setiap keputusan teknis |
| [🎯 Fitur Lengkap](features.md) | **Semua fitur** — daftar lengkap + contoh penggunaan + use case matrix |
| [📊 Architecture Diagram](ops-term-architecture.excalidraw) | **Diagram Excalidraw** — buka di [excalidraw.com](https://excalidraw.com) |
| [🖼️ Architecture Diagram (PNG)](ops-term-architecture.png) | **Diagram versi gambar** — langsung liat tanpa perlu buka excalidraw |

---

## 🚀 Quick Overview

```
┌─────────────────────────────────────────────────────┐
│                  USER LAPTOP                         │
│  ┌───────────────────────────────────────────────┐  │
│  │  $ ai ssh vps-utama                           │  │
│  │  $ ai "how to check disk"                     │  │
│  │  $ docker ps | ai "error?"                    │  │
│  └───────────────┬───────────────────────────────┘  │
│                  │                                   │
│  ┌───────────────▼───────────────────────────────┐  │
│  │           OpsTerm (bin/ai)                     │  │
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
│   └── ai                    ← Main script (single file, ~1500 baris)
├── completions/
│   ├── opsterm.bash          ← Bash tab completion
│   └── opsterm.zsh           ← Zsh tab completion
├── zsh/
│   └── opsterm.plugin.zsh    ← Zsh shell integration plugin
├── docs/                     ← Dokumentasi ini
│   ├── README.md             ← Index dokumentasi
│   ├── architecture.md       ← Arsitektur & system design
│   ├── tech-stack.md         ← Tech stack detail
│   ├── design-decisions.md   ← Design rationale
│   └── ops-term-architecture.excalidraw ← Diagram Excalidraw
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
2. **Single file** — `bin/ai` bisa dicopy ke server mana pun dan langsung jalan
3. **Local-first** — AI di terminal lokal, bukan di server. Bisa SSH tanpa kehilangan AI
4. **Config as code** — server & workflow config pake YAML, bisa di-version control
5. **Progressive disclosure** — fitur sederhana gampang dipake, fitur kompleks available kalo butuh

---

## 🎯 Recommended Reading Order

1. [📐 Arsitektur & System Design](architecture.md) — paham alur kerja
2. [🔧 Tech Stack](tech-stack.md) — teknologi yang dipake
3. [🤔 Design Decisions](design-decisions.md) — kenapa milih ini
4. [📊 Architecture Diagram](ops-term-architecture.excalidraw) — visual overview (buka di excalidraw.com)

---

Selanjutnya: [📐 Arsitektur & System Design →](architecture.md)
