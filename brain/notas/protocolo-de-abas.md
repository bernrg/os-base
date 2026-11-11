---
tipo: conhecimento
dominio: [os-pessoal]
forma: [gargalo-de-informacao]
criado: {{HOJE}}
status: semente
---

# A aba de controle governa por leitura, nunca por trava

Quando várias abas do Claude Code trabalham sobre a mesma raiz, uma delas deixa de implementar e passa a ser o ponto de observação — a *aba de controle*. O poder dela é inteiramente informacional: ela sabe quem existe, em que projeto cada uma está e o que cada uma executa agora. Ela não bloqueia ninguém, não troca branch alheia e não mata processo de ninguém. No instante em que a aba de controle começa a editar repo, ela vira mais uma disputante e perde a autoridade de dizer onde é seguro mexer.

Esta nota é a doutrina de operação; a ferramenta é `.claude/bin/abas`. **Trabalhando com uma aba só, nada aqui custa nem atrapalha:** o registro sai calado e o portão nunca nega.

## Por que uma aba dedicada

Sem ela, o inventário das abas é refeito à mão, no primeiro parágrafo de cada sessão. O gargalo nunca é de capacidade — é de **informação**: várias sessões trabalhando bem, nenhuma sabendo das outras. Concentrar essa leitura em uma aba resolve o gargalo sem tocar em quem produz.

## Abertura do dia

Toda aba nova nasce sabendo das vizinhas: se houver outra aba viva, o `SessionStart` injeta **uma linha** com quem está aberto e em que projeto. É fato, nunca conselho — a aba não sugere abrir nada nem comenta o inventário sem ser perguntada. Isso mata o preâmbulo manual na fonte, em toda aba, e não só na de controle.

O que a linha não cabe é o que justifica a aba de controle: o que cada uma está *executando* agora, repo sujo sem dono e a ordem do `/fim`.

1. `/abas` na aba de controle — retrato do que sobreviveu da noite anterior.
2. Batizar cada aba nova assim que ela abre: `abas nome <session_id> "<projeto>"`. Aba sem nome é aba que você vai reabrir para descobrir o que é.
3. Ler os **alertas** antes da tabela. Repo sujo sem aba viva reivindicando é a linha mais importante do painel: é trabalho órfão de uma sessão que fechou. Não comitar por cima — descobrir de onde veio pelo transcript antes de qualquer coisa.

## Regra de dono

**Um repo, uma aba.** O corte útil entre abas é por repo, nunca por camada — abrir "front" e "back" do mesmo sistema não paraleliza nada e faz as duas colidirem no mesmo arquivo.

Antes de mandar uma aba mexer num repo, o painel responde se outra já o reivindica. Se sim, há dois caminhos honestos, nesta ordem de preferência:

1. **Esperar** — quase sempre é mais barato que coordenar.
2. **Worktree** — criar worktree a partir da `main` e trabalhar lá; para mesclar, um segundo worktree na `main`. O checkout alheio nunca é tocado.

Não existe terceiro caminho. `git checkout` para "só dar uma olhada" arranca o chão da outra sessão, e ela não tem como perceber.

## Leitura de banco de projeto que outra aba roda

Nunca no arquivo vivo: ele está aberto pelo servidor da outra aba. Copiar para uma pasta temporária (banco SQLite: o `.db` **junto com `-wal` e `-shm`**) e ler a cópia.

## O `/fim` com N abas

Quando o corte já é por repo, os repos param de colidir e **a camada OS da raiz vira o único recurso disputado**: `STATUS.md`, `brain/notas/projetos/<slug>.md` e o `ledger.jsonl` são escritos por todas as abas.

- **Serializar — pelo trinco, não por pergunta:** uma aba faz `/fim` por vez, e quem decide a vez é `.claude/bin/abas trinco pegar` (arquivo `.claude/abas/trinco.json` com o pid da aba). O `/fim` pega sozinho, espera até 90 s se outra aba estiver no dela e solta ao terminar; pid morto é trinco vazio, então aba fechada no meio não trava ninguém. Ninguém pergunta aba por aba de quem é a vez: o trinco é a autorização.
- **Reler imediatamente antes de escrever**, nunca editar a partir do que foi lido no começo da sessão.
- `git add` **por caminho**, só nos arquivos que aquela sessão tocou. Nunca `git add -A` na raiz.
- A aba de controle fecha **por último**, porque só ela vê se sobrou repo sujo.

## O que a aba de controle não faz

- Não roda `/fim` pelas outras abas — cada sessão destila a própria, porque só ela tem o contexto.
- Não mata processo alheio. Job longo em outra aba (suíte de testes, build) é trabalho, não travamento.
- Não edita repo de projeto. Se precisar mexer em código, abre outra aba para isso.
- Não promete impedir overwrite de **arquivo**. Ela **mostra** o risco; quem evita é a disciplina de reler antes de escrever.

