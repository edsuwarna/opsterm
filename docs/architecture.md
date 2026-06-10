# 📐 Architecture & System Design

This document explains in detail how OpsTerm works — from when the user types a command until the output is displayed.

---

## 🏗️ Overall Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ CLI Terminal  │  │ Zsh Plugin   │  │ Pipe (stdin)     │  │
│  │ opsterm <command>  │  │ opsterm-last      │  │ cmd | opsterm <prompt>│  │
│  │ opsterm ssh <svr>  │  │ opsterm-explain   │  │                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
└─────────┼─────────────────┼────────────────────┼────────────┘
          │                 │                    │
          ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   CLI ROUTER (argparse)                     │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────┐ ┌───────┐  │
│  │ opsterm <ask> │ │ opsterm ssh   │ │ai scp  │ │ai run│ │        │  │
│  │ (default)│ │          │ │        │ │      │ │        │  │
│  └────┬─────┘ └────┬─────┘ └───┬────┘ └──┬───┘ └───┬───┘  │
└───────┼────────────┼───────────┼─────────┼──────────┼──────┘
        │            │           │         │          │
        ▼            ▼           ▼         ▼          ▼
┌────────────────────────────────────────────────────────────┐
│                      ENGINES                                │
│                                                             │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────────┐  │
│  │ AI Client    │  │ SSH Runner │  │ SCP Transfer       │  │
│  │ (urllib)     │  │ (subproc)  │  │ (subprocess)       │  │
│  │ OpenAI-compat│  │ multi-hop  │  │ local ↔ remote     │  │
│  └──────┬───────┘  └─────┬──────┘  └────────┬───────────┘  │
│         │                │                   │              │
│  ┌──────▼────────────────▼───────────────────▼──────────┐  │
│  │              Workflow Executor                       │  │
│  │  Step: SSH → SCP → Local → Confirm → Wait           │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────┐  ┌────────────┐                          │
│  │ Config Loader│  │ History    │                          │
│  │ (YAML/JSON)  │  │ (SQLite)   │                          │
│  └──────┬───────┘  └─────┬──────┘                          │
└─────────┼────────────────┼──────────────────────────────────┘
          │                │
          ▼                ▼
┌────────────────────────────────────────────────────────────┐
│                    EXTERNAL SYSTEMS                         │
│                                                             │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ AI Provider API  │  │ SSH Servers  │  │ Local File    │ │
│  │ (DeepSeek,OpenAI,│  │ (VPS, cloud, │  │ System        │ │
│  │  Ollama, etc)    │  │  instances)  │  │ (config)       │ │
│  └─────────────────┘  └──────────────┘  └───────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Execution Flows

### Flow 1: AI Chat (`opsterm how to check disk`)

```
User input: "opsterm how to check disk"
             │
             ▼
    ┌─────────────────┐
    │ 1. Parse args    │ ← argparse: subcmd=None (default AI mode)
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 2. Load config   │ ← config.yaml (API key, model, URL)
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. Build prompt  │ ← + stdin_data if piped
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ 4. AI Chat (ai_chat())          │
    │    POST to /v1/chat/completions  │
    │    Headers: Authorization Bearer │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. Parse response│ ← JSON: choices[0].message.content
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 6. Print output  │ ← stdout
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 7. Auto-exec?    │ ← If response contains $, prompt user
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ 8. Save history  │ ← SQLite (mode, input, output)
    └──────────────────┘
```

### Flow 2: SSH (`opsterm ssh vps-utama --via bastion`)

```
User input: "opsterm ssh vps-utama --via bastion"
             │
             ▼
    ┌───────────────────────┐
    │ 1. Parse args          │ ← subcmd="ssh", server="vps-utama"
    └──────────┬─────────────┘    proxy="bastion"
               │
               ▼
    ┌───────────────────────┐
    │ 2. Load servers.yaml   │ ← get_servers()
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 3. Lookup server       │ ← _server_lookup("vps-utama")
    │    vps-utama:          │
    │      host: 43.157..    │
    │      user: ubuntu      │
    │      key: ~/.ssh/...   │
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 4. Resolve proxy      │ ← _resolve_proxy("bastion")
    │    → "ubuntu@10.0.0.1"│    → format: user@host[:port]
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 5. Build SSH command   │ ← ["ssh", "-J", proxy, "-i", key,
    │                          "ubuntu@43.157..", "-t"]
    └──────────┬─────────────┘
               │
               ▼
    ┌───────────────────────┐
    │ 6. execvp()            │ ← Replace process with interactive SSH
    │    → Interactive SSH   │
    └───────────────────────┘
```

