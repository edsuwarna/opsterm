# 🔒 Keamanan

Model keamanan OpsTerm dan best practices.

## Local-First Design

- AI API keys tetap di laptop lu
- SSH keys dipake dari local agent
- Enggak ada installasi di server remote

## API Key Security

```bash
chmod 600 ~/.ai-workflows/config.yaml
```

Atau pake environment variables:

```bash
export OPSTERM_API_KEY=sk-xxx
```

## Vault Encryption

Credential dienkripsi pake AES-256-GCM:

- Key derivation: PBKDF2 100,000 iterasi
- Master password: gak pernah disimpan

## Best Practices

1. **Restrict config permissions:**
   ```bash
   chmod 600 ~/.ai-workflows/config.yaml
   ```

2. **Gunakan env vars untuk CI:**
   ```bash
   export OPSTERM_API_KEY=$CI_AI_KEY
   ```

3. **Rotate vault berkala:**
   ```bash
   opsterm vault rotate
   ```
