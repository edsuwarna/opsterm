# 📦 Installation

OpsTerm is a zero-dependency Python script — just Python 3 and a terminal.

## Prerequisites

- **Python 3.8+** (check with `python3 --version`)
- **Git** (for cloning)
- **Bash or Zsh** (shell integration)

## Quick Install (Linux / macOS)

```bash
# 1. Clone repo
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm

# 2. Run setup (creates symlink + inits config)
./setup.sh

# 3. Set API key
export OPSTERM_API_KEY='sk-...'

# 4. Tab completion (bash)
echo 'source <(opsterm completion bash)' >> ~/.bashrc
source ~/.bashrc

# 5. Zsh plugin (optional — explain-last, last)
echo 'source ~/opsterm/zsh/opsterm.plugin.zsh' >> ~/.zshrc

# 6. Try it
opsterm --help
```

### macOS Notes
- Python 3 ships with macOS Ventura (13.0+) and newer
- If missing: `brew install python@3`
- macOS defaults to Zsh — tab completion: `opsterm completion zsh`

## Single-File Install (no repo)

```bash
# Download just the script
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm

# Init config
opsterm init
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
cd ~/opsterm && git pull
```

Or if you installed via single file:

```bash
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/main/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
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
