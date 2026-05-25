# 📦 Instalasi

OpsTerm adalah Python script zero-dependency — cukup Python 3 dan terminal.

## Prasyarat

- **Python 3.8+** (cek dengan `python3 --version`)
- **Git** (untuk clone)
- **Zsh atau Bash** (shell integration)

## Method 1: Git Clone (Rekomendasi)

```bash
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm
```

Tambah ke shell config:

```bash
# ~/.bashrc atau ~/.zshrc
export PATH="$HOME/opsterm/bin:$PATH"

# Zsh plugin (opsional)
source "$HOME/opsterm/zsh/opsterm.plugin.zsh"
```

## Method 2: Single File

```bash
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
```

## Setup AI Provider

Buat `~/.ai-workflows/config.yaml`:

```yaml
provider: openai
api_key: sk-xxx
model: gpt-4o
```

## Verifikasi

```bash
opsterm --version
```

## Shell Integration (Opsional)

```bash
# ~/.zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh
```
