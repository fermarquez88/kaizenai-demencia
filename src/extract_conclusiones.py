"""
Corpus de CONCLUSIONES (perfil neuropsicológico) para el estudio de reevaluaciones.

Materia prima para codificar el `perfil` como variable. Determinístico y
auditable: por cada evaluación de un paciente con >=2 episodios (excl. pediátrico
WISC-V), localiza el PDF del informe firmado, extrae la sección "Conclusiones"
(y "Recomendaciones") verbatim vía extract_narrative, y escribe un CSV keyed por
eval_id/persona_id/t_orden.

NO codifica el perfil todavía: eso es una pasada aparte, con codebook validado.
"""
import os, re, csv, sys, unicodedata
import duckdb
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from extract_narrative import process as narr_process

DB = "db/evaluaciones_v2.duckdb"
OUT = "data/interim/conclusiones_reeval.csv"

def _norm(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', s.lower())

def _dates(s):
    return set(re.findall(r'\d{6,8}', s))

def find_pdf(xlsx_path):
    """Devuelve (pdf_path|None, metodo)."""
    d = os.path.dirname(xlsx_path)
    stem = os.path.splitext(os.path.basename(xlsx_path))[0]
    if not os.path.isdir(d):
        return None, 'nodir'
    pdfs = [f for f in os.listdir(d) if f.lower().endswith('.pdf')]
    # excluir formularios de admisión / consentimientos (NO son el informe)
    rep = [f for f in pdfs if not re.search(r'formulario|consentimiento|cuestionario|autoriz', f, re.I)]
    if not rep:
        return None, 'no_pdf'
    nstem = _norm(stem)
    for f in rep:  # 1) match exacto de stem normalizado
        if _norm(os.path.splitext(f)[0]) == nstem:
            return os.path.join(d, f), 'exact'
    if len(rep) == 1:  # 2) único candidato de informe
        return os.path.join(d, rep[0]), 'single'
    dst = _dates(stem)  # 3) match por token de fecha en el nombre
    if dst:
        cands = [f for f in rep if _dates(os.path.splitext(f)[0]) & dst]
        if len(cands) == 1:
            return os.path.join(d, cands[0]), 'date'
    return None, f'ambiguous({len(rep)})'

def main():
    con = duckdb.connect(DB, read_only=True)
    # cohorte de reevaluaciones: >=2 episodios, excl. pediátrico; excluir la
    # persona anómala (n_episodios==72 = colisión de carpeta)
    rows = con.execute("""
        SELECT e.eval_id, e.persona_id, e.folder, e.path, e.fecha_ev, e.year,
               e.cohorte, e.has_pdf_struct, p.n_episodios
        FROM evaluaciones_v2 e JOIN personas p USING(persona_id)
        WHERE p.n_episodios >= 2 AND p.n_episodios < 60 AND e.cohorte <> 'wisc_v'
        ORDER BY e.persona_id, e.fecha_ev
    """).fetchall()
    cols = [c[0] for c in con.description]
    con.close()
    recs = [dict(zip(cols, r)) for r in rows]

    # t_orden e intervalo por persona (por fecha_ev ISO; None al final)
    from collections import defaultdict
    by_p = defaultdict(list)
    for r in recs:
        by_p[r['persona_id']].append(r)
    for pid, lst in by_p.items():
        lst.sort(key=lambda r: (r['fecha_ev'] is None, r['fecha_ev'] or ''))
        f0 = next((r['fecha_ev'] for r in lst if r['fecha_ev']), None)
        for i, r in enumerate(lst, 1):
            r['t_orden'] = i
            r['n_tomas'] = len(lst)

    out_fields = ['eval_id', 'persona_id', 'folder', 'fecha_ev', 'year', 'cohorte',
                  't_orden', 'n_tomas', 'pdf_metodo', 'pdf_file', 'has_conclusiones',
                  'n_chars_concl', 'conclusiones', 'recomendaciones', 'antecedentes']
    stats = defaultdict(int)
    written = 0
    with open(OUT, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields, extrasaction='ignore')
        w.writeheader()
        for r in recs:
            pdf, metodo = find_pdf(r['path'])
            r['pdf_metodo'] = metodo
            r['pdf_file'] = os.path.basename(pdf) if pdf else ''
            stats[f'pdf_{metodo.split("(")[0]}'] += 1
            concl = reco = ante = ''
            if pdf:
                try:
                    nr = narr_process(pdf)
                    sec = nr['secciones']
                    concl = sec.get('conclusiones', '') or ''
                    reco = sec.get('recomendaciones', '') or ''
                    ante = sec.get('antecedentes', '') or ''
                except Exception as e:
                    stats['narr_error'] += 1
                    r['pdf_metodo'] = f'{metodo}|err:{type(e).__name__}'
            r['conclusiones'] = concl.strip()
            r['recomendaciones'] = reco.strip()
            r['antecedentes'] = ante.strip()
            r['has_conclusiones'] = bool(concl.strip())
            r['n_chars_concl'] = len(concl.strip())
            if concl.strip():
                stats['con_conclusiones'] += 1
            w.writerow(r)
            written += 1
            if written % 100 == 0:
                print(f'  ... {written}/{len(recs)}', file=sys.stderr)

    print(f'\nEscrito: {OUT}  ({written} evals)')
    print('Cohorte:', len(by_p), 'personas /', len(recs), 'evals')
    print('Cobertura:')
    for k in sorted(stats):
        print(f'  {k:24s} {stats[k]}')

if __name__ == '__main__':
    main()
