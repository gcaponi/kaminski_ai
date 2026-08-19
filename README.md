# Kaminski AI

Vault-wiki delle trascrizioni di **Gabriel Kaminski** (PT-BR), usata da:

- Guglielmo, in Obsidian sul laptop
- Fama / Hermes, sulla VPS

Stesso repo, stesso grafo. Nessun file sulla Scrivania.

**Repo:** https://github.com/gcaponi/kaminski_ai

## Come lavoriamo

1. I link sono in `video.txt` (265 URL).
2. Io (VPS) scarico i transcript, classifico, pusho.
3. Tu fai pull e apri questa cartella come vault Obsidian.

```bash
git pull
# sul laptop: Obsidian → Open folder as vault → cartella del clone
```

## Cosa c'è dentro

| Percorso | Ruolo |
|---|---|
| `SCHEMA.md` | Regole. Leggerlo prima di toccare qualsiasi nota. |
| `index.md` | Catalogo di tutte le pagine wiki. |
| `log.md` | Diario append-only. |
| `video.txt` | Lista dei 265 video da ingerire. |
| `raw/transcripts/` | Una nota per video. Testo integrale PT-BR. Immutabile. |
| `temas/` | Mappe di contenuto (un file per tema). Qui nasce il grafo. |
| `entities/` | Persone / canali. |
| `scripts/` | Ingest dei transcript. |

Un video parla spesso di più temi: la trascrizione sta **una sola volta** in `raw/transcripts/`. I temi la collegano con `[[wikilink]]`. Niente copie.

## Prima azione (tu)

```bash
git clone git@github.com:gcaponi/kaminski_ai.git
# Obsidian → Open folder as vault → cartella del clone
```
