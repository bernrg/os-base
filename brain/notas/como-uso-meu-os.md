---
tipo: conhecimento
dominio: [metodo]
forma: [ciclo-de-feedback]
criado: {{HOJE}}
status: madura
---

# Este OS não se lê inteiro, se opera pelo ciclo da sessão

Nota para {{NOME}} daqui a seis meses, quando tiver esquecido como isto funciona. O sistema inteiro é um **ciclo de feedback**: toda sessão começa lendo o estado, produz trabalho, e no fim devolve o que aprendeu ao lugar certo — e o doctor fecha o loop auditando se cada peça voltou para seu dono. Você não precisa decorar as regras (elas estão no `CLAUDE.md` da raiz e em [[REGRAS]]); precisa confiar no ritmo e deixar as ferramentas te lembrarem. Se você está abrindo arquivos na mão para descobrir "onde parei", o loop quebrou — a resposta é uma linha, dada na abertura da sessão.

## Por que existe esse ritmo

Sem um lugar que force convergência, cada sessão recomeça do zero e o contexto evapora. O ritmo início→fim existe para isso — não é burocracia, é o que impede que o custo de "relembrar" cresça até engolir o trabalho. **Início** te reorienta em uma frase. **Fim** (`/fim`, ou "vou dormir" / "fechando") destila o *porquê* da sessão antes que ele suma — o `git log` é cronologia, não memória. Rode `/fim` toda vez que fechar, mesmo sessão curta: o barato é destilar quente, o caro é reconstruir frio.

## Quando puxar cada ferramenta

- **`/projeto-novo`** — só quando um projeto vira real (vai ter repo próprio). Ele carimba os quatro passos de uma vez para você nunca deixar um pela metade.
- **`/entrega`** — antes de dizer "pronto". Confere com evidência, não com impressão.
- **`/clash`** — no meio do trabalho, quando bate a sensação "isso lembra outra coisa". É a ferramenta que paga a aposta do vocabulário de `forma`: cruza domínios distantes pela mesma estrutura. Use quando quer *ideia*, não quando quer resposta.
- **`bin/nota` / `bin/memoria`** — busca rápida antes de escrever, para não duplicar. `nota` filtra por `--forma` / `--dominio`; `memoria` acha o fato que muda comportamento.
- **`/melhoria`** — quando o atrito repetiu (o mesmo erro, a mesma permissão negada). O ledger junta sozinho; você só lê quando quer consertar o *sistema*, não o projeto.

## O que o doctor está te dizendo

O doctor é o guarda do loop, não um linter de estilo. Traduza a saída:

- **PASS geral** — o sistema está honesto: cada informação no dono certo, painel batendo com as notas, memória indexada. Pode commitar.
- **WARN staleness / cruzamentos-elos** — nada quebrou, mas algo esfriou: uma nota parada, um `#elo-especulativo` que nunca virou relação nem foi descartado, um cruzamento preso em `semente`. É a dívida do segundo cérebro te cutucando: **decida** (promove ou joga fora), não deixe apodrecer.
- **FAIL** — contrato roto: núcleo grande demais, fila malformada, symlink de memória perdido, índice furado, guarda desligada. Trava o commit de propósito. Conserte antes; é sempre estrutural, nunca estético. Quando o FAIL é da máquina (memória, zsh, guardas globais), o conserto é `.claude/bin/instalar`.

## Quando a guarda te para

`.claude/bin/guarda` roda antes de todo comando do Claude. Ela **nega** o que não tem volta e nunca é necessário (push forçado, apagar pasta sem backup ou um projeto inteiro, commit com senha dentro) e **pergunta** antes do que sai da sua máquina (push, publicar o site) e do que descarta trabalho sem commit. Quando ela perguntar, leia: o texto diz o que o comando faz. As três perguntas do fim (como se desfaz, qual a janela, o que fica para sempre) são para você responder antes do sim. Se você não sabe responder, a resposta é não, e a próxima pergunta ao Claude é "me explica o que isso faz".

## As decisões de desenho, e por quê

- **Repo por projeto, raiz só com a camada OS.** Cada projeto tem ciclo de vida próprio e um dia pode ganhar sócio ou virar de outra pessoa; misturar históricos git seria irreversível. A raiz versiona só o "sistema operacional" e ignora cada pasta de projeto.
- **Sem projeto aninhado.** Um repo dentro de outro confunde a ferramenta e você mesmo sobre onde uma mudança mora. Fronteira física = fronteira mental.
- **Um dono por informação.** A regra que mais te salva. Duplicar parece útil e sempre mente: as cópias divergem e nenhuma vira confiável. Quando bater a tentação de copiar, aponte com wikilink — foi por isso que esta nota não repete o `CLAUDE.md` nem [[REGRAS]].
- **Vocabulário fechado de `forma`.** A aposta central do vault: se `forma` fosse texto livre, nada cruzaria. Fechado e fatiado pelo objeto que o gargalo estrangula (capacidade, decisão, informação), dois problemas de domínios distantes com a mesma estrutura viram par visível — é onde mora a ideia que você não teria sozinho. Pagar o preço de escolher da lista é o que faz o [[mecanismos-de-cruzamento|cruzamento]] funcionar.
- **Regra que importa mora na máquina, não na memória de ninguém.** Regra escrita depende de alguém lembrar; hook e doctor não. O que é irreversível tem guarda; o que é estrutural tem check.

Ver também: [[protocolo-de-delegacao]] (como orquestrar a execução), [[protocolo-de-abas]] (mais de uma sessão ao mesmo tempo) e [[painel]] (visões do vault sob demanda).
