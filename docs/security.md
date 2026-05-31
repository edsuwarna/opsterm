# 🔒 Security

OpsTerm's security model, best practices, and known considerations.

## Architecture Security

### Local-First Design

OpsTerm runs on **your local machine**. The AI never runs on remote servers:
- AI API keys stay on your laptop
- SSH keys are used from your local agent
- No server-side installation needed (except SSH)

### No Remote Agent

Unlike other tools, OpsTerm doesn't install anything on remote servers. This means:
- No persistence on remote machines
- No privileged daemons running on your VPS
- Clean SSH sessions — nothing left behind

## API Key Security

Your AI provider API key is stored in `~/.ai-workflows/config.yaml`:

```yaml
# Recommended: restrictive permissions
chmod 600 ~/.ai-workflows/config.yaml
```

### Alternative: Environment Variables

```bash
export OPSTERM_API_KEY=sk-xxx
# config.yaml can omit api_key when env var is set
```

This is useful for CI/CD or shared environments.

## SSH Security

- OpsTerm uses your existing SSH keys and `~/.ssh/config`
- No SSH password storage in plaintext
- ProxyJump support for bastion hosts
- SSH connection timeout configurable via `OPSTERM_SSH_TIMEOUT`

## Best Practices

1. **Restrict config file permissions:**
   ```bash
   chmod 600 ~/.ai-workflows/config.yaml
   chmod 700 ~/.ai-workflows/
   ```

2. **Use environment variables for CI:**
   ```bash
   export OPSTERM_API_KEY=$CI_AI_KEY
   ```

3. **Audit server list:**
   ```bash
   opsterm servers  # review configured servers
   ```

## Known Considerations

- AI queries containing sensitive data are sent to third-party providers (OpenAI, Anthropic, etc.)
- Use on-premise providers (Ollama, vLLM) for sensitive environments
- SSH session content is never logged or transmitted outside your machine
