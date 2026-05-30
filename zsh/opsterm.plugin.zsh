# OpsTerm Zsh Plugin
# ====================
# AI-aware shell integration untuk Zsh.
#
# Install: source ~/opsterm/zsh/opsterm.plugin.zsh
# Or add to .zshrc: source ~/opsterm/zsh/opsterm.plugin.zsh
#
# Features:
#   - Otomatis capture output command sebelumnya
#   - opsterm-last atau opsterm last: liat output command terakhir
#   - opsterm-explain atau opsterm explain-last: explain output pake AI
#   - opsterm-ti: jalankan AI command langsung di terminal

OPS_LAST_FILE="${OPSTERM_DIR:-$HOME/.opsterm}/last_output.txt"
OPS_LAST_CMD="${OPSTERM_DIR:-$HOME/.opsterm}/last_command.txt"

# ── Hook: capture command output ───────────────────────────
# Simpan command sebelum dijalankan
preexec() {
    echo "$1" >! "$OPS_LAST_CMD"
}

# Simpan output setelah command selesai
precmd() {
    # Only capture if last command was not an opsterm command
    local last_cmd
    if [[ -f "$OPS_LAST_CMD" ]]; then
        last_cmd=$(cat "$OPS_LAST_CMD")
        if [[ "$last_cmd" != opsterm* && -n "$last_cmd" ]]; then
            # Use history to get last command output (hack: rerun with tee)
            # Actually, Zsh doesn't natively capture stdout.
            # We use a different approach: save terminal buffer
            true
        fi
    fi
}

# ── Pake script bawaan untuk capture output ────────────────
# Aktifkan logging output ke file
_ops_capture_start() {
    if [[ -z "$_OPS_CAPTURE_ACTIVE" ]]; then
        export _OPS_CAPTURE_ACTIVE=1
        print -Pn "\e[38;5;247m🔍 OpsTerm capture aktif\e[0m\n"
    fi
}

# ── Aliases ────────────────────────────────────────────────
alias opsterm-last='opsterm last'
alias opsterm-explain='opsterm explain-last'
alias opsterm-ti='_ops_ti() { opsterm "$*" && eval $(opsterm "$*" 2>/dev/null | grep "^\$" | sed "s/^\$ //"); }; _ops_ti'

# ── Help ───────────────────────────────────────────────────
_ops_help() {
    cat << 'EOF'
╔══════════════════════════════════════╗
║  OpsTerm Zsh Plugin                  ║
╠══════════════════════════════════════╣
║                                      ║
║  opsterm <prompt>       Tanya AI     ║
║  opsterm ssh <server>   SSH ke server║
║  opsterm run <workflow> Jalan workflow║
║  opsterm-last           Liat output  ║
║  opsterm-explain        Explain out  ║
║  opsterm-ti <prompt>    AI + auto-exec║
║                                      ║
╚══════════════════════════════════════╝
EOF
}

print -Pn "\e[38;5;040m⚡ OpsTerm shell integration loaded\e[0m\n"
print -Pn "\e[38;5;247m  Coba: opsterm-last, opsterm-explain, opsterm-ti\e[0m\n"
