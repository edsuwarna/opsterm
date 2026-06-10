# 🔍 Troubleshooting

Common issues and their solutions.

## Command Not Found

```bash
# opsterm: command not found
# Fix: add to PATH
export PATH="$HOME/opsterm/bin:$PATH"
```

If the error persists, check your shell config:

```bash
echo 'export PATH="$HOME/opsterm/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## AI Provider Errors

### "API key not configured"

```bash
# Set your API key
export OPSTERM_API_KEY=sk-xxx
# Or create config file
mkdir -p ~/.opsterm
cat > ~/.opsterm/config.yaml << 'EOF'
provider: openai
api_key: sk-xxx
model: gpt-4o
EOF
```

### "Rate limit exceeded"

- Wait a few seconds and retry
- Check your API provider's rate limits
- Reduce concurrent requests

### "Connection timeout"

```bash
# Check network connectivity
curl -I https://api.openai.com

# Set custom timeout
export OPSTERM_TIMEOUT=120
```

## SSH Issues

### "Connection refused"

```bash
# Check if SSH is running on the server
ssh -p 22 user@server

# Verify server config
opsterm servers
```

### "Permission denied"

```bash
# Check SSH key
ssh-add -l  # list loaded keys

# Add your key
ssh-add ~/.ssh/id_ed25519

# Or specify key in servers.yaml
# ~/.opsterm/servers.yaml
servers:
  my-server:
    host: 192.168.1.10
    user: root
    key: ~/.ssh/id_ed25519
```

### "Host key verification failed"

```bash
# Clear the host key
ssh-keygen -R "server-ip-or-hostname"

# Or temporarily disable (not recommended for production)
# ~/.ssh/config
Host myserver
    StrictHostKeyChecking no
```

## Pipe Mode Issues

### "No output from pipe"

```bash
# Test pipe input separately
echo "test" | opsterm "what is this?"

# Some commands buffer output — use stdbuf
stdbuf -oL docker logs my-app | opsterm "analyze"
```

### "Slow response with large input"

OpsTerm sends the full piped content as context. For large logs:

```bash
# Limit input
tail -100 /var/log/syslog | opsterm "find errors"

# Or use grep first
dmesg | grep -i error | opsterm "analyze"
```

## Debug Mode

Enable verbose logging:

```bash
export OPSTERM_DEBUG=true
opsterm "test query"
```

This prints detailed information about API calls, config loading, and SSH connections.

## Getting Help

- **GitHub Issues:** [github.com/edsuwarna/opsterm/issues](https://github.com/edsuwarna/opsterm/issues)
- **Docs:** Re-read the relevant documentation page
- **Quick test:** `opsterm "hello"` — if this works, the core AI feature is fine
