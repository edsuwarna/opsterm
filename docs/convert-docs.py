#!/usr/bin/env python3
"""Convert OpsTerm Markdown docs to HTML for Cloudflare Pages."""
import os
import re
import markdown

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))

# ── ToC Generator ──────────────────────────────────────
def generate_toc(html):
    """Extract h1/h2/h3 from HTML, assign IDs, return (html_with_ids, toc_html)."""
    toc_items = []
    seen_ids = {}

    def heading_replacer(m):
        tag = m.group(1)           # '1', '2', or '3'
        tag_name = f'h{tag}'     # 'h1', 'h2', 'h3'
        existing_id = m.group(2) or ""
        inner = m.group(3)
        attrs = m.group(2) or ""

        # Clean text for ID
        text = re.sub(r'<[^>]+>', '', inner)  # strip inner tags
        raw_id = text.lower().strip()
        raw_id = re.sub(r'[^a-z0-9]+', '-', raw_id).strip('-')
        raw_id = re.sub(r'-+', '-', raw_id)

        # Deduplicate
        if raw_id in seen_ids:
            seen_ids[raw_id] += 1
            raw_id = f"{raw_id}-{seen_ids[raw_id]}"
        else:
            seen_ids[raw_id] = 1

        # Add id attribute
        if 'id=' in existing_id:
            new_open = f'<{tag_name} {existing_id}'
        else:
            new_open = f'<{tag_name} id="{raw_id}"'

        # Collect for ToC
        level = int(tag)  # 1, 2, 3
        toc_items.append((level, raw_id, text))

        return new_open + '>' + inner + f'</{tag_name}>'

    # Match opening h1/h2/h3 with optional attributes
    html_fixed = re.sub(
        r'<h([123])([^>]*)>(.*?)</h\1>',
        heading_replacer,
        html,
        flags=re.DOTALL
    )

    # Build ToC HTML for right sidebar (simple links, no wrapper)
    if not toc_items:
        return html_fixed, ""
    toc_lines = []
    for level, hid, text in toc_items:
        cls = f'lvl-{level}'
        text_clean = re.sub(r'[🇬🇧🇮🇩📱🔀⚙️💾🌐📖🚀📁🧠🎯✨🔑🔐🔗⌨️🖼️📊📄📂]+', '', text).strip()
        if not text_clean:
            text_clean = text.strip()
        toc_lines.append(f'<a href="#{hid}" class="{cls}">{text_clean}</a>')
    return html_fixed, "\n".join(toc_lines)


# ── Document Navigation Bar ────────────────────────────
DOC_NAV_ITEMS = [
    ("📖", "Overview", "README.html"),
    ("📐", "Architecture", "architecture.html"),
    ("🔧", "Tech Stack", "tech-stack.html"),
    ("🤔", "Design Decisions", "design-decisions.html"),
    ("🎯", "Features", "features.html"),
]

def generate_sidebar_nav(current_basename):
    """Generate sidebar navigation with active highlight."""
    items_html = []
    for emoji, label, href in DOC_NAV_ITEMS:
        target_base = href.replace('.html', '')
        active = ' active' if target_base == current_basename else ''
        items_html.append(
            f'<a href="{href}" class="{active}">'
            f'{emoji} {label}</a>'
        )
    # Add diagram link
    items_html.append(
        '<a href="../ops-term-architecture.png" target="_blank">'
        '🖼️ Diagram</a>'
    )
    return "\n".join(items_html)


