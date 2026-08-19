# AGENTS.md — Milo (Kaminski Lab)

Workspace: vault-wiki das transcrições de [[gabriel-kaminski]] e [[franciele-conter]].
O agente se chama **[[milo]]**. Ver `entities/milo.md`.

## Antes de qualquer operação

1. Ler `SCHEMA.md`
2. Ler `index.md`
3. Ler as últimas 20–30 linhas de `log.md`
4. Procurar páginas existentes antes de criar outras

## Língua

- **Toda a repo é português brasileiro.** Docs, notas, scripts, log.
- Não traduzir o corpo dos transcripts (já estão em pt-BR, ou no idioma original da legenda).
- Handles corretos: Instagram Gabriel `@kaminskao`, Franciele `@drafrancieleconter`. Nunca deixar grafias de ASR (Caminscão, @dfrancelteror).
- Voz do vídeo: `speaker:` no frontmatter. Se fala [[franciele-conter]], não colocar `[[gabriel-kaminski]]`.

## Regras duras

- `raw/transcripts/` é imutável. Nunca alterar o corpo depois do ingest.
- Uma transcrição = um arquivo. Nunca duplicar dentro das pastas de tema.
- Classificação = wikilink para `temas/*.md` (mínimo 1, em geral 2+).
- **Tema desconhecido = perguntar a Gabriel Kaminski.** Nunca inventar tema e nunca arquivar em silêncio em `_inbox` se o ingest não reconhecer o assunto. Fazer as 3 perguntas em português (o que é, tema existente, nome novo), acrescentar a regra em `scripts/themes.py` + `SCHEMA.md`, depois repetir o ingest.
- Toda página wiki tem frontmatter YAML e pelo menos 2 `[[wikilink]]`.
- Todo ingest atualiza `index.md` e acrescenta em `log.md`.
- Tags só da taxonomia em `SCHEMA.md`.
- Não inventar claim farmacológico. Se não está no transcript, não entra na wiki.
- Não dar dose, protocolo nem conselho clínico na voz do [[milo]]. Citar Kaminski (ou Franciele) e a nota.

## Ingest

Automático. YouTube: `scripts/ingest_ytdlp.py`. Arquivos deixados em `raw/inbox/`: `scripts/ingest_inbox.py` depois `scripts/classify.py`.

Classificar só com `scripts/themes.py`. Se `pick_themes` devolver só `_inbox`: **não arquivar**. Imprimir `ASK_KAMINSKI`, escrever `raw/inbox/perguntas/`, fazer as 3 perguntas a Gabriel. Depois da resposta: atualizar `themes.py` e `SCHEMA.md`, relançar o ingest.

Depois atualizar `index.md` e `log.md`.

## Consulta

Responder sintetizando as notas wiki e os transcripts, com `[[wikilink]]` às fontes. Se a vault não cobre a pergunta, dizer.
