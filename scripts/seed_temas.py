#!/usr/bin/env python3
"""Create seed theme MOC pages. Safe to re-run: does not overwrite existing files."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMAS = ROOT / "temas"
TODAY = "2026-08-19"

PAGES = [
    ("_inbox", "_inbox", "Vídeos ingeridos ainda sem classificação.", ["gabriel-kaminski", "farmacologia-geral"]),
    ("testosterona", "Testosterona", "TRT, eixos androgênicos, testosterona endógena e exógena.", ["ciclo-e-pct", "exames-e-saude", "gabriel-kaminski"]),
    ("peptideos", "Peptídeos", "Peptídeos em geral. Incretinas ficam em [[incretinas]].", ["incretinas", "farmacologia-geral", "gabriel-kaminski"]),
    ("incretinas", "Incretinas", "Retatrutida, tirzepatida, semaglutida, GLP-1 e metabolismo.", ["peptideos", "nutricao", "gabriel-kaminski"]),
    ("esteroides-aas", "Esteroides / AAS", "AAS, stacking, ciclos anabólicos.", ["ciclo-e-pct", "testosterona", "gabriel-kaminski"]),
    ("hormonio-de-crescimento", "Hormônio de crescimento", "GH e secretagogos.", ["peptideos", "exames-e-saude", "gabriel-kaminski"]),
    ("insulina", "Insulina", "Insulina, carboidrato, hipoglicemia.", ["nutricao", "exames-e-saude", "gabriel-kaminski"]),
    ("tireoide", "Tireoide", "T3, T4, TSH.", ["exames-e-saude", "farmacologia-geral", "gabriel-kaminski"]),
    ("ciclo-e-pct", "Ciclo e PCT", "Organização de ciclo e pós-ciclo.", ["esteroides-aas", "testosterona", "gabriel-kaminski"]),
    ("exames-e-saude", "Exames e saúde", "Labs, hematologia, segurança.", ["farmacologia-geral", "ciclo-e-pct", "gabriel-kaminski"]),
    ("treino", "Treino", "Periodização e hipertrofia.", ["nutricao", "gabriel-kaminski"]),
    ("nutricao", "Nutrição", "Dieta e suplementos alimentares.", ["treino", "insulina", "gabriel-kaminski"]),
    ("genetica", "Genética", "Polimorfismos e resposta individual.", ["farmacologia-geral", "gabriel-kaminski"]),
    ("mulher", "Mulher", "Farmacologia e preparo feminino.", ["testosterona", "exames-e-saude", "gabriel-kaminski"]),
    ("farmacologia-geral", "Farmacologia geral", "Mecanismos, PK/PD, aulas transversais.", ["gabriel-kaminski", "exames-e-saude"]),
]


def render(slug: str, title: str, blurb: str, links: list[str]) -> str:
    tags = "inbox" if slug == "_inbox" else slug.replace("-", "_")
    wikilinks = "\n".join(f"- [[{x}]]" for x in links)
    return f"""---
title: {title}
created: {TODAY}
updated: {TODAY}
type: concept
tags: [{tags}]
sources: []
confidence: medium
---

# {title}

{blurb}

Fonte: [[gabriel-kaminski]]

## Ligado a

{wikilinks}

## Vídeos

Nenhum ainda.
"""


def main() -> None:
    TEMAS.mkdir(parents=True, exist_ok=True)
    created = 0
    for slug, title, blurb, links in PAGES:
        path = TEMAS / f"{slug}.md"
        if path.exists():
            continue
        path.write_text(render(slug, title, blurb, links), encoding="utf-8")
        created += 1
        print(f"created {path.relative_to(ROOT)}")
    print(f"done created={created}")


if __name__ == "__main__":
    main()
