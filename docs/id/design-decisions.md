# 🤔 Design Decisions

Dokumen ini menjelaskan **kenapa** OpsTerm dirancang seperti ini — alasan di balik setiap keputusan teknis, termasuk trade-off yang diambil.

---

## 📜 Daftar Keputusan

| # | Keputusan | Pilihan | Alternatif yang Ditolak |
|---|-----------|---------|------------------------|
| 1 | **Bahasa** | Python 3 | Go, Rust, Node.js, Bash |
| 2 | **Arsitektur** | Single file CLI | Modular package, Client-server |
| 3 | **Dependencies** | Zero (stdlib only) | PyYAML, requests, click |
| 4 | **Config format** | YAML (custom parser) | JSON, TOML, INI |
| 5 | **AI Protocol** | OpenAI-compatible API | LangChain, custom gRPC |
| 6 | **SSH Method** | Subprocess + system ssh | paramiko, asyncssh |
| 7 | **State** | File-based (no daemon) | SQLite daemon, Redis |
| 8 | **Vault** | Optional cryptography | Hardcoded key, no encryption |
| 9 | **Completion** | Generated script | Manual completion |
| 10 | **Shell Integration** | Zsh plugin | Hook shell, LD_PRELOAD |

---

## 1️⃣ Kenapa Python, bukan Go/Rust?

### Konteks
OpsTerm butuh bahasa yang **portable, zero-dep, dan gampang di-maintain**.

### Keputusan: ✅ Python 3

**Alasan:**

1. **Ada di mana-mana** — Semua Linux & macOS punya Python 3. User tinggal download script, langsung jalan. Kalo Go/Rust, harus compile dulu atau download binary.

2. **Stdlib kaya** — `argparse`, `json`, `sqlite3`, `urllib`, `hashlib`, `subprocess` — semua built-in. Di Go/Rust, library-library ini butuh import eksternal atau stdlib yang kurang lengkap.

3. **Maintainability** — Python lebih gampang dibaca & dimodifikasi. Kontributor potensial lebih gampang ngerti kode.

4. **File size** — Script Python ~50KB vs Go binary ~10MB. Kecil, gampang di-copy ke server mana pun.

5. **Rapid iteration** — Fitur baru bisa langsung dipake tanpa compile. Edit → save → run.

**Trade-off:**
- Performance lebih rendah (tapi untuk CLI tool, ini gak kerasa)
- Butuh Python interpreter (tapi udah ada di semua system modern)

---

## 2️⃣ Kenapa single file, bukan package?

### Konteks
OpsTerm bisa aja dibikin sebagai Python package dengan `pip install`.

### Keputusan: ✅ Single file (`bin/opsterm`)

**Alasan:**

1. **Portable** — Copy 1 file ke server mana pun, langsung jalan. `scp bin/opsterm server:~/.local/bin/`

2. **Zero setup** — Ga perlu `pip install`, ga perlu `python -m opsterm`. Langsung `./ai`.

3. **Transparent** — Isinya bisa dibaca & dipahami. Gak ada `__pycache__`, `egg-info`, dll.

4. **Easy debugging** — Kalo error, tinggal edit baris tertentu, gak perlu cari file di folder.

**Trade-off:**
- File besar (~1500 baris). Tapi masih kecil dibanding app lain.
- Semua fungsi dalam 1 file — susah di-test secara unit.
- Solusi: kode diorganisir dengan section headers (comments).

---

## 3️⃣ Kenapa zero dependencies?

### Konteks
Banyak Python CLI tool pake `PyYAML`, `requests`, `click`, dll.

### Keputusan: ✅ Zero external dependencies

**Alasan:**

1. **No install step** — Clone repo → langsung jalan. Gak perlu `pip install -r requirements.txt`.

2. **No version conflicts** — Gak bakal bentrok sama library system atau project lain.

3. **Works in any Python env** — Virtual env, system Python, container, semuanya jalan.

4. **Easy to audit** — Semua kode yang jalan bisa dibaca. Gak ada hidden dependency.

**Yang dikorbankan:**
- YAML parser **manual** (~80 baris) — gak support full YAML spec, tapi cukup buat kebutuhan.
- HTTP client **stdlib** (`urllib`) — lebih verbose daripada `requests`, tapi fungsional.
- CLI parser **stdlib** (`argparse`) — kurang powerful daripada `click`, tapi cukup.

---

## 4️⃣ Kenapa YAML, bukan JSON/TOML?

### Konteks
Config format buat server, workflow, dan AI settings.

### Keputusan: ✅ YAML (dengan custom parser)

**Alasan:**

1. **Readability** — YAML lebih enak dibaca manusia dibanding JSON. Comment, indentasi bersih.

2. **User-friendly** — Target user OpsTerm adalah DevOps engineer yang biasa pake YAML (Docker Compose, Kubernetes, Ansible, GitHub Actions).

3. **No brackets** — JSON penuh `{}` dan `[]` yang ganggu readability buat config panjang.

**Trade-off:**
- Custom parser → terbatas. Tapi subset YAML yang kita pake (mapping, list, scalar) stabil dan cukup.
- Inkonisten dengan "zero dep" — technically YAML parsing itu custom code, bukan dependency eksternal.

