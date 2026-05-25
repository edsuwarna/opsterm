# 🛠️ Pengembangan

Setup environment development untuk OpsTerm.

## Prasyarat

- Python 3.8+
- Git

## Setup Lokal

```bash
git clone https://github.com/edsuwarna/opsterm.git
cd opsterm
```

## Struktur Project

```
opsterm/
├── bin/opsterm              ← Main CLI (single file)
├── completions/             ← Tab completion
├── zsh/                     ← Zsh plugin
└── docs/                    ← Dokumentasi
```

## Running di Development

```bash
./bin/opsterm "hello"
```

## Code Style

- Single-file architecture
- Python stdlib only (zero dependencies)
- Functions grouped by feature

## Testing

```bash
./bin/opsterm "say hello"
./bin/opsterm ssh my-server "uptime"
```

## Kontribusi

1. Fork repo di [GitHub](https://github.com/edsuwarna/opsterm)
2. Buat branch: `git checkout -b feat/my-feature`
3. Commit & Push
4. Open Pull Request
