# ⚡ Quick Start

Get OpsTerm running in under 5 minutes.

## 5-Minute Setup

```bash
# 1. Clone or download
git clone https://github.com/edsuwarna/opsterm.git
cd opsterm

# 2. Add to PATH
echo 'export PATH=$PATH:'"$(pwd)"'/bin' >> ~/.bashrc
source ~/.bashrc

# 3. Set AI provider
mkdir -p ~/.ai-workflows
cat > ~/.ai-workflows/config.yaml << 'EOF'
provider: openai
api_key: sk-your-key-here
model: gpt-4o
EOF

# 4. Verify it works
opsterm "say hello in one word"
```

> **Tip:** See [Installation](installation.md) for other methods (Homebrew, Zsh plugin, etc.)

## First Commands

```bash
# AI chat
opsterm "how to check disk usage"

# SSH into a server
opsterm ssh my-server

# Pipe mode — explain command output
docker ps | opsterm "any errors?"

# List saved servers
opsterm servers
```

## What's Next?

- [📦 Installation](installation.md) — detailed install options
- [🚀 Usage Guide](usage-guide.md) — day-to-day workflows
- [⚙️ Configuration](configuration.md) — customize everything
