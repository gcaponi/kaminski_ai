# Kaminski AI

Vault Obsidian + base per l’agente Hermes. Contenuto in **portoghese brasiliano**.

**Repo:** https://github.com/gcaponi/kaminski_ai

---

## Dove vanno le informazioni

| Cosa | Dove |
|---|---|
| Trascrizioni YouTube | `raw/transcripts/<id-video>.md` — testo integrale, una volta sola |
| File che Kaminski lascia (PDF, Word, PPT, txt) | li mette in `raw/inbox/` → dopo l’ingest diventano `raw/docs/<nome>.md` |
| Temi (AAS, peptídeos, …) | `temas/<tema>.md` — **non** copiano il testo; elencano i `[[link]]` |
| Autore | `entities/gabriel-kaminski.md` |

Il testo non si duplica. Un video su GH e peptídeos resta **un** file in `raw/transcripts/` e punta a due temi.

---

## Cosa crea il grafo Obsidian

**I `[[wikilink]]`**, non le cartelle.

Nodi:

- ogni nota in `raw/transcripts/` e `raw/docs/`
- ogni pagina in `temas/`
- `entities/gabriel-kaminski.md`

Archi: la riga `- Temas: [[peptideos]] · [[incretinas]]` e le liste `## Vídeos` dentro `temas/`.

In Obsidian: Open folder as vault → Graph view.

---

## Per Kaminski

Leggere `PARA-O-KAMINSKI.md`. In sintesi: trascina file in `raw/inbox/`. Se l’agente non riconosce il tema, gli fa 3 domande.

---

## Script (solo agente / VPS)

- `scripts/ingest_ytdlp.py` — YouTube
- `scripts/ingest_inbox.py` — file in inbox
- `scripts/classify.py` — etichette + aggiorna `temas/`
- `scripts/themes.py` — regole dei temi
