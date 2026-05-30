# 🤔 Design Decisions

This document explains **why** OpsTerm is designed the way it is — the reasoning behind each technical decision, including the trade-offs that were made.

---

## 📜 Decision Summary

| # | Decision | Choice | Rejected Alternatives |
|---|----------|--------|-----------------------|
| 1 | **Language** | Python 3 | Go, Rust, Node.js, Bash |
| 2 | **Architecture** | Single-file CLI | Modular package, Client-server |
| 3 | **Dependencies** | Zero (stdlib only) | PyYAML, requests, click |
| 4 | **Config format** | YAML (custom parser) | JSON, TOML, INI |
| 5 | **AI Protocol** | OpenAI-compatible API | LangChain, custom gRPC |
| 6 | **SSH Method** | Subprocess + system SSH | paramiko, asyncssh |
| 7 | **State** | File-based (no daemon) | SQLite daemon, Redis |
| 8 | **Vault** | Optional cryptography | Hardcoded key, no encryption |
| 9 | **Completion** | Generated script | Manual completion |
| 10 | **Shell Integration** | Separate Zsh plugin | Hook shell, LD_PRELOAD |
| 11 | **RTK Integration** | Optional, auto-detect, graceful fallback | Always-on, hard dependency |

---

## 1️⃣ Why Python, not Go/Rust?

### Context
OpsTerm needed a language that is **portable, zero-dependency, and easy to maintain**.

### Decision: ✅ Python 3

**Reasons:**

1. **Ubiquitous** — Every Linux and macOS system has Python 3. Users just download the script and run it. With Go/Rust, you'd need to compile first or download a binary.

2. **Rich stdlib** — `argparse`, `json`, `sqlite3`, `urllib`, `hashlib`, `subprocess` — all built-in. In Go/Rust, these libraries require external imports or have less complete standard libraries.

3. **Maintainability** — Python is easier to read and modify. Potential contributors can understand the code more easily.

4. **File size** — ~50KB Python script vs ~10MB Go binary. Small and easy to copy to any server.

5. **Rapid iteration** — New features can be used immediately without compilation. Edit → save → run.

**Trade-offs:**
- Lower performance (but for a CLI tool, this is imperceptible)
- Requires Python interpreter (but every modern system already has one)

---

## 2️⃣ Why single file, not a package?

### Context
OpsTerm could have been built as a Python package installable via `pip install`.

### Decision: ✅ Single file (`bin/opsterm`)

**Reasons:**

1. **Portable** — Copy one file to any server and it runs. `scp bin/opsterm server:~/.local/bin/`

2. **Zero setup** — No `pip install`, no `python -m opsterm`. Just `./ai`.

3. **Transparent** — The entire code can be read and understood. No `__pycache__`, `egg-info`, etc.

4. **Easy debugging** — If there's an error, just edit a specific line. No need to hunt through directories.

**Trade-offs:**
- Large file (~1500 lines). Still small compared to other applications.
- All functions in one file — harder to unit test.
- Mitigation: code is organized with section header comments.

---

## 3️⃣ Why zero dependencies?

### Context
Many Python CLI tools use `PyYAML`, `requests`, `click`, etc.

### Decision: ✅ Zero external dependencies

**Reasons:**

1. **No install step** — Clone repo → run directly. No `pip install -r requirements.txt` needed.

2. **No version conflicts** — Will never clash with system libraries or other projects.

3. **Works in any Python environment** — Virtual env, system Python, container — all work.

4. **Easy to audit** — All running code can be read. No hidden dependencies.

**What was sacrificed:**

- **Manual YAML parser** (~80 lines) — doesn't support the full YAML spec, but sufficient for needs.
- **HTTP client via stdlib** (`urllib`) — more verbose than `requests`, but functional.
- **CLI parser via stdlib** (`argparse`) — less powerful than `click`, but sufficient.

---

## 4️⃣ Why YAML, not JSON/TOML?

### Context
Config format for servers, workflows, and AI settings.

### Decision: ✅ YAML (with custom parser)

**Reasons:**

1. **Readability** — YAML is more human-readable than JSON. Comments and clean indentation.

2. **User-friendly** — OpsTerm's target users are DevOps engineers who already use YAML (Docker Compose, Kubernetes, Ansible, GitHub Actions).

3. **No brackets** — JSON is full of `{}` and `[]` that hurt readability for long configs.

**Trade-offs:**
- Custom parser → limited. But the YAML subset we use (mapping, list, scalar) is stable and sufficient.
- Inconsistency with "zero dep" — technically YAML parsing is custom code, not an external dependency.

---

## 5️⃣ Why OpenAI-compatible API, not an AI library?

### Context
Could have used LangChain, LiteLLM, or another AI abstraction library.

### Decision: ✅ Direct HTTP call (OpenAI-compatible)

**Reasons:**

1. **Zero dependency** — Only `urllib` (stdlib). LangChain requires 20+ dependencies.

2. **Provider agnostic** — The OpenAI request/response format has become the de-facto standard. DeepSeek, Ollama, vLLM, OpenRouter — all support it.

3. **Simple** — The Chat Completion API is just one endpoint with a simple format.

4. **Debug friendly** — Requests/responses can be logged, inspected, and tested with curl.

**Trade-offs:**
- No built-in retry logic, streaming, or tool calling.
- But for a blocking CLI tool, this doesn't matter.

---

## 6️⃣ Why system SSH, not a Python library?

