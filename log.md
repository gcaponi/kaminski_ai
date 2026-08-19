# Registro da wiki

> Registro cronológico, só acrescentar. Formato: `## [YYYY-MM-DD] ação | assunto`

## [2026-08-19] create | wiki inicializada

- Domínio: falas públicas de Gabriel Kaminski (farmacologia / bodybuilding)
- Repo: https://github.com/gcaponi/kaminski_ai
- Estrutura: SCHEMA, index, temas semente, entities, scripts de ingest
- Transcripts: 0
- Catálogo: `video.txt` — 265 URLs do YouTube (commit 9d11548)

## [2026-08-19] ingest | pipeline automática na VPS

- Método: `scripts/ingest_ytdlp.py` (yt-dlp + cookie Chrome Profile 3, `pt-orig`)
- Teste: 3/3 OK (MI4B18okOyY, hXCADESzQgM, Lq7Sa42QUWw)
- Catálogo restante: 262 vídeos. Job na VPS.

## [2026-08-19] escopo | só @kaminskilab/videos

- Ingest dos 265 interrompido (muitos Shorts/Reels sem conteúdo sério)
- `raw/transcripts/` esvaziada
- Novo catálogo: 67 vídeos de https://www.youtube.com/@kaminskilab/videos
- `video.txt` substituído. Lista humana em `catalog/kaminskilab-videos.md`

## [2026-08-19] ingest | 59/67 vídeos oficiais

- Transcripts pt-BR dos vídeos @kaminskilab/videos (parser com fechamento)
- Faltavam 8 IDs no fim do catálogo

## [2026-08-19] ingest | 67/67 vídeos oficiais

- Os 8 que faltavam, fechados
- `AdUQmiPvq5Q` (AS MENINAS NASCERAM): sem pt-orig, só ASR inglês fraco

## [2026-08-19] classify | regras automáticas

- `scripts/themes.py` + `scripts/classify.py` + `scripts/ingest_inbox.py`
- Gabriel deixa arquivo em `raw/inbox/` (PDF/PPT/Word/txt)
- 67 vídeos etiquetados; `_inbox` vazio depois da correção de acentos

## [2026-08-19] regra | tema desconhecido → perguntas ao Gabriel

- Ingest sem tema: não arquivar. Três perguntas em pt-BR. Arquivo fica em `raw/inbox/`, perguntas em `raw/inbox/perguntas/`.

## [2026-08-19] chore | limpeza da repo

- Removidos leftover: `catalog/video-urls.txt`, tsv, scripts de prova (cdp, seed, ingest_urls), README redundantes.

## [2026-08-19] speakers | Gabriel vs Franciele

- Handles: `@kaminskao` e `@drafrancieleconter` (via ASR Caminscão / dfrancelteror)
- 11 vídeos com `speaker: franciele-conter` (incl. n_4TkZXtqjY). Wikilink `[[franciele-conter]]`, não Gabriel.

## [2026-08-19] formato | transcript em prosa

- Removidos os timestamps `[00:00:00]`. Texto contínuo em parágrafos. Ingest novo já sai em prosa.

## [2026-08-19] agente | Milo + repo só pt-BR

- Nome do agente (e futuro bot Telegram): [[milo]] — ver `entities/milo.md`
- Docs, log, AGENTS e comentários dos scripts passados para português brasileiro
- Catálogo reescrito com os títulos pt-BR dos transcripts
