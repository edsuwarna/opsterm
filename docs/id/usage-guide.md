# 🚀 Panduan Penggunaan

Gimana pake OpsTerm sehari-hari.

## AI Chat

```bash
# Pertanyaan sederhana
opsterm "cari file besar"

# Pipe mode
docker logs my-app | opsterm "ada error apa?"

# Info sistem
opsterm "cek disk usage"
```

## SSH Mode

```bash
# SSH langsung
opsterm ssh my-server

# Via proxy
opsterm ssh internal-server --via bastion

# Multi-hop
opsterm ssh app-3 --via bastion --via jump-box
```

## Pipe Mode

```bash
journalctl -u nginx | opsterm "cari error pattern"
cat /etc/nginx/nginx.conf | opsterm "masalah keamanan?"
```

## SCP File Transfer

```bash
# Upload
opsterm scp ./config.yaml my-server:/etc/app/

# Download
opsterm scp my-server:/var/log/app.log ./logs/
```

## Vault

```bash
opsterm vault add db-pass mysecret123
opsterm vault list
opsterm vault get db-pass
```

## Workflows

```bash
opsterm workflows
opsterm run health-check
```
