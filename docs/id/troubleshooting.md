# 🔍 Pemecahan Masalah

Masalah umum dan solusinya.

## Command Not Found

```bash
export PATH="$HOME/opsterm/bin:$PATH"
```

## AI Provider Errors

### "API key not configured"

```bash
export OPSTERM_API_KEY=sk-xxx
mkdir -p ~/.ai-workflows
```

### "Connection timeout"

```bash
curl -I https://api.openai.com
export OPSTERM_TIMEOUT=120
```

## SSH Issues

### "Connection refused"

```bash
ssh -p 22 user@server
opsterm servers
```

### "Permission denied"

```bash
ssh-add ~/.ssh/id_ed25519
```

## Pipe Mode Issues

```bash
tail -100 /var/log/syslog | opsterm "cari error"
```

## Debug Mode

```bash
export OPSTERM_DEBUG=true
opsterm "test query"
```

## Bantuan

- **GitHub Issues:** [github.com/edsuwarna/opsterm/issues](https://github.com/edsuwarna/opsterm/issues)
- **Test cepat:** `opsterm "hello"`
