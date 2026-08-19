# Kaminski AI

Vault-wiki delle **trascrizioni** di [Gabriel Kaminski](https://www.youtube.com/@kaminskilab) (PhD, farmacologia).

Due lettori, un solo repo:

- **Guglielmo** — apre la cartella come vault Obsidian sul laptop
- **Fama / Hermes** — lavora sulla VPS, classifica, tiene il grafo

**Repo:** https://github.com/gcaponi/kaminski_ai

Lingua del contenuto: **portoghese brasiliano**. I transcript non si traducono.

---

## Cosa entra (e cosa no)

Entra **solo** il tab video lunghi del canale ufficiale:

https://www.youtube.com/@kaminskilab/videos

Oggi: **67 video** (elenco in `video.txt` e `catalog/kaminskilab-videos.md`).

**Non entra:**

- Shorts / Reels / clip da 30–90 secondi
- video di altri canali, podcast ospite, tagli
- consigli clinici scritti da Fama: qui si archivia quello che ha detto Kaminski, con link

---

## Come lavoriamo

1. Fama aggiorna `video.txt` dal tab `/videos` e scarica i transcript **dalla VPS** (automatico).
2. Tu fai `git pull` e apri questa cartella in Obsidian.
3. I temi (`temas/`) collegano i video con `[[wikilink]]`. Un video può stare su più temi. Il testo integrale sta **una volta sola** in `raw/transcripts/`.

```bash
git clone git@github.com:gcaponi/kaminski_ai.git
# Obsidian → Open folder as vault → cartella del clone
git pull
```

Non serve lanciare script sul laptop.

---

## Struttura

| Percorso | Ruolo |
|---|---|
| `SCHEMA.md` | Regole della wiki. Leggerlo prima di toccare una nota. |
| `AGENTS.md` | Istruzioni per Hermes. |
| `index.md` | Catalogo delle pagine wiki. |
| `log.md` | Diario, solo append. |
| `video.txt` | URL dei 67 video ufficiali. |
| `catalog/kaminskilab-videos.md` | Stessa lista, con titolo e durata. |
| `raw/transcripts/` | Una nota per video. PT-BR. Immutabile dopo l'ingest. |
| `temas/` | Mappe di contenuto (testosterona, peptídeos, AAS, …). Qui nasce il grafo. |
| `entities/gabriel-kaminski.md` | Pagina autore. |
| `scripts/ingest_ytdlp.py` | Ingest automatico (yt-dlp + cookie Chrome VPS). |

---

## Ingest (solo VPS)

YouTube blocca gli IP da datacenter. Sulla VPS usiamo i cookie del Chrome già loggato (Profile 3), un caption `pt-orig` per video, con pausa anti-429.

```bash
python scripts/ingest_ytdlp.py video.txt
```

Il parser tiene anche le ultime parole del caption (le auto-caption YouTube le lasciano solo sull’ultimo cue).

---

## Grafo Obsidian

Il grafo nasce dai `[[wikilink]]`, non dalle cartelle.

Esempio: un video su testosterona **e** peptídeos resta un file in `raw/transcripts/` e punta a `[[testosterona]]` e `[[peptideos]]`.
