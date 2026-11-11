# CLAUDE.md — {{OS}} (OS pessoal)

{{OS}} (a "raiz") é a camada "OS" do trabalho de {{NOME}}: indexa os projetos, guarda o que não é código e codifica o modo de trabalho. Cada projeto vive numa subpasta com repo git PRÓPRIO; o repo da raiz versiona só a camada OS.

## Mapa

- `CLAUDE.md` — regras de como agir aqui.
- `STATUS.md` — painel ÚNICO do estado corrente: fila + tabela de projetos.
- `brain/` — segundo cérebro (vault Obsidian): `SOUL.md` (tom e postura do agente, por contexto) · `CONTEXTO.md` (quem é {{NOME}}, negócios, pessoas, objetivo) · `REGRAS.md` (como escrever e conectar nota) · `templates/`.
  - `brain/notas/projetos/<slug>.md` — uma nota por projeto: `## Contexto`, `## Pendências`, `## Histórico`.
  - `brain/notas/` — conhecimento avulso: `diario/` (rotina e destilado sem projeto), `semanas/` (retrospectiva), `cruzamentos/` (do `/clash`), `melhorias/` (do `/melhoria`), `painel.md` (visões Dataview), `como-uso-meu-os.md` (manual de uma página).
  - `brain/memoria/` — fatos duráveis que mudam comportamento, um arquivo por fato + `MEMORY.md` como índice.
  - `brain/privado/` — **FORA do git**: vida, saúde, finanças.
- `documentos/` — propostas, contratos, o que é de negócio e não é código.
- `assets/<projeto>/` — identidade visual compartilhada (logo, cores, fontes), versionada pela raiz. **Dono único**: os projetos apontam para cá, nunca duplicam o logo. Cópia (deploy isolado) **só com aprovação de {{NOME}}**, registrada em `assets/<projeto>/README.md`, que manda reexportar todas se o logo mudar.
- `arquivo/` — material morto ou sensível, **FORA de qualquer git**.
- Pastas de projeto na raiz — repo próprio, ignoradas pela raiz. Projeto pessoal vai em `pessoal/<slug>/`.
- `.claude/` — automação: `bin/` (`doctor`, `guarda`, `instalar`, `nota`, `memoria`, `abas`, `radar`, `heartbeat`, `auto-commit`, `retomada`, `achados`, `melhoria-scan.py`), `commands/` (`/clash`, `/melhoria`, `/abas`, `/destilar`, `/retrospectiva`), `skills/` (`/fim`, `/projeto-novo`, `/entrega`), `agents/` (executor e revisores), `melhoria/ledger.jsonl`, `abas/` (sessões vivas, **fora do git**).

## Regra de ouro: um dono por informação

Nunca duplicar, sempre apontar. Desempate nota/memória/skill, anatomia da nota e vocabulário (`dominio`/`forma`) são de `brain/REGRAS.md` — ler antes de criar ou reestruturar nota.

| Informação | Dono único |
|---|---|
| Regra de como agir | `CLAUDE.md` |
| Quem é {{NOME}}, negócios, pessoas | `brain/CONTEXTO.md` |
| Estado corrente de cada projeto | `STATUS.md`, e só ele |
| Pendências de {{NOME}} | Fila do `STATUS.md` (`- [projeto] ação`, máx. 3 por projeto); excedente na nota, com marcador `(+N na nota)` |
| O que o projeto é, arquitetura, decisões duráveis | `## Contexto` da nota do projeto |
| O que aconteceu e por quê | `## Histórico` da mesma nota — datado, sempre append |
| Fato durável que muda comportamento | `brain/memoria/` + linha no `MEMORY.md` |
| Procedimento multi-passo provado | skill em `.claude/skills/` |
| Como escrever e conectar nota | `brain/REGRAS.md` |
| Cronologia das sessões | `git log` |
| Vida pessoal (foco, pendências, decisões) | `brain/privado/pessoal.md`, fora do git; só a fila `[pessoal]` no STATUS.md |

## Segurança e git

