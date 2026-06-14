# Installation

OpsTerm is a zero-dependency Python script — just Python 3 and a terminal.

## Prerequisites

- **Python 3.8+** (check with `python3 --version`)
- **Git** (for cloning)
- **Bash or Zsh** (shell integration)

## Quick Install (Linux / macOS)

No repo needed — download the single Python file and go:

```bash
# 1. Download the script (single file, zero deps)
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/LATEST -o /tmp/opsterm_latest
OPSTERM_VER=$(cat /tmp/opsterm_latest)
curl -L "https://raw.githubusercontent.com/edsuwarna/opsterm/${OPSTERM_VER}/bin/opsterm" -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
rm -f /tmp/opsterm_latest

# 2. Init config
opsterm init

# 3. Set API key
export OPSTERM_API_KEY='sk-...'

# 4. Tab completion (bash)
echo 'source <(opsterm completion bash)' >> ~/.bashrc
source ~/.bashrc

# 5. Try it
opsterm --help
```

> 💡 Make sure `~/.local/bin` is in your `PATH`. If not, add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc` or `~/.zshrc`.

### macOS Notes
- Python 3 ships with macOS Ventura (13.0+) and newer
- If missing: `brew install python@3`
- macOS defaults to Zsh — tab completion: `opsterm completion zsh`

## Clone Install (with shell plugin)

For the Zsh plugin (`opsterm last`, `opsterm explain-last`) or to browse the full source:

```bash
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm && ./setup.sh
echo 'source ~/opsterm/zsh/opsterm.plugin.zsh' >> ~/.zshrc
```

## Post-Install: Configure AI Provider

### Add AI Provider

```bash
# Smart interactive — just enter API key, pick provider, choose model
opsterm provider add

# The tool will:
#   1. Ask for API key
#   2. Show known providers (OpenAI, OpenCode, DeepSeek, OpenRouter, Groq, etc.)
#   3. Auto-fill the correct API URL
#   4. Fetch available models from the provider
#   5. Let you pick a model from the list

# Or one-liner with flags
opsterm provider add default --api-key 'sk-...' --model gpt-4o

# Set as default
opsterm provider default default

# List configured providers
opsterm provider list
```

Config file at `~/.opsterm/config.yaml`:

```yaml
default_provider: default
providers:
  default:
    api_key: "sk-..."
    api_url: "https://api.deepseek.com/v1/chat/completions"
    model: "deepseek-chat"

ai:
  temperature: 0.3
  max_tokens: 1024
```

### Supported Providers

| Provider | API URL | Model |
|----------|---------|-------|
| OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-4o`, `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/v1/chat/completions` | `deepseek-chat`, `deepseek-coder` |
| OpenRouter | `https://openrouter.ai/api/v1/chat/completions` | `anthropic/claude-sonnet-4` |
| Ollama (local) | `http://localhost:11434/v1/chat/completions` | `llama3`, `qwen2.5` |
|| OpenCode Zen | `https://opencode.ai/zen/v1/chat/completions` | `deepseek-v4-flash` (curated) |
|| OpenCode Go | `https://opencode.ai/zen/v1/chat/completions` | `deepseek-v4-flash` (subscription) |

## Verify Installation

```bash
opsterm --help
# → Shows usage with all subcommands

# Test AI (if API key is set)
opsterm "hello from opsterm"
```

## Shell Integration (Optional)

For the best experience, enable the Zsh plugin:

```bash
# ~/.zshrc
source ~/opsterm/zsh/opsterm.plugin.zsh
```

This adds:
- `opsterm last` — view last command output
- `opsterm explain-last` — explain last output with AI
- Auto-save of command output for AI analysis

## Updating

### Single-file install

```bash
# Re-download the script
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/LATEST -o /tmp/opsterm_latest
OPSTERM_VER=$(cat /tmp/opsterm_latest)
curl -L "https://raw.githubusercontent.com/edsuwarna/opsterm/${OPSTERM_VER}/bin/opsterm" -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
rm -f /tmp/opsterm_latest

# Check for new features
opsterm --help
```

### Clone install

```bash
cd ~/opsterm && git pull && ./setup.sh
```

### Post-update

After updating, check if there are new subcommands or config options:

```bash
# List all commands
opsterm --help

# Migrate config if needed (adds new default sections)
opsterm init --force

# Check current provider
opsterm provider list
```

> 💡 **Tip:** `opsterm init --force` will regenerate your config without overwriting existing servers, workflows, or providers. Run it after updates to get new config defaults.

## Uninstall

```bash
# 1. Remove symlink and repo
rm ~/.local/bin/opsterm
rm -rf ~/opsterm

# 2. Remove config (⚠️ deletes all servers, workflows, history)
rm -rf ~/.opsterm

# 3. Remove shell integration from ~/.bashrc or ~/.zshrc
#    Delete or comment out these lines:
#      source ~/opsterm/zsh/opsterm.plugin.zsh
#      source <(opsterm completion ...)
#      export OPSTERM_API_KEY="..."
#    Then: source ~/.bashrc
```

> 💡 Config is independent from the repo — removing `~/opsterm` won't delete your servers or workflows. You need to `rm -rf ~/.opsterm` separately to fully remove all data.