# ── CSS for Doc Nav ────────────────────────────────────
TOC_CSS = '''
/* ── Theme ── */
:root {
  --bg: #0d1117; --bg2: #161b22; --bg3: #1c2128; --border: #30363d;
  --text: #e6edf3; --text2: #8b949e; --text3: #484f58;
  --accent: #58a6ff; --green: #3fb950;
  --code-bg: #151b23;
}
[data-theme="light"] {
  --bg: #ffffff; --bg2: #f6f8fa; --bg3: #eef1f5; --border: #d0d7de;
  --text: #1f2328; --text2: #656d76; --text3: #afb8c1;
  --accent: #0969da; --green: #1a7f37;
  --code-bg: #f6f8fa;
}
html { scroll-behavior: smooth; }
body {
  font-family: 'Segoe UI', -apple-system, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.7;
  margin: 0; padding: 0; transition: background 0.2s, color 0.2s;
}
.layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 240px; background: var(--bg2);
  border-right: 1px solid var(--border);
  position: fixed; top: 0; left: 0; height: 100vh; overflow-y: auto; z-index: 100;
  transition: background 0.2s;
}
.sidebar-header {
  padding: 20px 16px; border-bottom: 1px solid var(--border);
  font-weight: 700; font-size: 16px;
  background: linear-gradient(135deg,var(--accent),var(--green));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sidebar-back {
  display: flex; align-items: center; gap: 6px; padding: 12px 16px;
  color: var(--accent); text-decoration: none; font-size: 13px; font-weight: 500;
  border-bottom: 1px solid var(--border); transition: background 0.2s;
}
.sidebar-back:hover { background: var(--bg3); }
.sidebar-label { padding: 12px 16px 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text2); }
.sidebar-nav { padding: 4px 0; }
.sidebar-nav a {
  display: block; padding: 6px 16px; color: var(--text2); text-decoration: none;
  font-size: 13px; border-left: 2px solid transparent; transition: all 0.15s;
}
.sidebar-nav a:hover { color: var(--text); background: var(--bg3); }
.sidebar-nav a.active { color: var(--accent); border-left-color: var(--accent); background: #1f6feb11; }
.sidebar::-webkit-scrollbar { width: 5px; }
.sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

.theme-toggle {
  position: fixed; top: 12px; right: 12px; z-index: 200;
  background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
  width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;
  cursor: pointer; font-size: 16px; transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.theme-toggle:hover { background: var(--bg3); }

.content { flex: 1; margin-left: 240px; padding: 32px 48px; max-width: 860px; }

h1 { font-size: 28px; margin: 20px 0 10px; }
h2 { font-size: 22px; margin: 30px 0 12px; padding-bottom: 6px; border-bottom: 2px solid var(--border); }
h3 { font-size: 18px; margin: 20px 0 8px; }
p { margin: 10px 0; }
code {
  background: var(--bg3); padding: 2px 6px; border-radius: 4px;
  font-size: 0.9em; font-family: 'Cascadia Code', 'Fira Code', monospace;
}
pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px 20px; margin: 12px 0 20px; overflow-x: auto; }
pre code { display: block; background: none; border: none; padding: 0; color: var(--text); font-size: 13px; }
pre code .comment { color: var(--text2); }
table { width: 100%; border-collapse: collapse; margin: 15px 0; }
th, td { border: 1px solid var(--border); padding: 10px 14px; text-align: left; font-size: 14px; }
th { background: var(--bg3); font-weight: 600; }
tr:nth-child(even) td { background: var(--bg2); }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
ul, ol { margin: 10px 0; padding-left: 24px; }
li { margin: 4px 0; }
hr { border: none; border-top: 2px solid var(--border); margin: 30px 0; }
blockquote { border-left: 4px solid var(--accent); padding: 10px 16px; margin: 15px 0; background: var(--bg3); border-radius: 0 6px 6px 0; }
blockquote p { margin: 0; }
img { max-width: 100%; border-radius: 8px; border: 1px solid var(--border); }

/* ── Right TOC ── */
.right-toc {
  position: fixed; top: 0; right: 0; width: 200px;
  height: 100vh; overflow-y: auto; padding: 24px 12px;
  border-left: 1px solid var(--border);
  background: var(--bg);
  transition: background 0.2s;
  display: none;
}
.right-toc-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text2); margin-bottom: 10px; padding-left: 4px; }
.right-toc a { display: block; padding: 3px 8px; font-size: 12px; color: var(--text2); text-decoration: none; border-left: 2px solid transparent; transition: all 0.15s; }
.right-toc a:hover { color: var(--text); }
.right-toc a.active { color: var(--accent); border-left-color: var(--accent); }
.right-toc a.lvl-2 { padding-left: 8px; }
.right-toc a.lvl-3 { padding-left: 20px; font-size: 11.5px; }
.right-toc::-webkit-scrollbar { width: 4px; }
.right-toc::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
@media (min-width: 1300px) { .right-toc { display: block; } .content { max-width: 720px; padding: 32px 64px 32px 48px; } }
@media (min-width: 1500px) { .right-toc { width: 230px; } }

/* ── Page TOC (top box, hidden — moved to right) ── */
.page-toc { display: none; } padding: 10px 16px; margin: 15px 0; background: var(--bg3); border-radius: 0 6px 6px 0; }
blockquote p { margin: 0; }
img { max-width: 100%; border-radius: 8px; border: 1px solid var(--border); }

.footer { text-align: center; padding: 30px 0 10px; font-size: 13px; color: var(--text3); border-top: 1px solid var(--border); margin-top: 40px; }
.footer a { color: var(--accent); }

@media (max-width: 900px) {
  .sidebar { transform: translateX(-100%); transition: transform 0.3s; }
  .sidebar.open { transform: translateX(0); }
  .sidebar-overlay.open { display: block; }
  .sidebar-toggle { display: block; }
  .content { margin-left: 0; padding: 24px 20px; max-width: 100%; }
}
.sidebar-toggle { display: none; position: fixed; top: 12px; left: 12px; z-index: 200; background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; cursor: pointer; font-size: 20px; color: var(--text); }
.sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 99; }
'''# ── HTML Template ──────────────────────────────────────
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="{lang}" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — OpsTerm</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
{TOC_CSS}
</style>
</head>
<body>
<button class="sidebar-toggle" id="sidebarToggle">☰</button>
<div class="sidebar-overlay" id="sidebarOverlay"></div>
<button class="theme-toggle" id="themeToggle" title="Toggle theme">🌙</button>

