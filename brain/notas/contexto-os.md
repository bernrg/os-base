---
tipo: conhecimento
dominio: [os-pessoal]
forma: []
criado: {{HOJE}}
status: ativa
---

# Contexto: meu OS pessoal e como trabalho

Este texto é para colar no Claude do navegador ou do celular (Claude.ai), que não enxerga a minha máquina. Ele explica como meu ambiente de trabalho é organizado, para você me ajudar a pensar e planejar sem sugerir coisas que quebrem minhas convenções. Quem executa é o Claude Code, localmente. Seu papel aqui é raciocínio, planejamento, análise e redação. Quando algo precisar ser executado no sistema, você me ajuda a formular a instrução, e eu levo ao Claude Code.

## Quem sou

<!-- Duas ou três frases, copiadas de brain/CONTEXTO.md. Sem dado sensível: este texto sai da máquina. -->

## A ideia do "OS pessoal"

Tenho um workspace central na minha máquina (uma pasta raiz) que funciona como camada de sistema operacional do meu trabalho. Ela não guarda código — indexa projetos, guarda o que não é código, e codifica meu modo de trabalhar num formato que o Claude Code lê no início de cada sessão. Três camadas:

- **OS**: regras de comportamento e estado corrente do trabalho (arquivos CLAUDE.md e STATUS.md na raiz).
- **Cérebro (brain/)**: conhecimento durável — quem sou, o que sei, o que decidi. É um vault de Obsidian em markdown puro.
- **Projetos**: o trabalho de verdade (código). Cada projeto vive em subpasta com repositório git próprio, separado da camada OS.

## A regra de ouro: cada informação tem UM dono

Nunca duplico informação; sempre aponto. Se a mesma coisa aparece em dois lugares, um está errado. Onde cada coisa mora:

- Regra de como agir → CLAUDE.md
- Quem sou, negócios, pessoas → brain/CONTEXTO.md
- Estado corrente de cada projeto → STATUS.md (e só ele)
- Minhas pendências → fila do STATUS.md (top 3 por projeto); excedente na nota do projeto
- O que um projeto é, arquitetura, decisões duráveis → seção ## Contexto da nota do projeto
- O que aconteceu e por quê → seção ## Histórico da nota (datado, sempre append)
- Fato durável que muda comportamento → brain/memoria/
- Procedimento multi-passo provado → skill em .claude/skills/
- Convenções de escrita de nota → brain/REGRAS.md

Desempate: "isto muda como devo agir?" → memória. "É conhecimento para reler?" → nota. "É procedimento verificado?" → skill.

**Implicação para você:** quando me ajudar com um projeto novo, não sugira guardar estado, decisão ou pendência de forma solta — encaixe na estrutura acima. Se eu propuser algo que duplica informação, aponte.

## Como um projeto novo nasce

Todo projeto novo = pasta na raiz com repo git próprio + linha no .gitignore da raiz + linha no STATUS.md + nota em brain/notas/projetos/<slug>.md. Sem exceção. Existe um comando (/projeto-novo) que faz os quatro de uma vez. Cada projeto é um irmão na raiz — nunca aninhado dentro de outro. Um negócio ou cliente vive no CONTEXTO.md; os sistemas e sites que construo para ele é que são projetos.

## Regras de segurança que sempre valem

- Nunca versionar segredo técnico (chave, token, senha, string de conexão) — em nenhum repo, nem em .env.
- O git push é sempre decisão minha. Ferramentas nunca fazem push sozinhas.
- Segredos entram por variável de ambiente, nunca no código.
- brain/privado/ e arquivo/ ficam fora do git e não têm backup — nada os referencia.

## Ritmo de trabalho

Cada sessão de trabalho no Claude Code abre lendo o contexto e o estado, e fecha com um ritual (/fim) que destila o que aconteceu, atualiza o estado e comita. Nada é dado por pronto sem evidência: o comando de aceite roda e a saída aparece. Decisões de escopo e arquitetura são minhas — a IA traz análise, eu decido, e a decisão vira registro no ## Contexto do projeto.

## Como me ajudar melhor

- Ao planejar algo novo, encaixe na estrutura do OS acima em vez de propor organização paralela.
- Quando uma decisão for de escopo ou arquitetura, traga trade-offs e me deixe decidir — não decida por mim.
- Se eu pedir algo que duplica informação, quebra a regra de dono único, ou aninha projeto dentro de projeto, aponte antes de seguir.
- Distinga o que você pode fazer aqui (pensar, analisar, redigir) do que precisa ir ao Claude Code (mexer em arquivos, rodar, comitar) — e me ajude a formular a instrução para levar até lá.
- Prefira que eu valide antes de commits e antes de ações irreversíveis.
