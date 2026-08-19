# Wiki Log

> Registro cronológico, só append. Formato: `## [YYYY-MM-DD] action | subject`

## [2026-08-19] create | Wiki initialized

- Domain: falas públicas de Gabriel Kaminski (farmacologia / bodybuilding)
- Repo: https://github.com/gcaponi/kaminski_ai
- Estrutura: SCHEMA, index, temas semente, entities, scripts de ingest
- Transcripts: 0
- Catalogo: `video.txt` — 265 URL YouTube unici (commit 9d11548)
## [2026-08-19] ingest | pipeline automatica VPS

- Metodo: `scripts/ingest_ytdlp.py` (yt-dlp + cookie Chrome Profile 3, `pt-orig`)
- Test: 3/3 OK (MI4B18okOyY, hXCADESzQgM, Lq7Sa42QUWw)
- Catalogo restante: 262 video. Job in corso sulla VPS.

## [2026-08-19] scope | solo @kaminskilab/videos

- Fermato ingest dei 265 (troppi Shorts/Reels senza contenuto serio)
- Svuotata `raw/transcripts/` (tenuto solo README)
- Nuovo catalogo: 67 video da https://www.youtube.com/@kaminskilab/videos
- `video.txt` sostituito. Lista umana in `catalog/kaminskilab-videos.md`

## [2026-08-19] ingest | 59/67 video ufficiali

- Transcripts PT-BR dei video @kaminskilab/videos (parser con chiusure)
- Mancano 8 ID in coda al catalogo

## [2026-08-19] ingest | 67/67 video ufficiali

- Chiusi gli 8 mancanti
- `AdUQmiPvq5Q` (AS MENINAS NASCERAM): niente pt-orig, solo ASR inglese scarsa

## [2026-08-19] classify | regole automatiche

- `scripts/themes.py` + `scripts/classify.py` + `scripts/ingest_inbox.py`
- Kaminski lascia file in `raw/inbox/` (PDF/PPT/Word/txt)
- 67 video etichettati; `_inbox` vuoto dopo correzione accenti

## [2026-08-19] rule | tema sconosciuto → domande a Gabriel

- Ingest senza tema: non archiviare. Chiedere 3 domande in PT. File resta in `raw/inbox/`, domande in `raw/inbox/perguntas/`.

## [2026-08-19] chore | pulizia repo

- Rimossi leftover: `catalog/video-urls.txt`, tsv, script di prova (cdp, seed, ingest_urls), README ridondanti.

## [2026-08-19] format | transcript in prosa

- Rimossi i timestamp `[00:00:00]`. Testo continuo a paragrafi. Ingest nuovi già in prosa.
