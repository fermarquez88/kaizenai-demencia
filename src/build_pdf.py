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
/* --- Paleta Nature (referencia CAN): azul acero + rojo ladrillo + navy --- */
:root{
  --ink:#1c1c1c; --navy:#22415f; --steel:#3f6a9c; --brick:#b0463c;
  --muted:#6c6c6c; --rule:#141414; --hair:#e8e8e8; --emph:#eaf0f6; --cream:#f7f0dd;
}
@page { size: A4; margin: 19mm 17mm; }
* { box-sizing: border-box; }
body { font-family:'Helvetica Neue','Helvetica','Arial',sans-serif; font-size:10pt; line-height:1.5;
       color:var(--ink); max-width:100%; -webkit-font-smoothing:antialiased; }
h1 { font-size:17pt; line-height:1.22; font-weight:750; letter-spacing:-.01em;
     color:var(--navy); border-bottom:2px solid var(--steel); padding-bottom:7px; margin:0 0 12px; text-wrap:balance; }
h2 { font-size:12.5pt; font-weight:730; color:var(--navy); margin:20px 0 6px;
     border-bottom:1px solid #dde4ec; padding-bottom:3px; page-break-after:avoid; }
h3 { font-size:10.6pt; font-weight:700; color:#2c2c2c; margin:13px 0 4px; page-break-after:avoid; }
p { margin:5px 0; text-align:justify; }
strong { color:var(--navy); font-weight:700; }
blockquote { border-left:3px solid var(--brick); margin:9px 0; padding:3px 13px; color:#555;
             font-size:8.9pt; background:#faf7f2; }
/* --- Tablas estilo Nature: sin líneas verticales, reglas finas arriba/abajo del encabezado --- */
table { border-collapse:collapse; width:100%; margin:13px 0 5px; font-size:8.6pt; page-break-inside:avoid; }
thead th { border-top:1.4px solid var(--rule); border-bottom:1px solid var(--rule);
           padding:6px 9px; text-align:left; font-weight:700; color:var(--navy); vertical-align:bottom;
           letter-spacing:.005em; }
tbody td { padding:5px 9px; border-bottom:1px solid var(--hair); vertical-align:top;
           font-variant-numeric:tabular-nums; }
tbody tr:last-child td { border-bottom:1.4px solid var(--rule); }
tbody tr td:first-child { color:var(--ink); }
img { max-width:96%; height:auto; display:block; margin:10px auto 4px; page-break-inside:avoid; }
hr { border:none; border-top:1px solid #d8d8d8; margin:18px 0; }
/* pies de tabla y epígrafes de figura (líneas en cursiva): gris pequeño estilo Nature */
table + p em, img + em, p > em:only-child { color:var(--muted); font-size:8.4pt; }
em { color:#4a4a4a; }
code { font-family:'SF Mono',Consolas,monospace; font-size:8.8pt; color:#333; }
ol,ul { margin:5px 0 5px 18px; padding:0; } li { margin:2px 0; }
ol { font-size:9.2pt; }
h2 + p, h3 + p { page-break-before:avoid; }
a { color:var(--steel); text-decoration:none; }
"""
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
hp = os.path.join(REPO, "MANUSCRIPT.html"); open(hp, "w", encoding="utf-8").write(html)

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
out = os.path.join(REPO, "MANUSCRIPT.pdf")
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={out}", f"file://{hp}"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("OK:", out, os.path.getsize(out), "bytes")
