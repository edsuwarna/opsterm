# 🛠️ Development

How to set up a development environment for OpsTerm and contribute.

## Prerequisites

- Python 3.8+
- Git
- A terminal emulator (for testing SSH/SCP features)

## Local Setup

```bash
git clone https://github.com/edsuwarna/opsterm.git
cd opsterm

# OpsTerm has zero pip dependencies — just Python stdlib
# Set up config for testing
mkdir -p ~/.ai-workflows
```

The main script is a single file: `bin/opsterm` (~1500 lines).

## Project Structure

```
opsterm/
├── bin/
│   └── opsterm              ← Main CLI (single file)
├── completions/
│   ├── opsterm.bash          ← Bash completion
│   └── opsterm.zsh           ← Zsh completion
├── zsh/
│   └── opsterm.plugin.zsh    ← Zsh integration plugin
├── docs/
│   ├── en/                   ← English docs (.md files)
│   ├── id/                   ← Indonesian docs (.md files)
│   ├── docs.html             ← SPA documentation viewer
│   └── index.html            ← Landing page
└── setup.sh                  ← Install script
```

## Running in Development

```bash
# Run directly (no install needed)
./bin/opsterm "hello"

# Or add to PATH temporarily
export PATH="$PWD/bin:$PATH"
opsterm "how to check memory"
```

## Code Style

- Single-file architecture — all logic in `bin/opsterm`
- Python stdlib only (zero external dependencies)
- Functions grouped by feature (ssh, scp, ai, servers, workflows, etc.)
- Error messages use emoji indicators for clarity

## Testing

```bash
# Manual test — AI query
./bin/opsterm "say hello"

# Manual test — SSH (needs a configured server)
./bin/opsterm ssh my-server "uptime"

# Manual test — pipe mode
echo "error: connection refused" | ./bin/opsterm "explain"
```

## Submitting Changes

1. Fork the repo on [GitHub](https://github.com/edsuwarna/opsterm)
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Test manually
5. Commit and push
6. Open a Pull Request

## Documentation Updates

Docs are in `docs/en/*.md` (English) and `docs/id/*.md` (Indonesian). When adding features:

1. Update the relevant `.md` files
2. Keep EN and ID in sync
3. The `docs.html` SPA loads `.md` files directly — no build step needed
