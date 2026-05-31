# OpsTerm Zsh Completion
# Source:  source <(opsterm completion zsh)
# Or add to .zshrc:  source <(opsterm completion zsh)

_opsterm() {
    local -a cmds
    cmds=(
        'ssh:SSH to saved server'
        'run:Run a workflow'
        'servers:Manage server list'
        'workflows:Manage workflow list'
        'config:View/set configuration'
        'provider:Manage AI provider'
        'history:Show command history'
        'init:Setup initial config'
        'scp:Upload/download files'
        'last:Last command output'
        'explain-last:Explain last output with AI'
        'doctor:Diagnose installation and configuration'
        'search:Search chat history'
        'export:Export config to tar.gz'
        'import:Import config from tar.gz'
        'reset:Reset config to defaults'
        'completion:Generate completion script'
    )
    _arguments -C '1: :->command' '*: :->args'
    case "$state" in
        command) _describe 'command' cmds ;;
        args)
            case "$words[1]" in
                ssh|--via)
                    local servers; servers=(${(f)"$(opsterm servers list 2>/dev/null | awk 'NR>2 && !/^---/ && !/^Total:/ {print $1}')"})
                    _describe 'server' servers ;;
                run)
                    local workflows; workflows=(${(f)"$(opsterm workflows list 2>/dev/null | grep '⚡' | awk '{print $2}')"})
                    _describe 'workflow' workflows ;;
                servers) _values 'action' list add edit rm ping show rename import-ssh-config ;;
                workflows) _values 'action' list add edit rm init ;;
                config) _values 'action' list get set validate ;;
                provider) _values 'action' list add rm default test models supported ;;

                scp)
                    local servers; servers=(${(f)"$(opsterm servers list 2>/dev/null | awk 'NR>2 && !/^---/ && !/^Total:/ {print $1":"}')"})
                    _describe 'server' servers ;;
                completion) _values 'action' bash zsh install ;;
            esac ;;
    esac
}
compdef _opsterm opsterm
