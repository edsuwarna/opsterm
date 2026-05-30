# ⚡ Quick Start

Get OpsTerm running in less than 2 minutes.

## 1. Install

```bash
git clone https://github.com/edsuwarna/opsterm.git ~/opsterm
cd ~/opsterm && ./setup.sh
```

## 2. Set API Key

```bash
export OPSTERM_API_KEY='sk-your-key'
```

Or edit `~/.opsterm/config.yaml`:

```yaml
ai:
  api_key: "sk-your-key"
  model: "gpt-4o"  # or deepseek-chat, claude-sonnet-4, etc.
```

## 3. Try It

```bash
opsterm "hello from opsterm"
opsterm how to check disk space
```

## 4. Add a Server (Optional)

```bash
opsterm servers add
```

Or edit `~/.opsterm/servers.yaml`:

```yaml
servers:
  my-server:
    host: "1.2.3.4"
    user: "root"
    port: 22
    desc: "My VPS"
```

## 5. SSH Without IPs

```bash
opsterm ssh my-server
```

## Next Steps

- [Installation Guide](installation.md) — full install/uninstall
- [Usage Guide](usage-guide.md) — all features
- [Configuration](configuration.md) — advanced settings
- [Workflows](features.md#workflows) — multi-step automation