- NUNCA versionar segredo técnico (chave, token, senha, string de conexão) — em nenhum repo, nem em `.env`. O arquivo `.env` é de {{NOME}}: eu digo qual variável criar e com que nome, quem escreve o valor é {{NOME}}. Segredo nunca é colado no chat nem escrito em nota ou memória (as duas são versionadas).
- NUNCA rodar `git push` por conta própria: o Claude executa, {{NOME}} decide. Só com pedido explícito **daquele** push ("pode seguir" no meio de outra tarefa não conta). Antes de todo push: varrer o diff por segredo e dizer para onde ele vai (repositório e ramo).
- NUNCA publicar o site, enviar mensagem ou rodar o que sai da máquina e não volta sem pedido explícito daquela ação. Antes, dizer: como se desfaz, qual a janela para desfazer, o que fica feito para sempre.
- NUNCA reescrever histórico publicado (push forçado, `rebase` de ramo que já subiu).
- NUNCA `git add -A` na raiz (sessões paralelas) — sempre add por caminho.
- NUNCA `git clean -fdx` na raiz — apagaria `brain/privado/` e `arquivo/`, sem backup.
- Antes de apagar ou sobrescrever, olhar o alvo. Apagar é por nome exato, nunca por curinga em pasta que não foi listada antes.
- Todo `cd` em Bash usa caminho ABSOLUTO: o diretório do shell persiste entre chamadas.
- Shell **zsh** não-interativo (`zsh -c`; a cada chamada só o `~/.zshenv` é lido, e ele desliga `EQUALS`/`NOMATCH`): glob sem match e `echo ====` não abortam mais a linha — check `zsh do Bash tool` do `doctor`. Padrão de glob para `find`/`grep` sempre entre aspas.
- Rodar o Claude Code sempre NA RAIZ, nunca dentro de `brain/` nem dentro da pasta de um projeto (a memória e os hooks do OS são indexados pela pasta de trabalho).
- Dado de outra pessoa (cliente, família, funcionário) é sigiloso por padrão: não vai para repositório público, nem para serviço externo, sem {{NOME}} decidir.

### Guardas na máquina

As regras acima não dependem só de eu lembrar. `.claude/bin/guarda` roda antes de todo comando Bash, em qualquer sessão desta máquina:

- **Nega:** push forçado; `git clean` com `-x`; `git add -A`/`.`/`:/` e `commit -a` no repo da raiz; `rm -r` na raiz, em `brain/`, `brain/privado/`, `arquivo/`, na pasta pessoal, com curinga dentro de uma delas, num `.git` ou num projeto inteiro; commit que leva segredo ou que não dá para examinar; apelido do git (`git ci`) e configuração na linha que muda o que ele faz (`-c alias.…`, `GIT_DIR=…` com commit). Comando do git é sempre por extenso, e na raiz caminho é nome exato, sem curinga.
- **Pergunta a {{NOME}}:** `git push`, publicação, mesclar PR; `git reset --hard`, `git clean`, `git checkout .`, `git restore .`, apagar ramo à força, `git stash drop`.
- O commit automático do fim de sessão (`auto-commit`) usa os mesmos padrões: arquivo que parece levar segredo fica retido, com o motivo em `.claude/abas/auto-commit.log`, e o resto segue.
- `.claude/settings.json` nega ao Claude ler `.env` e arquivo de chave (`.pem`, `.key`), e editar `.env`. `.env.example` é livre.

Guarda negou: ler o motivo, mudar o plano, **nunca** contornar (outro comando para o mesmo efeito, script que faz por dentro, variável que esconde o texto). Se a guarda errou, dizer isso a {{NOME}} e parar; quem decide afrouxar uma guarda é {{NOME}}, e a mudança vira commit com o porquê. A guarda é cinto de segurança, não barreira: o que ela não lê (comando em variável, `eval`, script) continua proibido pela regra escrita.

## Ritmo de sessão

