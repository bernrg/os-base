# REGRAS — escrita e conexão do segundo cérebro

Ler antes de **criar ou reestruturar** nota. Não é sempre-ligado (fora do núcleo do doctor).

## Anatomia de uma nota

- **Frontmatter obrigatório** — schema único, 5 campos:
  ```yaml
  tipo:     conhecimento        # projeto|conhecimento|diario|semana|melhoria|pack|cruzamento
  dominio:  [os-pessoal]        # lista; vocabulário fechado (ver fim)
  forma:    [gargalo]           # lista; vocabulário fechado (ver fim)
  criado:   2026-07-21          # AAAA-MM-DD
  status:   semente             # semente|ativa|madura|dormente
  ```
- **Título é afirmação, não tópico:** `# O gargalo do site é a foto do produto, não o texto` — nunca `# Site`.
- **Uma ideia por nota.** Se o título pede "e", provavelmente são duas notas.
- **Primeiro parágrafo se sustenta sozinho** — legível fora de qualquer contexto, sem depender do título.

## Nota, memória ou skill

Desempate: *"Isto muda como você deve agir?"* → memória. *"É conhecimento para reler?"* → nota. *"É procedimento verificado?"* → skill.

- **Memória** (`brain/memoria/`): "o fornecedor só responde por e-mail"; "o deploy do site só sai depois do teste no celular"; "nunca `git add -A` na raiz". Muda comportamento na hora.
- **Nota** (`brain/notas/`): "como a loja define o preço de cada linha"; "o caminho do cliente até o pedido"; "por que não vender para atacado no início". Conhecimento para reler.
- **Skill** (`.claude/skills/`): "ritual de fim de sessão"; "carimbo de projeto novo"; "deploy verificado". Procedimento multi-passo provado.
- **Casos-limite:** decisão datada de projeto → `## Histórico` da nota, não nota nova. Fato que *também* muda comportamento → memória **e** linha na nota; a memória é o dono.

## Linkar, tagar ou embutir

- **`[[wikilink]]`** = relação entre duas ideias. É o default.
- **`#tag`** = eixo transversal que corta domínios (`#alavanca`, `#cliente`). Nunca taxonomia profunda (`#site/produto/foto` é proibido).
- **`![[embed]]`** = só para o trecho que precisa ser *lido no lugar*. Custa contexto; na dúvida, linke.

## Conexões especulativas

Elo **provado** é `[[wikilink]]` na prosa. Elo **não-provado** é bullet numa seção `## Elos especulativos`, marcado com `#elo-especulativo`:

```
## Elos especulativos
- [[preco-por-linha]] — e se o gargalo do atendimento for o mesmo gargalo de capacidade do estoque? #elo-especulativo
```

- **Promover:** a relação se sustentou → mover para a prosa como `[[wikilink]]`, remover a tag.
- **Descartar:** não se sustentou → apagar a linha.

O `/clash` sempre nasce especulativo. O doctor (check 10) cobra elos parados — nem promovidos, nem descartados.

## Nomenclatura

- Slug **kebab-case**: `foto-do-produto.md`.
- **Sem data no nome**, exceto `diario/` e `semanas/` (`2026-07-21.md`).
- **Sem numeração hierárquica** (`01-`, `1.2-`). A estrutura vive nos links, não no nome.

## O que NÃO vira nota

- **Estado corrente** ("site no ar, falta o domínio") → `STATUS.md`, dono único.
- **Cronologia de sessão** ("mexi no doctor hoje") → `git log`.
- **Atrito da sessão** (erro, correção, permissão negada) → ledger de melhoria.

Nota é o que você relê daqui a 3 meses e ainda vale.

## Vocabulário fechado

`dominio` e `forma` casam ideias entre notas. Adicionar termo = editar os blocos abaixo (o `doctor` e o `bin/nota` leem daqui — dono único do vocabulário). O bloco de `dominio` nasce só com os dois termos do próprio OS: os seus domínios (áreas da sua vida e do seu trabalho) entram na instalação e conforme aparecerem.

<!-- VOCAB:dominio -->
os-pessoal metodo
<!-- /VOCAB:dominio -->

<!-- VOCAB:forma -->
gargalo-de-capacidade gargalo-de-decisao gargalo-de-informacao ciclo-de-feedback tradeoff alavanca restricao arbitragem
<!-- /VOCAB:forma -->

`forma` é a **estrutura abstrata** do problema, não o assunto: é um **gargalo** (de **capacidade**? de **decisao**? de **informacao**?)? um **tradeoff**? um **ciclo-de-feedback**? uma **alavanca**? uma **restricao**? uma **arbitragem**? Mesma `forma` + `dominio` diferente = candidato a cruzamento — e por isso o gargalo é fatiado pelo objeto que ele estrangula (capacidade de produção, decisão/aprovação, fluxo de informação): dois gargalos do mesmo tipo em domínios distintos é que rende cruzamento, "gargalo" solto não.

**No máximo uma `forma` dominante por nota.** A dominante é a estrutura que o **título afirma** e vem **primeiro** na lista; formas seguintes entram só como qualificação (ex.: `[gargalo-de-decisao, restricao]` — o gargalo é o quadro, a restrição é o detalhe). Se duas formas disputam o papel central, provavelmente são **duas notas** (ver "Uma ideia por nota").
