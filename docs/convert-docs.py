#!/usr/bin/env python3
"""Convert OpsTerm Markdown docs to HTML for Cloudflare Pages."""
import os
import re
import markdown

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(DOCS_DIR)

# HTML template with OpsTerm branding
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
  margin-bottom: 20px;
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
</style>
</head>
<body>
<div class="container">

<p class="nav-back"><a href="../index.html">← Back to OpsTerm</a></p>

{content}

<div class="footer">
  <p><a href="https://github.com/edsuwarna/opsterm">OpsTerm</a> · MIT License</p>
</div>

</div>
</body>
</html>'''

def fix_links(html, lang_prefix):
    """Fix internal .md links to .html, adjust paths."""
    # Internal links: (../id/ or en/ or id/)  -> adjust
    def replace_link(m):
        href = m.group(1)
        if href.startswith("http"):
            return m.group(0)
        if href.endswith(".md"):
            # Convert .md to .html
            href = href[:-3] + ".html"
        if href.startswith("../id/"):
            # From en/ -> id/../id/ -> id/
            href = "../" + href[3:] if lang_prefix == "en" else href[3:]
        elif href.startswith("id/") and lang_prefix == "id":
            href = href[3:]
        elif href.startswith("../"):
            pass  # keep as is
        return f'href="{href}"'
    
    html = re.sub(r'href="([^"]+)"', replace_link, html)
    return html

def convert_md_to_html(filepath, lang):
    """Convert a single .md file to .html."""
    dirname = os.path.dirname(filepath)
    basename = os.path.splitext(os.path.basename(filepath))[0]
    
    with open(filepath, 'r') as f:
        md_content = f.read()
    
    # Determine language prefix for link fixing
    parent_dir = os.path.basename(dirname)
    
    # Convert markdown to HTML with extra features
    html_body = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'codehilite', 'nl2br']
    )
    
    # Fix links
    html_body = fix_links(html_body, parent_dir)
    
    # Get title from first H1
    title_match = re.search(r'<h1>(.*?)</h1>', html_body)
    title = title_match.group(1) if title_match else basename.replace('-', ' ').title()
    
    # Determine lang attribute
    lang_code = 'id' if parent_dir == 'id' else 'en'
    
    # Wrap in template
    html_full = HTML_TEMPLATE.format(
        lang=lang_code,
        title=title,
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
    
    # Fix links from .md to .html
    content = content.replace('href="en/README.md"', 'href="en/README.html"')
    content = content.replace('href="id/README.md"', 'href="id/README.html"')
    
    with open(index_path, 'w') as f:
        f.write(content)
    print(f"  ✓ Updated index.html links")

# Main
print("📝 Converting OpsTerm documentation .md → .html")
print()

# Walk through en/ and id/ directories
for subdir in ['en', 'id']:
    dirpath = os.path.join(DOCS_DIR, subdir)
    if not os.path.isdir(dirpath):
        continue
    print(f"--- {subdir}/ ---")
    for fname in sorted(os.listdir(dirpath)):
        if fname.endswith('.md') and not fname.startswith('.'):
            convert_md_to_html(os.path.join(dirpath, fname), subdir)

print()
print("📝 Updating index.html links...")
update_index_links()

print()
print("✅ Done! All .md files converted to .html")