- **Início:** ler `brain/SOUL.md` + `brain/CONTEXTO.md` + `STATUS.md` e dizer em uma linha onde paramos e a próxima ação.
- **Fim:** skill `/fim` — destila a sessão (histórico na nota, ou diário sem projeto), atualiza o `STATUS.md` e comita `sessão: <resumo>`. "Salva tudo", "vou dormir", "fechando" são gatilho.
- **Nada é dado por pronto sem evidência:** o comando de aceite roda e a saída aparece no relatório. Ao declarar algo pronto, a skill `/entrega` roda o checklist do tipo da entrega. Site: "pronto" é a página aberta no navegador e conferida, não o arquivo salvo.
- **Cirúrgico:** alterar só o que foi pedido; nunca "melhorar" o que funciona. Mudança em arquivo que {{NOME}} não escreveu (base do site, biblioteca, configuração): dizer o que vai mudar e por quê antes de mudar.

## Modo de trabalho (orquestração)

- A sessão principal ORQUESTRA: decompõe, delega, revisa cada diff antes de comitar. Implementação direta só em mudança trivial.
- Delegação segue `brain/notas/protocolo-de-delegacao.md` (quando delegar, tiering, pack do executor, prompt em 8 elementos, revisão do diff).
- `.claude/bin/doctor` audita a camada OS — gate de commit do `/fim` e do `/projeto-novo`. FAIL de máquina (memória, zsh, guardas) se conserta com `.claude/bin/instalar`. Busca: `.claude/bin/memoria <termo>`, `.claude/bin/nota <termo> [--dominio/--forma/--status]`; abrir só o de maior score. Memória nova: `.claude/bin/memoria add <slug> "<Título>" "<gancho>"`.
- `/clash` cruza o assunto corrente com o vault (só leitura). Atrito de sessão vai para `melhoria/ledger.jsonl` (coletor no SessionEnd, só de sessão aberta dentro do OS; guarda o começo do primeiro pedido e as correções, e é versionado: nada de segredo em pedido) e é analisado por `/melhoria`.
- **Mais de uma aba do Claude Code ao mesmo tempo:** um repo, uma aba. `/abas` mostra quem está onde; a doutrina é `brain/notas/protocolo-de-abas.md`. Com uma aba só, nada disso custa.
- **Manutenção é ritual de sessão, não daemon** (o TCC do macOS nega ao launchd ler `~/Documents`): o `heartbeat` avisa na abertura; `/destilar` (auto-commits sem `/fim`) e `/retrospectiva` (semana) fazem o trabalho com {{NOME}} presente. Marco é o commit, nunca um stamp.
- **Skills do plugin `superpowers`, se instalado, usadas sem esperar `/`:** implementação não-trivial → `test-driven-development`; trabalho grande → `brainstorming` → `writing-plans` → `executing-plans`; bug ou comportamento inexplicado → `systematic-debugging`; antes de push relevante → `requesting-code-review`; ao declarar algo concluído → `verification-before-completion`. Exceção: tarefa trivial ou conversacional, dizendo por que o skill foi pulado.

## Fonte oficial: qualquer biblioteca, API ou sistema externo

- Antes de escrever ou alterar código que toque uma biblioteca ou API externa (WebGL, three.js, o framework do site, a hospedagem, Stripe, Google, o que for): consultar a **documentação oficial do fornecedor**, na versão que o projeto usa. Nunca só memória (APIs mudam entre versões), nunca agregador de terceiros.
- Toda afirmação sobre um sistema de terceiros (campo, parâmetro, limite, preço, regra) leva referência: URL oficial ou "lido em AAAA-MM-DD em <onde>". Sem fonte, entra como `[a confirmar]` e não vira código nem regra de negócio.
- Se a documentação não cobrir, dizer que não cobre e perguntar a {{NOME}} ou a quem cuida do sistema. Motivo: um chute vira dado errado em produção.

## Convenção de projeto novo

Novo projeto = pasta na raiz com repo próprio + linha no `.gitignore` da raiz + linha no `STATUS.md` + nota em `brain/notas/projetos/<slug>.md`. Sem exceção. Usar `/projeto-novo`. Projeto pessoal vai em `pessoal/<slug>/` (a raiz já ignora `/pessoal/`); vida pessoal segue em `brain/privado/`. Projeto que já existe em outro lugar (um site que outra pessoa começou) entra do mesmo jeito: `git clone` para dentro da raiz, depois os outros três passos.
