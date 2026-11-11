---
description: Choca o assunto da conversa corrente contra o vault inteiro à procura de relação não-óbvia e oportunidade. Somente leitura — só escreve nota-de-cruzamento com aprovação.
---

# /clash — cross-pollination sob demanda

Ferramenta central de cruzamento: pega o assunto do momento e o choca contra `brain/notas/**` e `brain/memoria/**` procurando a relação que você não veria sozinho. Roda no meio do trabalho.

## Invocação

- `/clash` — o assunto é **inferido** da conversa (últimas mensagens + projeto ativo no STATUS.md). Antes de buscar, declarar em **uma linha** qual assunto foi inferido, para {{NOME}} corrigir.
- `/clash <tema>` — tema explícito; substitui a inferência.
- `/clash <tema> --dominio=<x>` — restringe o lado do vault ao domínio `x`.
- `/clash --forma=<f>` — busca só por estrutura abstrata, ignorando o assunto.

## Algoritmo

1. **DESTILAR** — reduzir o assunto a: 1 frase do que é; 2–4 termos de busca; 1–3 tags de `forma` (é um gargalo? um tradeoff? um ciclo de feedback?). **Mostrar isso antes de seguir.**
2. **RECRUTAR** — três buscas independentes sobre `brain/notas/**` e `brain/memoria/**`, no máx. 12 candidatas:
   - (a) **termos literais** — `.claude/bin/nota <termos>`, `.claude/bin/memoria <termos>` e `grep -ri` como reforço.
   - (b) **mesma forma, domínio DIFERENTE** — `.claude/bin/nota --forma=<f> --dominio-diferente-de=<dom-do-assunto>`. **É a busca que gera o valor.**
   - (c) **uma dormente sorteada** — dentre `.claude/bin/nota --status=dormente` (variar a escolha pelo índice, sem `Math.random`).
3. **CHOCAR** — para cada candidata, formular a tensão em uma frase: onde ela **contradiz**, **reforça** ou sugere **transposição** para o assunto corrente. Descartar sem dó o que só tem semelhança lexical de vocabulário — semelhança de palavra não é relação.
4. **RANQUEAR** — manter no máx. **5**, ordenadas por **quão pouco óbvia** é a relação. Mesmo domínio / mesmo projeto vai para o fim ou é cortado.
5. **REPORTAR** — no chat, formato fixo por item, sem preâmbulo e sem resumir o que já sei:
   `[[nota]] — <a tensão em uma frase> → <o que sugere fazer ou pensar>`
6. **OFERECER** — terminar perguntando se algum par vira nota-de-cruzamento em `brain/notas/cruzamentos/`. **Nunca escrever arquivo sem resposta.**

## Regras

- **Somente leitura por padrão.** Não escreve, não comita, não toca no STATUS.md, não cria memória. Única escrita possível: a nota-de-cruzamento aprovada no passo 6.
- **Nunca ler `brain/privado/` nem `arquivo/`** — nem para "contexto interno".
- **Vault vazio ou sem match:** dizer isso em uma linha e parar. Proibido inventar conexão para preencher o formato — resultado vazio é válido.
- **Assunto trivial ou operacional** (rodar comando, corrigir typo): recusar em uma linha em vez de chocar.
- **Custo de contexto:** ler só frontmatter + primeiro parágrafo das candidatas; abrir a nota inteira apenas das 5 finalistas.

## Escrita da nota-de-cruzamento (passo 6, se aprovado)

- Usar `brain/templates/cruzamento.md`: nasce `tipo: cruzamento`, `status: semente`, `dominio:` com os domínios envolvidos, `criado:` hoje.
- As conexões propostas entram como **link especulativo** (seção `## Elos especulativos`, tag `#elo-especulativo`, ver `brain/REGRAS.md`). Só viram `[[wikilink]]` na prosa depois que {{NOME}} confirmar que a relação se sustenta.
- Não comitar — o commit é do `/fim`, depois da revisão.

## Aceite

- Assunto plantado com relação conhecida no vault → a nota certa aparece no top 5.
- Assunto sem nenhuma relação → retorna vazio, não força conexão.
