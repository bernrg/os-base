---
tipo: conhecimento
dominio: [os-pessoal]
forma: [ciclo-de-feedback]
criado: {{HOJE}}
status: madura
---

# Os cinco mecanismos que forçam contato entre domínios

Cruzamento não acontece por vontade — acontece por mecanismo. Cinco, todos sobre a estrutura que já existe. O casador principal é sempre o eixo `forma` do frontmatter: **mesma `forma` + `dominio` diferente = candidato**. O artefato de saída é sempre a **nota-de-cruzamento** (`brain/notas/cruzamentos/`), que registra o par, a tensão e o que ela sugere. Nenhum mecanismo escreve no STATUS.md.

## 1. `/clash` — sob demanda (o ativo)

No meio do trabalho, `/clash` choca o assunto corrente contra o vault. É o único sob demanda; os outros quatro são passivos ou agendados. Ver `.claude/commands/clash.md`.

## 2. Bloco de cruzamento forçado na retro semanal — ritual

O `/retrospectiva` (domingo, ou quando o `doctor` cobrar) escreve `brain/notas/semanas/AAAA-MM-DD.md` com a seção `## Cruzamento forçado` do template, obrigando um par de domínios diferentes por semana. Quem acha o par é o `/clash --forma=<f>` — a retrospectiva não reimplementa a busca.

## 3. Query "mesma forma, domínio diferente" — passivo (plugin)

Bloco 2 de `brain/notas/painel.md`: lista notas agrupadas por `forma`; onde a mesma forma cruza domínios distintos, há par candidato. Degrada para `.claude/bin/nota --forma=<f>`.

## 4. "Sexta do cruzamento" — ritual manual semanal, sem plugin

5 minutos, sexta: rodar `.claude/bin/nota --forma=<f>` (ou o gerador de par do painel), pegar duas notas de domínios diferentes e escrever a tensão à mão. Zero dependência de plugin — funciona só com o script e um editor de texto.

## 5. Tag transversal de `forma` — passivo, nativo do Obsidian

Toda nota carrega `forma` no frontmatter e pode espelhá-la como `#gargalo`/`#tradeoff` no corpo. Clicar na tag (ou no grafo filtrado por forma) já lista, sem query nenhuma, todas as notas daquela estrutura entre domínios — cruzamento como efeito colateral da navegação.
