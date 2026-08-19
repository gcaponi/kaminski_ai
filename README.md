# Kaminski AI

Vault Obsidian + base do agente **[[milo]]**. Conteúdo e arquivos operacionais em **português brasileiro**.

**Repo:** https://github.com/gcaponi/kaminski_ai

---

## Onde fica cada coisa

| O quê | Onde |
|---|---|
| Transcrições do YouTube | `raw/transcripts/<id-do-video>.md` — texto integral, uma vez só |
| Arquivos que Gabriel deixa (PDF, Word, PPT, txt) | ele solta em `raw/inbox/` → depois do ingest viram `raw/docs/<nome>.md` |
| Temas (AAS, peptídeos, …) | `temas/<tema>.md` — **não** copiam o texto; listam os `[[link]]` |
| Pessoas | `entities/gabriel-kaminski.md`, `entities/franciele-conter.md` |
| O agente | `entities/milo.md` |

O texto não se duplica. Um vídeo sobre GH e peptídeos continua **um** arquivo em `raw/transcripts/` e aponta para os dois temas.

---

## O que cria o grafo do Obsidian

**Os `[[wikilink]]`**, não as pastas.

Nós:

- cada nota em `raw/transcripts/` e `raw/docs/`
- cada página em `temas/`
- `entities/gabriel-kaminski.md`, `entities/franciele-conter.md`, `entities/milo.md`

Arestas: a linha `- Temas: [[peptideos]] · [[incretinas]]` e as listas `## Vídeos` dentro de `temas/`.

No Obsidian: Open folder as vault → Graph view.

---

## Para o Kaminski

Ler `PARA-O-KAMINSKI.md`. Em resumo: arraste arquivos para `raw/inbox/`. Se o [[milo]] não reconhecer o tema, faz 3 perguntas.

---

## Scripts (só o agente / VPS)

- `scripts/ingest_ytdlp.py` — YouTube
- `scripts/ingest_inbox.py` — arquivos da inbox
- `scripts/classify.py` — etiquetas + atualiza `temas/`
- `scripts/themes.py` — regras dos temas
