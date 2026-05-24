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

    # Build ToC HTML
    if not toc_items:
        return html_fixed, ""

    toc_lines = ['<nav class="page-toc">',
                 '<div class="toc-title">📑 On this page</div>',
                 '<ul>']
    for level, hid, text in toc_items:
        indent = "  " * (level - 1)
        cls = 'toc-h1' if level == 1 else 'toc-h2' if level == 2 else 'toc-h3'
        text_clean = re.sub(r'[🇬🇧🇮🇩📱🔀⚙️💾🌐📖🚀📁🧠🎯✨🔑🔐🔗⌨️🖼️📊📄📂]+', '', text).strip()
        if not text_clean:
            text_clean = text.strip()
        toc_lines.append(f'{indent}<li class="{cls}"><a href="#{hid}">{text_clean}</a></li>')
    toc_lines.append('</ul>')
    toc_lines.append('</nav>')

    return html_fixed, "\n".join(toc_lines)


# ── CSS ────────────────────────────────────────────────
TOC_CSS = '''
/* ── Table of Contents ── */
.page-toc {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-left: 4px solid #1971c2;
  border-radius: 8px;
  padding: 16px 20px;
  margin: 0 0 30px 0;
}
.page-toc .toc-title {
  font-size: 14px;
  font-weight: 700;
  color: #1971c2;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.page-toc ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.page-toc li {
  margin: 3px 0;
  line-height: 1.5;
}
.page-toc li.toc-h1 { padding-left: 0; }
.page-toc li.toc-h2 { padding-left: 18px; }
.page-toc li.toc-h3 { padding-left: 36px; }
.page-toc li a {
  font-size: 14px;
  color: #495057;
  text-decoration: none;
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.15s;
}
.page-toc li a:hover {
  background: #e8f4fd;
  color: #1971c2;
}
/* Sticky ToC for wide screens */
@media (min-width: 1200px) {
  .page-toc {
    position: fixed;
    top: 24px;
    right: 24px;
    width: 240px;
    max-height: calc(100vh - 48px);
    overflow-y: auto;
    z-index: 100;
    margin: 0;
    background: rgba(255,255,255,0.97);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  .container { max-width: 800px; }
}
@media (min-width: 1400px) {
  .page-toc { width: 280px; }
}
@media (max-width: 1199px) {
  .page-toc { position: static; width: auto; }
}
'''

# ── HTML Template ──────────────────────────────────────
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — OpsTerm</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: 'Segoe UI', -apple-system, sans-serif;
  background: #f8f9fa;
  color: #1a1a2e;
  line-height: 1.7;
  padding: 20px;
}}
.container {{
  max-width: 860px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 40px 48px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  border: 1px solid #e9ecef;
}}
h1 {{ font-size: 28px; margin: 20px 0 10px; }}
h2 {{ font-size: 22px; margin: 30px 0 12px; padding-bottom: 6px; border-bottom: 2px solid #e9ecef; }}
h3 {{ font-size: 18px; margin: 20px 0 8px; }}
p {{ margin: 10px 0; }}
code {{
  background: #f1f3f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Cascadia Code', 'Fira Code', monospace;
}}
pre code {{
  display: block;
  background: #1a1a2e;
  color: #e9ecef;
  padding: 16px 20px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.6;
}}
pre code .comment {{ color: #6c757d; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
}}
th, td {{
  border: 1px solid #dee2e6;
  padding: 10px 14px;
  text-align: left;
  font-size: 14px;
}}
th {{ background: #f1f3f5; font-weight: 600; }}
tr:nth-child(even) td {{ background: #f8f9fa; }}
a {{ color: #1971c2; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
ul, ol {{ margin: 10px 0; padding-left: 24px; }}
li {{ margin: 4px 0; }}
hr {{ border: none; border-top: 2px solid #e9ecef; margin: 30px 0; }}
blockquote {{
  border-left: 4px solid #1971c2;
  padding: 10px 16px;
  margin: 15px 0;
  background: #f1f3f5;
  border-radius: 0 6px 6px 0;
}}
blockquote p {{ margin: 0; }}
img {{ max-width: 100%; border-radius: 8px; border: 1px solid #e9ecef; }}
.nav-back {{
  display: inline-block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #888;
}}
.nav-back:hover {{ color: #1971c2; }}
.footer {{
  text-align: center;
  padding: 30px 0 10px;
  font-size: 13px;
  color: #888;
  border-top: 1px solid #e9ecef;
  margin-top: 40px;
}}
.footer a {{ color: #1971c2; }}
{TOC_CSS}
</style>
</head>
<body>
<div class="container">

<p class="nav-back"><a href="../index.html">← Back to OpsTerm</a></p>

{toc}

{content}

<div class="footer">
  <p><a href="https://github.com/edsuwarna/opsterm">OpsTerm</a> · MIT License</p>
</div>

</div>
</body>
</html>'''


# ── Link Fixer ──────────────────────────────────────────
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

    # Get title from first H1
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_body)
    title = title_match.group(1) if title_match else basename.replace('-', ' ').title()

    lang_code = 'id' if parent_dir == 'id' else 'en'

    html_full = HTML_TEMPLATE.format(
        lang=lang_code,
        title=title,
        toc=toc_html,
        TOC_CSS=TOC_CSS,
        content=html_body
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
