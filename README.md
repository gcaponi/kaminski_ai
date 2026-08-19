# Kaminski AI

Vault-wiki delle trascrizioni di **Gabriel Kaminski** (PT-BR), usata da:

- Guglielmo, in Obsidian sul laptop
- Fama / Hermes, sulla VPS

Stesso repo, stesso grafo. Nessun file sulla Scrivania.

**Repo:** https://github.com/gcaponi/kaminski_ai

## Come lavoriamo

1. I link sono in `video.txt` — **solo i video di** [youtube.com/@kaminskilab/videos](https://www.youtube.com/@kaminskilab/videos). Niente Shorts/Reels.
2. Fama scarica i transcript **dalla VPS**, in automatico (yt-dlp + cookie del Chrome già loggato). Tu non lanci nulla.
3. Tu fai `git pull` e apri la cartella come vault Obsidian.

```bash
git clone git@github.com:gcaponi/kaminski_ai.git
# Obsidian → Open folder as vault → cartella del clone
git pull
```

## Cosa c'è dentro

| Percorso | Ruolo |
|---|---|
| `SCHEMA.md` | Regole. Leggerlo prima di toccare qualsiasi nota. |
| `index.md` | Catalogo di tutte le pagine wiki. |
| `log.md` | Diario append-only. |
| `video.txt` | Lista ufficiale @kaminskilab/videos (67 video, no Shorts). |
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