### Flow 3: Workflow (`opsterm run deploy-app`)

```
User input: "opsterm run deploy-app"
             │
             ▼
    ┌──────────────────────┐
    │ 1. Parse args         │ ← subcmd="run", workflow="deploy-app"
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 2. Load workflows    │ ← workflows.yaml
    │    deploy-app:       │
    │      steps: [...]    │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 3. Iterate steps     │
    │                       │
    │  Step 1: ssh          │────→ SSH to server + execute command
    │  Step 2: scp          │────→ SCP file to server
    │  Step 3: local        │────→ Local shell command
    │  Step 4: confirm      │────→ Prompt user Y/n
    │  Step 5: wait         │────→ time.sleep(n)
    │                       │
    └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 4. Done              │ ← "✅ Workflow complete!"
    └──────────────────────┘
```

### Flow 4: Pipe Mode (`docker ps | opsterm "any errors?"`)

```
User input: "docker ps | opsterm any errors?"
             │
             ▼
    ┌──────────────────────────────────┐
    │ 1. stdin detected (not isatty()) │ ← sys.stdin.read()
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │ 2. stdin_data = "CONTAINER ID..."│ ← docker ps output
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │ 3. Build prompt:                 │
    │    "Output of command:           │
    │     '''                          │
    │     CONTAINER ID IMAGE...        │
    │     '''                          │
    │                                 │
    │     Question: any errors?"      │
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │ 4. Send to AI           ← same as AI Chat flow
    └──────────────────────────────────┘
```

---

## 📁 State Management

OpsTerm **has no daemon or background process**. All state is stored in files:

| File | Format | Contents |
|------|--------|----------|
| `config.yaml` | YAML | AI provider, model, api_url, shell settings |
| `servers.yaml` | YAML | Server list: host, user, port, key, proxy |
| `workflows.yaml` | YAML | Workflow list: steps (ssh/scp/local) |

| `history.db` | SQLite | Command history (mode, input, output) |
| `last_output.txt` | Text | Last command output (for explain-last) |
| `last_command.txt` | Text | Last command |

**Data flow:**

```
Config is read every time a command runs → no in-memory caching
History is written after command finishes → append-only
Last output is written by the zsh plugin → read by opsterm last/explain-last
```

---

## 🔒 Security

### API Key
- Can be set via **env var** (`OPSTERM_API_KEY`) — recommended
- Or stored in **config.yaml** — but be careful if shared
- Gitignored (`config.yaml` is in `.gitignore`)

### SSH
- Uses **SSH key** from local filesystem (not password)
- ProxyJump via `-J` flag (secure, encrypted)
- Server config can specify key path per-server

---

## 🧪 Testing & Error Handling

### Error recovery in workflows:
```python
if result.returncode != 0:
    print(f"❌ Step {i} failed")
    # Ask user: continue or stop?
    cont = input("Continue? [y/N] ")
    if cont not in ("y", "yes"):
        print("⛔ Workflow aborted.")
        return
```

### Fallback strategy:
- **AI call fails** → print error message, don't crash
- **Config file corrupted** → return empty dict, don't crash

- **SSH server unreachable** → SSH itself handles the error

---

## 🚀 Performance

| Operation | Time (approx) | Notes |
|-----------|---------------|-------|
| AI Chat (DeepSeek) | 1-3 sec | Depends on provider & network |
| SSH Connect | < 1 sec | Direct execvp, no overhead |
| SCP Transfer | Varies | Depends on file size & bandwidth |
| Workflow (3 steps) | 5-15 sec | Depends on step complexity |
| Config load | < 10ms | Minimal YAML parsing |
| History write | < 5ms | SQLite append |

**Memory footprint:** ~15-30MB (Python interpreter) + overhead per operation.

---

Next: [🔧 Tech Stack →](tech-stack.md)
