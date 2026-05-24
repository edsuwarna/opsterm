#!/usr/bin/env bash
set -e

echo "🚀 OpsTerm — AI Terminal Assistant Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 required. Install dulu: sudo apt install python3"
    exit 1
fi

echo "✅ Python $(python3 --version) found"

# Create symlink
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="$SCRIPT_DIR/bin/opsterm"
INSTALL_DIR="${HOME}/.local/bin"

mkdir -p "$INSTALL_DIR"
if [ -f "$INSTALL_DIR/opsterm" ] || [ -L "$INSTALL_DIR/opsterm" ]; then
    rm -f "$INSTALL_DIR/opsterm"
fi
ln -sf "$TARGET" "$INSTALL_DIR/opsterm"
echo "✅ Symlink: $INSTALL_DIR/opsterm → $TARGET"

# Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    SHELL_CONFIG="${HOME}/.bashrc"
    if [ "$SHELL" = "/usr/bin/zsh" ] || [ "$SHELL" = "/bin/zsh" ]; then
        SHELL_CONFIG="${HOME}/.zshrc"
    fi
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_CONFIG"
    echo "✅ Added ~/.local/bin to PATH in $SHELL_CONFIG"
    echo "   Jalankan: source $SHELL_CONFIG"
fi

# Init config
python3 "$TARGET" init

echo ""
echo "🎉 OpsTerm siap digunakan!"
echo ""
echo "🔑 Jangan lupa set API key:"
echo "   export OPSTERM_API_KEY='sk-...'"
echo ""
echo "📖 Coba:"
echo "   opsterm --help"
echo "   opsterm ssh vps-utama"
echo "   opsterm run cek-server"
echo ""
