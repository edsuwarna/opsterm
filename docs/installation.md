# 📦 Installation

OpsTerm is a zero-dependency Python script — just Python 3 and a terminal.

## Prerequisites

- **Python 3.8+** (check with `python3 --version`)
- **Git** (for cloning)
- **Bash or Zsh** (shell integration)

## Quick Install (Linux / macOS)

No repo needed — download the single Python file and go:

```bash
# 1. Download the script (single file, zero deps)
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm

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

Set your API key — supports any OpenAI-compatible provider:

```bash
# Via env var (recommended)
export OPSTERM_API_KEY='sk-your-key'

# Via config file (~/.opsterm/config.yaml)
opsterm config set ai.api_key sk-your-key
```

Config file at `~/.opsterm/config.yaml`:

```yaml
ai:
  provider: opencode       # or: openai, deepseek, openrouter, ollama
  api_url: "https://opencode.ai/zen/go/v1/chat/completions"
  api_key: "sk-..."
  model: deepseek-v4-flash
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
| OpenCode | `https://opencode.ai/zen/go/v1/chat/completions` | `deepseek-v4-flash` |

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

```bash
# Single-file install — just re-download
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
```

Or if you installed via clone:

```bash
cd ~/opsterm && git pull && ./setup.sh
```

## Uninstall

```bash
# 1. Remove symlink and repo
rm ~/.local/bin/opsterm
rm -rf ~/opsterm

# 2. Remove config (⚠️ deletes all servers, workflows, vault, history)
rm -rf ~/.opsterm

# 3. Remove shell integration from ~/.bashrc or ~/.zshrc
#    Delete or comment out these lines:
#      source ~/opsterm/zsh/opsterm.plugin.zsh
#      source <(opsterm completion ...)
#      export OPSTERM_API_KEY="..."
#    Then: source ~/.bashrc
```

> 💡 Config is independent from the repo — removing `~/opsterm` won't delete your servers, workflows, or vault. You need to `rm -rf ~/.opsterm` separately to fully remove all data.
