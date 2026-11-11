---
tipo: conhecimento
dominio: [os-pessoal]
forma: []
criado: {{HOJE}}
status: madura
---

# Plugins do Obsidian para o vault

Regra dura: **todo arquivo continua markdown puro, legível pelo Claude Code via Read/Grep sem nenhum plugin.** Plugin que cria formato proprietário está **vetado** (Canvas visual à parte, nunca como dono de conhecimento). Nenhum plugin é fonte de verdade — só conforto.

## Essenciais (≤6)

1. **Templates (core)** — insere os templates de `brain/templates/`. Config: *Settings → Core plugins → Templates → Template folder = `brain/templates`*. Serve ao cruzamento porque garante `forma`/`dominio` em toda nota nova (sem eles, nada casa).
2. **Backlinks (core)** — painel de links de entrada. Config: *ativar; "Backlinks in document" ligado*. É onde um cruzamento vira visível: a nota aparece no rodapé da outra.
3. **Outgoing links (core)** — o espelho: para onde esta nota aponta. Ativar. Fecha o par com o backlink.
4. **Tag pane (core)** — lista as tags; clicar em `#gargalo`/`#alavanca` reúne notas da mesma `forma` entre domínios. Ativar.
5. **Graph view (core)** — grafo. Config: *colorir grupos por `dominio` (group: `path:brain/notas/projetos` etc.)*; filtrar por tag de `forma` para ver clusters de estrutura cruzando domínios.
6. **Dataview (comunidade)** — o único essencial de comunidade. As queries de `brain/notas/painel.md`. Config: *Settings → Dataview → "Enable JavaScript Queries" ligado* (o gerador de par do painel usa dataviewjs). Continua tudo markdown; se removido, o painel degrada para os fallbacks de terminal.

## Opcionais

- **Templater** — só se a captura <30s virar atrito por preencher `dominio`/`forma` à mão. Justificativa: prompta valores na inserção. **Fallback obrigatório:** todo template segue legível e válido sem ele (os `{{date}}` do core continuam funcionando). Não adotar sem essa dor real.
- **Breadcrumbs** — hierarquias explícitas entre notas; útil se o grafo virar sopa. Opcional.
