"""Shared theme rules for automatic classification.

Deterministic: same text → same labels. Hermes and a future laptop
agent must agree. Add a pattern here BEFORE using a new theme.
"""

from __future__ import annotations

import re

# slug -> (weight, compiled patterns). Title hits count 3x.
THEME_PATTERNS: dict[str, list[str]] = {
    "esteroides-aas": [
        r"\bboldenon",
        r"\bmasteron",
        r"primobolan",
        r"dianabol",
        r"trembolon",
        r"turinabol",
        r"oxandrolon",
        r"esteroide",
        r"ester[oó]ide",
        r"\baas\b",
        r"anabol",
        r"stacking",
    ],
    "peptideos": [
        r"pept[ií]d",
        r"pt-?141",
        r"bremelanotide",
        r"selank",
        r"semax",
        r"kisspeptin",
        r"mots-?c",
        r"cjc-?1295",
        r"ipamorelin",
        r"ghrp",
        r"tesamorelin",
        r"elamipretide",
        r"ss-?31",
        r"bioglutid",
        r"igf-?1",
    ],
    "incretinas": [
        r"incretin",
        r"ozempic",
        r"mounjaro",
        r"monjaro",
        r"retatrutid",
        r"tirzepatid",
        r"semaglutid",
        r"glp-?1",
        r"\bpyy\b",
        r"pept[ií]deo yy",
        r"bari[aá]tric",
    ],
    "hormonio-de-crescimento": [
        r"\bgh\b",
        r"crescimento",
        r"secretagog",
        r"ghrp",
        r"tesamorelin",
        r"cjc-?1295",
        r"ipamorelin",
        r"igf-?1",
    ],
    "testosterona": [
        r"testosteron",
        r"\btrt\b",
        r"\bhcg\b",
        r"gonadotrofina",
        r"androgen",
        r"eixo (hipot|androg)",
    ],
    "tireoide": [
        r"tireoid",
        r"thyroid",
        r"\bt3\b",
        r"\bt4\b",
        r"\btsh\b",
    ],
    "insulina": [
        r"insulin",
        r"hipoglicem",
        r"hypoglyc",
    ],
    "ciclo-e-pct": [
        r"\bpct\b",
        r"p[oó]s-ciclo",
        r"ciclo anab",
        r"taper",
    ],
    "exames-e-saude": [
        r"exame",
        r"hematolog",
        r"cardiovascular",
        r"cora[cç][aã]o",
        r"heart",
        r"laborat",
        r"seguran[cç]a",
    ],
    "treino": [
        r"treino",
        r"workout",
        r"leg day",
        r"chest workout",
        r"hipertrof",
        r"shape de pai",
        r"dad shape",
        r"pacho",
        r"franciscon",
    ],
    "nutricao": [
        r"prote[ií]na",
        r"protein",
        r"creatina",
        r"caf[eé]",
        r"coffee",
        r"suplement",
        r"dieta",
        r"nutri[cç]",
        r"comida",
        r"geladeira",
        r"alimento",
        r"refrigerator",
    ],
    "genetica": [
        r"gen[eé]tic",
        r"polimorf",
        r"snp\b",
    ],
    "mulher": [
        r"mulher",
        r"gesta[cç]",
        r"gravidez",
        r"gr[aá]vid",
        r"pregnant",
        r"menopausa",
        r"climat[eé]rio",
        r"estrog[eê]nio",
        r"estrogen",
        r"maternidade",
        r"motherhood",
        r"libido",
    ],
    "longevidade": [
        r"longevid",
        r"longevity",
        r"klotho",
        r"sirt",
        r"sir2",
        r"\bnnmt\b",
        r"nattokinase",
        r"melatonina",
        r"irisina",
        r"adiponectin",
        r"leptina",
    ],
    "pessoal": [
        r"nasceram",
        r"meninas",
        r"fomos para casa",
        r"went home",
        r"our girls",
    ],
    "farmacologia-geral": [
        r"comprimido ou injet",
        r"pills or injection",
        r"farmacolog",
        r"termog[eê]nese",
        r"thermogenesis",
        r"interleucina",
        r"inflama",
        r"regenera",
        r"retin[oó]id",
        r"mecanismo",
        r"pk/pd",
        r"via de administra",
    ],
}

COMPILED: dict[str, list[re.Pattern[str]]] = {
    slug: [re.compile(p, re.I) for p in pats] for slug, pats in THEME_PATTERNS.items()
}

THEME_SLUGS = [s for s in THEME_PATTERNS if s != "_inbox"]


def score_text(title: str, body: str) -> dict[str, int]:
    scores: dict[str, int] = {}
    title = title or ""
    body = body or ""
    for slug, pats in COMPILED.items():
        s = 0
        for pat in pats:
            if pat.search(title):
                s += 3
            if pat.search(body):
                s += 1
        if s:
            scores[slug] = s
    return scores


def pick_themes(title: str, body: str, max_themes: int = 3, min_score: int = 3) -> list[str]:
    scores = score_text(title, body)
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    chosen = [slug for slug, sc in ranked if sc >= min_score][:max_themes]
    return chosen or ["_inbox"]
