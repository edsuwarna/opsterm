# OpsTerm Bash Completion
# Source:  source <(opsterm completion bash)
# Or add to .bashrc:  source <(opsterm completion bash)

_opsterm_completions() {
    local cur prev words cword
    _init_completion || return

    # Get all subcommands
    local cmds="ssh run servers workflows config history init scp vault last explain-last completion"

    # Current word being typed
    cur="${words[cword]}"
    prev="${words[cword-1]}"

    # Determine context
    case "${prev}" in
        opsterm)
            mapfile -t COMPREPLY < <(compgen -W "${cmds}" -- "${cur}")
            return 0
            ;;
        ssh)
            # Complete server names
            local servers
            servers=$(opsterm servers list 2>/dev/null | grep -v "NAMA\|---\|Total:" | awk '{print $1}')
            mapfile -t COMPREPLY < <(compgen -W "${servers}" -- "${cur}")
            return 0
            ;;
        run)
            # Complete workflow names
            local workflows
            workflows=$(opsterm workflows list 2>/dev/null | grep "⚡" | awk '{print $2}')
            mapfile -t COMPREPLY < <(compgen -W "${workflows}" -- "${cur}")
            return 0
            ;;
        servers)
            mapfile -t COMPREPLY < <(compgen -W "list add edit rm" -- "${cur}")
            return 0
            ;;
        workflows)
            mapfile -t COMPREPLY < <(compgen -W "list add edit rm" -- "${cur}")
            return 0
            ;;
        config)
            mapfile -t COMPREPLY < <(compgen -W "list get set" -- "${cur}")
            return 0
            ;;
        vault)
            mapfile -t COMPREPLY < <(compgen -W "init set get list rm lock" -- "${cur}")
            return 0
            ;;
        scp)
            # Suggest server: or local paths
            local servers
            servers=$(opsterm servers list 2>/dev/null | grep -v "NAMA\|---\|Total:" | awk '{print $1":"}')
            mapfile -t COMPREPLY < <(compgen -W "${servers}" -- "${cur}")
            return 0
            ;;
        completion)
            mapfile -t COMPREPLY < <(compgen -W "bash zsh" -- "${cur}")
            return 0
            ;;
        edit)
            # Complete server names for "servers edit"
            local servers
            servers=$(opsterm servers list 2>/dev/null | grep -v "NAMA\|---\|Total:" | awk '{print $1}')
            mapfile -t COMPREPLY < <(compgen -W "${servers}" -- "${cur}")
            return 0
            ;;
        rm)
            # Check context: workflows rm or servers rm
            local prev2="${words[cword-2]}"
            if [[ "${prev2}" == "servers" ]]; then
                local servers
                servers=$(opsterm servers list 2>/dev/null | grep -v "NAMA\|---\|Total:" | awk '{print $1}')
                mapfile -t COMPREPLY < <(compgen -W "${servers}" -- "${cur}")
            elif [[ "${prev2}" == "workflows" ]]; then
                local workflows
                workflows=$(opsterm workflows list 2>/dev/null | grep "⚡" | awk '{print $2}')
                mapfile -t COMPREPLY < <(compgen -W "${workflows}" -- "${cur}")
            fi
            return 0
            ;;
        --via|-v)
            # Complete proxy server names
            local servers
            servers=$(opsterm servers list 2>/dev/null | grep -v "NAMA\|---\|Total:" | awk '{print $1}')
            mapfile -t COMPREPLY < <(compgen -W "${servers}" -- "${cur}")
            return 0
            ;;
        *)
            # Check if previous word is a server name (for scp/rm context)
            ;;
    esac

    # Default: complete subcommands
    if [[ "${cword}" -eq 1 ]]; then
        mapfile -t COMPREPLY < <(compgen -W "${cmds}" -- "${cur}")
    fi
}

complete -F _opsterm_completions opsterm
