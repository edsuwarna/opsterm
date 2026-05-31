# ⚡ Quick Start

Get OpsTerm running in less than 2 minutes.

## 1. Install

```bash
curl -L https://raw.githubusercontent.com/edsuwarna/opsterm/v0.1.1/bin/opsterm -o ~/.local/bin/opsterm
chmod +x ~/.local/bin/opsterm
opsterm init
```

## 2. Add AI Provider

```bash
# Smart interactive — enter API key, pick provider, choose model ✨
opsterm provider add

# Or one-liner
opsterm provider add default --api-key sk-your-key --model gpt-4o
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
