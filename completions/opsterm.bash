# OpsTerm Bash Completion
# Source:  source <(opsterm completion bash)
# Or add to .bashrc:  source <(opsterm completion bash)

_opsterm_completions() {
    local cur prev words cword
    _init_completion || return
    local cmds="ssh run servers workflows config provider history init scp vault last explain-last completion doctor search export import reset"
    cur="${words[cword]}"
    prev="${words[cword-1]}"
    case "${prev}" in
        opsterm) mapfile -t COMPREPLY < <(compgen -W "${cmds}" -- "${cur}"); return 0 ;;
        ssh|--via|-v)
            local servers; servers=$(opsterm servers list 2>/dev/null | awk 'NR>2 && !/^---/ && !/^Total:/ {print $1}')
            mapfile -t COMPREPLY < <(compgen -W "${servers}" -- "${cur}"); return 0 ;;
        run)
            local workflows; workflows=$(opsterm workflows list 2>/dev/null | grep '⚡' | awk '{print $2}')
            mapfile -t COMPREPLY < <(compgen -W "${workflows}" -- "${cur}"); return 0 ;;
        servers) mapfile -t COMPREPLY < <(compgen -W "list add edit rm ping show rename import-ssh-config" -- "${cur}"); return 0 ;;
        workflows) mapfile -t COMPREPLY < <(compgen -W "list add edit rm init" -- "${cur}"); return 0 ;;
        config) mapfile -t COMPREPLY < <(compgen -W "list get set validate" -- "${cur}"); return 0 ;;
        provider) mapfile -t COMPREPLY < <(compgen -W "list add rm default test models supported" -- "${cur}"); return 0 ;;
        vault) mapfile -t COMPREPLY < <(compgen -W "init set get list rm lock" -- "${cur}"); return 0 ;;
        scp)
            local servers; servers=$(opsterm servers list 2>/dev/null | awk 'NR>2 && !/^---/ && !/^Total:/ {print $1":"}')
            mapfile -t COMPREPLY < <(compgen -W "${servers}" -- "${cur}"); return 0 ;;
        completion) mapfile -t COMPREPLY < <(compgen -W "bash zsh install" -- "${cur}"); return 0 ;;
        doctor) return 0 ;;
        search) return 0 ;;
        export) return 0 ;;
        import) return 0 ;;
        reset) return 0 ;;
    esac
    if [[ "${cword}" -eq 1 ]]; then
        mapfile -t COMPREPLY < <(compgen -W "${cmds}" -- "${cur}")
    fi
}
complete -F _opsterm_completions opsterm