### Context
Could have used `paramiko` (a Python SSH client library).

### Decision: ✅ System SSH (`subprocess` + `/usr/bin/ssh`)

**Reasons:**

1. **Feature parity** — System SSH has every feature: key management, ProxyJump, agent forwarding, compression, etc.

2. **Zero dependency** — `paramiko` requires `bcrypt`, `cryptography`, `pynacl`, etc.

3. **Familiar** — All SSH configuration (known_hosts, config, agent) works automatically.

4. **Interactive support** — `os.execvp()` can provide a full interactive SSH session. `paramiko` can't do this seamlessly.

5. **Already configured** — Users already have SSH keys set up on their system.

**Trade-offs:**
- Cannot parse SSH output in real-time.
- Limited error handling (exit code only).

---

## 7️⃣ Why file-based state, not a daemon?

### Context
Some tools use a background daemon that stores state in memory.

### Decision: ✅ File-based (no daemon)

**Reasons:**

1. **Zero resource** — No background process. No RAM/CPU consumed when not in use.

2. **Crash-proof** — If the terminal is killed, data isn't lost. Everything is in files.

3. **Transparent** — Users can open the config directly and edit with a text editor.

4. **Simple** — No need to manage process lifecycle, signal handling, or lock files.

**Trade-offs:**
- State is read from disk on every command → slight overhead (<10ms).
- No "real-time" notification capability.

---

## 8️⃣ Why optional vault?

### Context
Vault requires `cryptography` which is not in stdlib.

### Decision: ✅ Optional — `cryptography` recommended, fallback available

**Reasons:**

1. **Zero dep still applies** — OpsTerm's core features work without the vault.

2. **Security remains a priority** — Vault uses AES via cryptography. Fallback uses XOR + HMAC when cryptography is unavailable.

3. **Progressive enhancement** — Users can start without the vault and install cryptography later if needed.

**Trade-offs:**
- Two code paths to maintain (with and without `cryptography`).
- Fallback encryption is weaker than AES.

---

## 9️⃣ Why generated completion?

### Context
Completion could be written manually or generated.

### Decision: ✅ Generated (embedded in script)

**Reasons:**

1. **Always up-to-date** — When new subcommands are added, completion automatically updates because it's generated from the code.

2. **Zero additional files** — `opsterm completion bash` prints directly to stdout. No separate file needed.

3. **Works out of the box** — `source <(opsterm completion bash)` — one command, done.

**Trade-offs:**
- Requires the `opsterm` script to be installed before completion works.
- Generator logic adds ~50 lines to the script.

---

## 🔟 Why a separate Zsh plugin?

### Context
Shell integration could be part of the main script or a separate file.

### Decision: ✅ Separate file (`zsh/opsterm.plugin.zsh`)

**Reasons:**

1. **Different language** — Zsh plugins use Zsh script, not Python. Combining them in the Python file would be messy.

2. **Zsh-only** — Shell hook features (`preexec`, `precmd`) only exist in Zsh.

3. **Lazy loading** — The plugin is only loaded if the user sources it in `.zshrc`. Doesn't add weight otherwise.

4. **Familiar pattern** — Zsh plugin format is already standard (oh-my-zsh, antigen, zplug).

**Trade-offs:**
- Only supports Zsh out of the box (no Bash/Fish support yet).
- Users must manually source the plugin in their shell config.

## 1️⃣1️⃣ 🗜️ Why optional RTK with graceful fallback?

### Context
OpsTerm processes command output (pipe mode, explain-last) that can be large — pytest output, git diffs, docker logs, etc. Sending all this to the AI provider consumes tokens and slows responses.

### Decision: ✅ Optional RTK integration — auto-detect, graceful fallback

**Reasons:**

1. **Token savings** — RTK compresses output 60-95% while preserving semantic meaning. pytest: 597→18 chars (-96%).

2. **Zero deps still applies** — RTK is optional. If not installed, OpsTerm runs normally. If installed, it's auto-detected.

3. **Auto-detect** — RTK automatically selects the best compression filter based on output patterns (git diff, pytest, docker ps, logs, etc.).

4. **Smart threshold** — Output <200 chars skips RTK (overhead not worth it). No unnecessary subprocess calls.

5. **Transparent** — User sees no difference in workflow. RTK happens silently between output capture and AI processing.

6. **RTK status** — `opsterm provider list` shows `🟢 RTK x.x.x` when available, `🔴 RTK unavailable` when not.

**Trade-offs:**
- Subprocess call overhead (~10-50ms). Mitigated by 200-char threshold.
- Another tool to install. Mitigated by graceful fallback — optional, not required.
- Extra config key (`rtk.*`) in config.yaml.

---

## 💡 Suggestions for Improvement

Based on the design decisions above, some future considerations:

1. **Python → Rust (future)** — If performance and distribution become issues, rewriting in Rust would provide a single binary.

2. **YAML → TOML** — If stricter configs with type safety are needed, TOML would be a better fit. However, this would require an external library.

3. **Add plugin system** — Allow the community to add features without editing the core script.

4. **Support Fish shell** — Popular among modern developers.

---

## 🔗 References

- [Python Argparse Docs](https://docs.python.org/3/library/argparse.html)
- [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat)
- [SSH ProxyJump (-J)](https://man.openbsd.org/ssh)
- [Fernet (symmetric encryption)](https://cryptography.io/en/latest/fernet/)
- [PBKDF2 Key Derivation](https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac)