<div class="layout">
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">OpsTerm</div>
        <a href="../index.html" class="sidebar-back">← Back to Home</a>
        <div class="sidebar-label">Documentation</div>
        <div class="sidebar-nav">
            {sidebar_nav}
        </div>
    </nav>

    <main class="content">
        {content}

        <div class="footer">
            <p><a href="https://github.com/edsuwarna/opsterm">OpsTerm</a> · MIT License</p>
        </div>
    </main>

    <aside class="right-toc" id="rightToc">
        <div class="right-toc-label">📑 On this page</div>
        <div id="rightTocLinks">
            {toc}
        </div>
    </aside>
</div>

<script>
function getTheme() {{{{ return document.documentElement.getAttribute(\'data-theme\'); }}}}
function setTheme(theme) {{{{
    document.documentElement.setAttribute(\'data-theme\', theme);
    localStorage.setItem(\'ops-term-theme\', theme);
    document.getElementById(\'themeToggle\').textContent = theme === \'dark\' ? \'🌙\' : \'☀️\';
}}}}
function toggleTheme() {{{{ setTheme(getTheme() === \'dark\' ? \'light\' : \'dark\'); }}}}
document.getElementById(\'themeToggle\').addEventListener(\'click\', toggleTheme);
const saved = localStorage.getItem(\'ops-term-theme\');
if (saved) setTheme(saved);

function toggleSidebar() {{{{
    document.getElementById(\'sidebar\').classList.toggle(\'open\');
    document.getElementById(\'sidebarOverlay\').classList.toggle(\'open\');
}}}}
document.getElementById('sidebarToggle').onclick = toggleSidebar;
document.getElementById('sidebarOverlay').onclick = toggleSidebar;

// ── Right TOC active tracking ──
function setupTOC() {{
    const links = document.querySelectorAll('#rightTocLinks a');
    if (!links.length) return;
    const observer = new IntersectionObserver((entries) => {{
        let visible = null;
        entries.forEach(e => {{ if (e.isIntersecting) visible = e.target.id; }});
        if (visible) {{
            links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + visible));
        }}
    }}, {{ rootMargin: '-80px 0px -60% 0px' }});
    links.forEach(l => {{
        const id = l.getAttribute('href').slice(1);
        const el = document.getElementById(id);
        if (el) observer.observe(el);
    }});
}}
setupTOC();
</script>

</body>
</html>'''# ── Link Fixer ──────────────────────────────────────────
def fix_links(html, lang_prefix):
    """Fix internal .md links to .html, adjust paths."""
    def replace_link(m):
        href = m.group(1)
        if href.startswith("http"):
            return m.group(0)
        if href.endswith(".md"):
            href = href[:-3] + ".html"
        if href.startswith("../id/"):
            href = "../" + href[3:] if lang_prefix == "en" else href[3:]
        elif href.startswith("id/") and lang_prefix == "id":
            href = href[3:]
        elif href.startswith("../"):
            pass
        return f'href="{href}"'

    html = re.sub(r'href="([^"]+)"', replace_link, html)
    return html


# ── Single File Converter ──────────────────────────────
def convert_md_to_html(filepath):
    """Convert a single .md file to .html with ToC."""
    dirname = os.path.dirname(filepath)
    basename = os.path.splitext(os.path.basename(filepath))[0]
    parent_dir = os.path.basename(dirname)

    with open(filepath, 'r') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'codehilite', 'nl2br']
    )

    # Fix links
    html_body = fix_links(html_body, parent_dir)

    # Generate ToC from headings
    html_body, toc_html = generate_toc(html_body)

    # Generate doc navigation bar
    sidebar_nav_html = generate_sidebar_nav(basename)

    # Get title from first H1
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_body)
    title = title_match.group(1) if title_match else basename.replace('-', ' ').title()

    lang_code = 'id' if parent_dir == 'id' else 'en'

    # Escape braces in content for .format() safety
    html_body_safe = html_body.replace('{', '{{').replace('}', '}}')
    toc_safe = toc_html.replace('{', '{{').replace('}', '}}')
    sidebar_safe = sidebar_nav_html.replace('{', '{{').replace('}', '}}')
    title_safe = title.replace('{', '{{').replace('}', '}}')

    html_full = HTML_TEMPLATE.format(
        lang=lang_code,
        title=title_safe,
        toc=toc_safe,
        sidebar_nav=sidebar_safe,
        TOC_CSS=TOC_CSS,
        content=html_body_safe
    )

    out_path = os.path.join(dirname, basename + '.html')
    with open(out_path, 'w') as f:
        f.write(html_full)
    print(f"  ✓ {out_path}")
    return out_path


def update_index_links():
    """Update docs/index.html to link to .html instead of .md"""
    index_path = os.path.join(DOCS_DIR, 'index.html')
    with open(index_path, 'r') as f:
        content = f.read()

    content = content.replace('href="en/README.md"', 'href="en/README.html"')
    content = content.replace('href="id/README.md"', 'href="id/README.html"')

    with open(index_path, 'w') as f:
        f.write(content)
    print(f"  ✓ Updated index.html links")


# ── Main ───────────────────────────────────────────────
if __name__ == '__main__':
    print("📝 Converting OpsTerm documentation .md → .html (with ToC)")
    print()

    for subdir in ['en', 'id']:
        dirpath = os.path.join(DOCS_DIR, subdir)
        if not os.path.isdir(dirpath):
            continue
        print(f"--- {subdir}/ ---")
        for fname in sorted(os.listdir(dirpath)):
            if fname.endswith('.md') and not fname.startswith('.'):
                convert_md_to_html(os.path.join(dirpath, fname))

    print()
    print("📝 Updating index.html links...")
    update_index_links()

    print()
    print("✅ Done! All .md files converted to .html with Table of Contents")
