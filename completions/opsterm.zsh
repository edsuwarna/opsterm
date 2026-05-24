# OpsTerm Zsh Completion
# Source:  source <(opsterm completion zsh)
# Or add to .zshrc:  source <(opsterm completion zsh)

_opsterm() {
    local -a cmds
    cmds=(
        'ssh:SSH ke server tersimpan'
        'run:Jalanin workflow'
        'servers:Manage server list'
        'workflows:Manage workflow list'
        'config:Lihat/set konfigurasi'
        'history:Riwayat command'
        'init:Setup konfigurasi awal'
        'scp:Upload/download file via server'
        'vault:Manage encrypted credentials'
        'last:Lihat output command terakhir'
        'explain-last:Explain output command terakhir pake AI'
        'completion:Generate shell completion script'
    )

    _arguments -C \
        '1: :->command' \
        '*: :->args'

    case "$state" in
        command)
            _describe 'command' cmds
            ;;
        args)
            case "$words[1]" in
                ssh)
                    _opsterm_servers
                    ;;
                run)
                    _opsterm_workflows
                    ;;
                servers)
                    _values 'action' list add edit rm
                    ;;
                workflows)
                    _values 'action' list add edit rm
                    ;;
                config)
                    _values 'action' list get set
                    ;;
                vault)
                    _values 'action' init set get list rm lock
                    ;;
                scp)
                    _opsterm_servers_with_colon
                    ;;
                completion)
                    _values 'shell' bash zsh
                    ;;
                edit|rm)
                    case "$words[1]" in
                        rm)
                            case "$words[-2]" in
                                servers) _opsterm_servers ;;
                                workflows) _opsterm_workflows ;;
                            esac
                            ;;
                        edit)
                            _opsterm_servers
                            ;;
                    esac
                    ;;
                ssh|run)
                    # Already handled above
                    ;;
            esac
            ;;
    esac
}

_opsterm_servers() {
    local -a servers
    servers=(${(f)"$(_call_program servers opsterm servers list 2>/dev/null | awk 'NR>2 && !/^---/ && !/^Total/ {print $1}')"})
    _describe 'server' servers
}

_opsterm_workflows() {
    local -a workflows
    workflows=(${(f)"$(_call_program workflows opsterm workflows list 2>/dev/null | grep '⚡' | awk '{print $2}')"})
    _describe 'workflow' workflows
}

_opsterm_servers_with_colon() {
    local -a servers
    servers=(${(f)"$(_call_program servers opsterm servers list 2>/dev/null | awk 'NR>2 && !/^---/ && !/^Total/ {print $1\": \"}'"})
    _describe 'server' servers
}

compdef _opsterm opsterm
