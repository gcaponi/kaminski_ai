# Wiki Schema

## Domain

Conhecimento publicado por **Gabriel Kaminski** (PhD em ciências farmacêuticas) em vídeo: farmacologia hormonal, preparo de bodybuilding, peptídeos, exames e limites do que o dado permite dizer.

Não é prontuário clínico. Não é protocolo. É um arquivo das falas dele, classificado para busca humana (Obsidian) e agente (Hermes).

## Conventions

- File names: lowercase, hyphens, no spaces (`testosterona.md`, `2024-05-18-farmacologia-esportiva.md`)
- Transcripts: `raw/transcripts/<youtube-id>.md` — um arquivo por vídeo, **imutável**
- Temas: `temas/<slug>.md` — mapa de conteúdo, sem copiar o transcript
- Entities: `entities/<slug>.md`
- Toda página wiki começa com YAML frontmatter
- Ligar com `[[wikilinks]]` (mínimo 2 outbound por página wiki)
- Ao atualizar uma página, subir o campo `updated`
- Toda página nova entra em `index.md` na seção certa
- Toda ação entra em `log.md`
- Idioma do conteúdo: **pt-BR**. Não traduzir transcripts.

## Frontmatter — páginas wiki (`temas/`, `entities/`)

```yaml
---
title: Título
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query
tags: []
sources: []
confidence: high | medium | low
---
```

## Frontmatter — transcripts (`raw/transcripts/`)

```yaml
---
source_url: https://www.youtube.com/watch?v=VIDEO_ID
youtube_id: VIDEO_ID
title: Título original do vídeo
channel: Nome do canal
published: YYYY-MM-DD
ingested: YYYY-MM-DD
language: pt-BR
duration_s: 0
temas: []
sha256: <hex do corpo depois do frontmatter>
---
```

`temas:` lista slugs que existem em `temas/`. Um vídeo pode ter vários. Isso alimenta o grafo.

## Tag taxonomy

Usar só estas tags. Se faltar uma, acrescentar aqui primeiro.

- Pessoas/canais: `pessoa`, `canal`
- Hormônios: `testosterona`, `aesh`, `gh`, `insulina`, `tireoide`, `estradiol`
- Compostos: `peptideo`, `incretina`, `retatrutida`, `aas`, `sarms`
- Prática: `ciclo`, `pct`, `treino`, `nutricao`, `exames`, `mulher`, `longevidade`, `pessoal`
- Meta: `farmacologia`, `genetica`, `limite`, `controversia`, `clip`, `podcast`

## Page thresholds

- **Criar página de tema** quando 2+ vídeos falarem do assunto, ou quando o assunto for central em um vídeo longo
- **Não criar** página para menção de passagem
- **Não copiar** o transcript para dentro de `temas/`
- **Dividir** uma página wiki acima de ~200 linhas
- **Inbox:** se le regole non riconoscono o assunto, **não arquivar em silêncio**. O agente pergunta a Gabriel Kaminski (3 perguntas em PT) e só então cria o tema ou aplica um existente.

## Temas semente

| Slug | Pasta/arquivo | Quando usar |
|---|---|---|
| `_inbox` | `temas/_inbox.md` | ainda não classificado |
| `testosterona` | `temas/testosterona.md` | TRT, androgênios, eixos |
| `peptideos` | `temas/peptideos.md` | peptídeos em geral (exceto incretinas) |
| `incretinas` | `temas/incretinas.md` | retatrutida, tirzepatida, semaglutida, GLP-1 |
| `esteroides-aas` | `temas/esteroides-aas.md` | AAS, stacking, ciclos anabólicos |
| `hormonio-de-crescimento` | `temas/hormonio-de-crescimento.md` | GH, secretagogos |
| `insulina` | `temas/insulina.md` | insulina, carboidrato, hipoglicemia |
| `tireoide` | `temas/tireoide.md` | T3/T4, TSH |
| `ciclo-e-pct` | `temas/ciclo-e-pct.md` | organização de ciclo, PCT |
| `exames-e-saude` | `temas/exames-e-saude.md` | labs, hematologia, segurança |
| `treino` | `temas/treino.md` | periodização, hipertrofia |
| `nutricao` | `temas/nutricao.md` | dieta, suplementos alimentares |
| `genetica` | `temas/genetica.md` | polimorfismos, resposta individual |
| `mulher` | `temas/mulher.md` | farmacologia / preparo feminino |
| `farmacologia-geral` | `temas/farmacologia-geral.md` | mecanismos, PK/PD, aula transversal |
| `longevidade` | `temas/longevidade.md` | Klotho, SIRT, NNMT, longevidade |
| `pessoal` | `temas/pessoal.md` | vlog, família — não é aula |

## Update policy

Quando um vídeo novo contradiz um antigo:

1. Não apagar a fala antiga
2. Registrar as duas posições com data e `[[youtube-id]]`
3. Marcar `contested: true` na página de tema
4. Anotar em `log.md`

## Grafo Obsidian

O grafo nasce dos `[[wikilinks]]`, não das pastas.

- Transcript `[[testosterona]]` e `[[peptideos]]` → o vídeo aparece ligado aos dois temas
- Página de tema lista os vídeos e conceitos vizinhos
- `entities/gabriel-kaminski.md` liga o autor a todos os temas