## O portão

O que a aba de controle não faz, um hook faz: `PreToolUse(Bash)` com `if: "Bash(git *)"` chama `.claude/bin/abas portao` antes de todo `git` que muda working tree ou HEAD (`checkout`, `switch`, `merge`, `pull`, `rebase`, `reset`, `restore`, `stash`, `cherry-pick`, `revert`, `clean`, `am`, `apply`). Ele descobre o checkout alvo (`-C`, `cd` anterior ou o cwd, subindo até o `.git`) e nega em dois casos, com o motivo na cara da sessão:

1. o alvo é o checkout que **outra aba viva segura** — o cwd dela, ou o último caminho que ela *escreveu* (Edit/Write, `cd`, git mutável); só ler não reivindica;
2. o alvo é a **raiz** com outra aba viva e esta aba **não tem o trinco**.

O mesmo portão vigia o **Write** (reescrita de arquivo inteiro) em `STATUS.md`, `CLAUDE.md`, `brain/notas/**` e `brain/memoria/MEMORY.md`: com outra aba viva, Write em arquivo que já existe é negado e a saída é Edit (relê na hora) ou o trinco. Criar arquivo novo passa. É o único modo de *perder* conteúdo entre abas — Write a partir de leitura velha apaga o que a outra gravou — e era o que sobrava para a disciplina humana.

Fora disso passa em silêncio e custa zero: sozinho, nenhum `git` nem Write é negado. `push` fica fora de propósito — não toca working tree nenhuma; segue regido por "só com pedido explícito de {{NOME}}" e pela guarda (`.claude/bin/guarda`). Falha aberta: erro do próprio portão nunca derruba um comando. Dívida assumida: comando montado em variável, `eval`, `$(…)` ou escondido num heredoc não é lido (o corpo do heredoc fica fora da análise); `git` por caminho absoluto (`/usr/bin/git`) não casa com o `if: Bash(git *)` do hook; `--work-tree`, `--git-dir`, `GIT_DIR=` e `-c alias.*` não mudam o alvo calculado; `git worktree remove` não está na lista; e aba aberta fora da raiz não carrega o hook. É cinto de segurança entre abas cooperantes, não barreira contra adversário — por isso falha aberta. Já cobertos: quebra de linha e `then`/`do`/`env` antes do `git`, symlink (o da memória) e caixa no caminho do Write, e a tomada de trinco morto sob `flock`. Medido na prova: o portão julga a chamada Bash **inteira antes de qualquer parte rodar** — `rm registro && git merge` na mesma chamada foi negado com o registro ainda presente; preparação e git mutável vão em chamadas separadas.

## Custo

Trabalhando sozinho, custa **zero**: sem outra aba viva, o `SessionStart` sai calado. Com outras abas, custa uma linha de contexto por sessão — o inventário. Rodar `.claude/bin/abas` num terminal comum, fora do Claude Code, também custa zero: o painel é para os seus olhos. Só `/abas` gasta contexto de verdade, e só quando você quer o cruzamento com o `STATUS.md`.

Essa linha substitui um preâmbulo digitado à mão, que disparava uma investigação muito mais cara. **A troca só se sustenta enquanto a linha for uma linha** — no dia em que ela virar um bloco, o argumento econômico se desfaz.

O modo caro seria um vigia em loop, reavaliando sozinho o tempo todo. Foi recusado no desenho justamente por isso: queimaria tokens de fundo com ninguém no teclado.

## Dívida conhecida

Adiada de propósito na construção, com o motivo:

- **A raiz não aparece no bloco REPOS.** O painel lista só as pastas de projeto, então o único recurso que o desenho admite continuar em disputa — `STATUS.md`, notas, `ledger.jsonl` — é justamente sobre o que ele se cala. Lacuna do spec, não da implementação.
- **`pids_claude_vivos()` varre a máquina inteira**, não este workspace. Uma aba rodando em outro diretório aparece aqui como fantasma `[não registrada]`. Inofensivo hoje, porque ela não reivindica projeto nenhum e portanto não suprime alerta.
- **`idade` zera no `/clear` e no compact** — o registro antigo é apagado e o novo nasce com `inicio` fresco. A aba mais antiga pode aparecer como recém-nascida.
- **`wt:1` significa "só a worktree principal"**, não "existe uma worktree extra".
- **`IGNORAR_CMD` casa por substring**, não por token.
- **A coluna "fazendo agora" mostra linha de comando literal.** Se algum comando levar segredo em argumento, ele aparece no painel — e daí pode ir para nota. Nunca copiar linha de comando literal para nota ou `STATUS.md`.
