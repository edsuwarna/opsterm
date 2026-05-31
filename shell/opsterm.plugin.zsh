# OpsTerm Zsh Plugin
# Source this in .zshrc:  source /path/to/opsterm.plugin.zsh
# Or use with plugin manager (oh-my-zsh, antigen, etc.)
#
# What it does:
#   - Auto-saves the last command and its exit code
#   - Makes `opsterm last` and `opsterm explain-last` work seamlessly
#   - Adds Ctrl-O binding to pipe last output to OpsTerm

OPSTERM_DIR="${OPSTERM_DIR:-$HOME/.opsterm}"
LAST_CMD_FILE="$OPSTERM_DIR/last_command.txt"
LAST_OUTPUT_FILE="$OPSTERM_DIR/last_output.txt"

# Ensure opsterm config dir exists
[[ -d "$OPSTERM_DIR" ]] || mkdir -p "$OPSTERM_DIR"

# ── Save command before execution ────────────────────────────
opsterm_preexec() {
    # $1 = the command line being executed (full string)
    printf '%s' "$1" >! "$LAST_CMD_FILE"
}

# ── Save exit code after execution ──────────────────────────
opsterm_precmd() {
    # $? is the exit code of the last foreground command
    local exit_code=$?
    # Save last command from history as fallback
    local last_cmd
    last_cmd="$(fc -ln -1 2>/dev/null)"
    if [[ -n "$last_cmd" ]]; then
        printf '%s' "$last_cmd" >! "$LAST_CMD_FILE"
    fi
    # Record exit code for explain-last context
    printf '%s' "$exit_code" >! "$OPSTERM_DIR/last_exit_code.txt"
}

# ── Ctrl-O: pipe last output to OpsTerm ────────────────────
# Press Ctrl-O after any command to analyze its output with AI
__opsterm_analyze_last() {
    # Re-run last command, capture output, pipe to opsterm
    local last_cmd
    last_cmd="$(fc -ln -1 2>/dev/null)"
    if [[ -z "$last_cmd" ]]; then
        zle reset-prompt
        return
    fi
    # Save output
    eval "$last_cmd" 2>&1 | tee "$LAST_OUTPUT_FILE" | opsterm "Explain this output"
    zle reset-prompt
}
zle -N __opsterm_analyze_last
bindkey '^O' __opsterm_analyze_last

# ── Install hooks ───────────────────────────────────────────
autoload -Uz add-zsh-hook
add-zsh-hook preexec opsterm_preexec
add-zsh-hook precmd opsterm_precmd
