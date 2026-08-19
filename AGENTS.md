# AGENTS.md — Kaminski AI

Workspace: vault-wiki delle trascrizioni di Gabriel Kaminski.

## Prima di qualsiasi operazione

1. Leggere `SCHEMA.md`
2. Leggere `index.md`
3. Leggere le ultime 20–30 righe di `log.md`
4. Cercare pagine esistenti prima di crearne di nuove

## Lingua

- Transcript e note wiki: **portoghese brasiliano**
- File operativi (`README.md`, questo file): italiano
- Non tradurre i transcript

## Regole dure

- `raw/transcripts/` è immutabile. Mai modificare il corpo dopo l'ingest.
- Una trascrizione = un file. Mai duplicarla dentro le cartelle tema.
- Classificazione = wikilink verso `temas/*.md` (minimo 1, spesso 2+).
- Ogni pagina wiki ha frontmatter YAML e almeno 2 `[[wikilink]]`.
- Ogni ingest aggiorna `index.md` e appende a `log.md`.
- Tag solo dalla tassonomia in `SCHEMA.md`.
- Non inventare claim farmacologici. Se non è nel transcript, non sta nella wiki.
- Non dare dosaggi, protocolli o consigli clinici in voce dell'agente. Citare Kaminski e la nota.

## Ingest

Automatico. YouTube: `scripts/ingest_ytdlp.py`. File lasciati in `raw/inbox/`: `scripts/ingest_inbox.py` poi `scripts/classify.py`.

Classificare solo con `scripts/themes.py` (tassonomia chiusa). Se manca un tema, aggiungerlo lì e in SCHEMA.md prima di usarlo.

Poi aggiornare `index.md` e `log.md`.

## Query

Rispondere sintetizzando le note wiki e i transcript, con `[[wikilink]]` alle fonti. Se la vault non copre la domanda, dirlo.
