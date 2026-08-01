"""Construye MANUSCRIPT.pdf desde MANUSCRIPT.md (markdown -> HTML -> Chrome headless -> PDF)."""
import subprocess, sys, os, re
try:
    import markdown
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "markdown"], check=True)
    import markdown

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md = open(os.path.join(REPO, "MANUSCRIPT.md"), encoding="utf-8").read()
body = markdown.markdown(md, extensions=["tables", "sane_lists", "attr_list"])

CSS = """
@page { size: A4; margin: 20mm 18mm; }
* { box-sizing: border-box; }
body { font-family: 'Charter','Georgia',serif; font-size: 10.3pt; line-height: 1.5;
       color:#1a1a1a; max-width: 100%; }
h1 { font-family:'Helvetica Neue',Arial,sans-serif; font-size: 16pt; line-height:1.25;
     color:#0b3b3f; border-bottom:2px solid #0b6b70; padding-bottom:6px; margin:0 0 10px; }
h2 { font-family:'Helvetica Neue',Arial,sans-serif; font-size: 12.5pt; color:#0b6b70;
     margin:18px 0 6px; border-bottom:1px solid #d5e2e2; padding-bottom:3px; page-break-after:avoid; }
h3 { font-family:'Helvetica Neue',Arial,sans-serif; font-size: 10.8pt; color:#123; margin:12px 0 4px; page-break-after:avoid; }
p { margin: 5px 0; text-align: justify; }
strong { color:#0b3b3f; }
blockquote { border-left:3px solid #b6602c; margin:8px 0; padding:2px 12px; color:#555;
             font-size:9.3pt; background:#faf6f2; }
table { border-collapse: collapse; width:100%; margin:8px 0; font-size:8.9pt; page-break-inside:avoid; }
th,td { border:1px solid #c9d6d6; padding:4px 7px; text-align:left; vertical-align:top; }
th { background:#eef4f4; font-family:'Helvetica Neue',Arial,sans-serif; color:#0b3b3f; }
img { max-width: 92%; height:auto; display:block; margin:8px auto; page-break-inside:avoid; }
hr { border:none; border-top:1px solid #ccc; margin:16px 0; }
em { color:#444; }
code { font-family:'SF Mono',Consolas,monospace; font-size:9pt; }
ol,ul { margin:5px 0 5px 18px; padding:0; } li { margin:2px 0; }
h2 + p, h3 + p { page-break-before: avoid; }
"""
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
hp = os.path.join(REPO, "MANUSCRIPT.html"); open(hp, "w", encoding="utf-8").write(html)

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
out = os.path.join(REPO, "MANUSCRIPT.pdf")
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={out}", f"file://{hp}"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("OK:", out, os.path.getsize(out), "bytes")