---

## 5️⃣ Kenapa OpenAI-compatible API, bukan library AI?

### Konteks
Bisa pake LangChain, LiteLLM, atau library abstraksi AI lainnya.

### Keputusan: ✅ Direct HTTP call (OpenAI-compatible)

**Alasan:**

1. **Zero dependency** — Cuma `urllib` (stdlib). LangChain butuh 20+ dependencies.

2. **Provider agnostic** — Format OpenAI request/response udah jadi standar de-facto. DeepSeek, Ollama, vLLM, OpenRouter — semua support.

3. **Simple** — Chat Completion API cuma 1 endpoint, format sederhana.

4. **Debug friendly** — Request/response bisa di-log, di-inspect, di-test pake curl.

**Trade-off:**
- Gak ada retry logic, streaming, atau tool calling.
- Tapi untuk CLI tool yang blocking, ini gak masalah.

---

## 6️⃣ Kenapa system SSH, bukan library Python?

### Konteks
Bisa pake `paramiko` (SSH client library Python).

### Keputusan: ✅ System SSH (`subprocess` + `/usr/bin/ssh`)

**Alasan:**

1. **Feature parity** — System SSH punya semua fitur: key management, ProxyJump, agent forwarding, compression, dll.

2. **Zero dependency** — `paramiko` butuh `bcrypt`, `cryptography`, `pynacl`, dll.

3. **Familiar** — Semua konfigurasi SSH (known_hosts, config, agent) jalan otomatis.

4. **Interactive support** — `os.execvp()` bisa ngasih SSH session interaktif penuh. `paramiko` gak bisa seamless.

5. **Already configured** — User pasti udah setup SSH key di system-nya.

**Trade-off:**
- Gak bisa parse SSH output secara real-time.
- Error handling terbatas (cuma exit code).

---

## 7️⃣ Kenapa file-based state, bukan daemon?

### Konteks
Beberapa tool pake background daemon yang nyimpen state di memory.

### Keputusan: ✅ File-based (no daemon)

**Alasan:**

1. **Zero resource** — Gak ada background process. Gak consume RAM/CPU kalo gak dipake.

2. **Crash-proof** — Kalo terminal kill, data gak ilang. Semua di file.

3. **Transparent** — User bisa buka config langsung, edit pake editor teks.

4. **Simple** — Gak perlu manage process lifecycle, signal handling, lock files.

**Trade-off:**
- State dibaca dari disk setiap kali command → overhead dikit (<10ms).
- Gak bisa ada "real-time" notification.

---

## 8️⃣ Kenapa vault optional?

### Konteks
Vault butuh `cryptography` yang gak ada di stdlib.

### Keputusan: ✅ Optional — `cryptography` recommended, fallback tersedia

**Alasan:**

1. **Zero dep tetap berlaku** — Fitur dasar OpsTerm jalan tanpa vault.

2. **Security tetap prioritas** — Vault pake AES via cryptography. Fallback XOR + HMAC kalo gak ada.

3. **Progressive enhancement** — User bisa mulai tanpa vault, install cryptography kalo butuh.

---

## 9️⃣ Kenapa generated completion?

### Konteks
Completion bisa ditulis manual atau di-generate.

### Keputusan: ✅ Generated (embedded in script)

**Alasan:**

1. **Always up-to-date** — Kalo ada subcommand baru, completion otomatis update karena di-generate dari kode.

2. **Zero additional file** — `opsterm completion bash` langsung print ke stdout. Gak perlu file terpisah.

3. **Works out of box** — `source <(opsterm completion bash)` — 1 command, langsung jadi.

---

## 🔟 Kenapa Zsh plugin terpisah?

### Konteks
Shell integration bisa jadi bagian dari main script atau file terpisah.

### Keputusan: ✅ File terpisah (`zsh/opsterm.plugin.zsh`)

**Alasan:**

1. **Bahasa berbeda** — Zsh plugin pake Zsh script, bukan Python. Gabungin di file Python bakal campur aduk.

2. **Zsh-only** — Fitur shell hooks (`preexec`, `precmd`) cuma ada di Zsh.

3. **Lazy loading** — Plugin cuma di-load kalo user source di `.zshrc`. Gak nambah weight.

4. **Familiar pattern** — Zsh plugin format udah standar (oh-my-zsh, antigen, zplug).

---

## 💡 Saran untuk Improvement

Berdasarkan design decisions di atas, beberapa saran:

1. **Python → Rust (masa depan)** — Kalo performa & distribution jadi masalah, rewrite ke Rust buat single binary.

2. **YAML → TOML** — Kalo butuh config yang lebih strict (type safety), TOML lebih cocok. Tapi butuh library eksternal.

3. **Add plugin system** — Biar komunitas bisa nambah fitur tanpa edit core script.

4. **Support Fish shell** — Populer di kalangan developer modern.

---

## 🔗 Referensi

- [Python Argparse Docs](https://docs.python.org/3/library/argparse.html)
- [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat)
- [SSH ProxyJump (-J)](https://man.openai.com/man/ssh/ssh/)
- [Fernet (symmetric encryption)](https://cryptography.io/en/latest/fernet/)
- [PBKDF2 Key Derivation](https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac)
