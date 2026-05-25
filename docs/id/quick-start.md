# ⚡ Mulai Cepat

Bikin OpsTerm jalan dalam 5 menit.

## Setup 5 Menit

```bash
# 1. Clone atau download
git clone https://github.com/edsuwarna/opsterm.git
cd opsterm

# 2. Tambah ke PATH
echo 'export PATH=$PATH:'"$(pwd)"'/bin' >> ~/.bashrc
source ~/.bashrc

# 3. Set AI provider
mkdir -p ~/.ai-workflows
cat > ~/.ai-workflows/config.yaml << 'EOF'
provider: openai
api_key: sk-your-key-here
model: gpt-4o
EOF

# 4. Verifikasi
opsterm "bilang hello dalam satu kata"
```

## Perintah Pertama

```bash
# AI chat
opsterm "cek penggunaan disk"

# SSH ke server
opsterm ssh my-server

# Pipe mode
docker ps | opsterm "ada error?"

# Lihat daftar server
opsterm servers
```

## Selanjutnya

- [📦 Instalasi](installation.md) — opsi install detail
- [🚀 Panduan Penggunaan](usage-guide.md) — workflow sehari-hari
