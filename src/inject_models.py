"""Inyecta models/models_deploy.json dentro del bloque `const MODELS = {...};` de index.html.
La app es 100% client-side (GitHub Pages + CSP): los coeficientes van embebidos, no por fetch.
Correr tras reentrenar (build_deploy_final.py / deploy_final_v2.py) para que la calculadora en vivo
use los modelos actuales. Idempotente."""
import json, os, re
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()
data = json.load(open(os.path.join(REPO, "models", "models_deploy.json"), encoding="utf-8"))

marker = "const MODELS = {"
i = html.index(marker)
j = i + len(marker) - 1              # posición del '{' que abre el objeto
depth = 0
for k in range(j, len(html)):        # brace-matching (el JSON no tiene llaves dentro de strings)
    if html[k] == '{': depth += 1
    elif html[k] == '}':
        depth -= 1
        if depth == 0:
            end = k
            break
new_block = "const MODELS = " + json.dumps(data, ensure_ascii=False, indent=1)
html2 = html[:i] + new_block + html[end + 1:]
open(os.path.join(REPO, "index.html"), "w", encoding="utf-8").write(html2)

# verificación
d = json.loads(new_block[len("const MODELS = "):])
for kk in ["demencia_dlm", "demencia_dclleve", "declive_fiable"]:
    v = d[kk]
    print(f"{kk:18s} n={v['n']} ev={v['eventos']} AUC={v['metrics']['auc']} coef={v['coef']} boots={len(v.get('bootstrap',[]))}")
print("claves:", list(d.keys()))
print("OK: index.html inyectado (bytes:", len(html2), ")")
