# 📦 Installation

OpsTerm is a zero-dependency Python script — just Python 3 and a terminal.

## Prerequisites

- **Python 3.8+** (check with `python3 --version`)
- **Git** (for cloning)
- **Zsh or Bash** (shell integration)

## Method 1: Git Clone (Recommended)

```bash
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm
```

Add to your shell config:

```bash
# ~/.bashrc or ~/.zshrc
export PATH="$HOME/opsterm/bin:$PATH"

# Zsh plugin (optional)
source "$HOME/opsterm/zsh/opsterm.plugin.zsh"
```

## Method 2: Single File Install

If you just want the binary without the full repo:

```bash
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
```

## Method 3: Docker (Experimental)

```bash
docker run --rm -it \
  -v ~/.ai-workflows:/root/.ai-workflows \
  -v ~/.ssh:/root/.ssh:ro \
  ghcr.io/edsuwarna/opsterm:latest \
  "check disk space"
```

## Post-Install: Setup AI Provider

Create `~/.ai-workflows/config.yaml`:

```yaml
provider: openai     # or: anthropic, deepseek, openrouter
api_key: sk-xxx     # your API key
model: gpt-4o        # or: claude-sonnet-4, deepseek-chat
```

## Verify Installation

```bash
opsterm --version
# Should output something like: OpsTerm v0.x.x
```

## Shell Integration (Optional)

For the best experience, enable the Zsh plugin:

```bash
# ~/.zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh
```

This adds:
- `opsterm-explain-last` — explain the last command output
- `opsterm-last` — re-run last command with AI
- Tab completion for servers

## Updating

```bash
cd ~/opsterm && git pull
```

Or if you installed via single file:

```bash
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
```
