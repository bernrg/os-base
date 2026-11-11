---
name: fim
description: Ritual de fim de sessão — destila a sessão no histórico do projeto (ou no diário), atualiza o STATUS.md e comita a camada OS. Gatilhos: "salva tudo", "vou dormir", "fechando" e equivalentes.
---

# /fim — ritual de fim de sessão

Executar NA RAIZ do workspace, nesta ordem.

**Idempotente:** sem nada novo desde o último commit desta aba, o `/fim` só confere e responde "nada a registrar", com a mesma evidência do passo 8 (e solta o trinco, passo 7).

1. **Identificar o escopo da sessão:** qual(is) projeto(s) foram tocados. Se nenhum, o destino do destilado é o diário.
   - **Trinco:** rodar `.claude/bin/abas trinco pegar --espera 90 --motivo fim` — é o que serializa os `/fim` entre abas sem ninguém perguntar a ninguém. Exit 0: a vez é desta aba, seguir. Exit 1: outra aba está no `/fim` há mais de 90 s; dizer qual (a saída cita) e parar aqui, sem escrever nada. Ninguém pede autorização às outras abas: o trinco é a autorização.
   - **Abas:** rodar `.claude/bin/abas`. Com outra aba viva, seguir "O `/fim` com N abas" de `brain/notas/protocolo-de-abas.md`: reler cada arquivo imediatamente antes de escrever, add só dos caminhos desta sessão, e arquivo sujo de outra aba fica de fora. Dizer no relatório, em uma linha, o que era de outra aba e ficou de fora.
2. **Destilar a sessão** — o que aconteceu e por quê (decisões, descobertas, mudanças de rumo), não um log de comandos:
   - **Três perguntas antes de escrever, nesta ordem:** (a) surgiu **regra de negócio** (como a empresa ou o cliente funciona: prazo, preço, quem decide, o que o sistema faz de verdade)? (b) surgiu **decisão ou leitura estratégica** (rumo, prioridade, o que não fazer e por quê)? (c) surgiu **fato técnico** que muda comportamento? Destino: (a) → memória se muda como agir, senão bullet datado em `## Contexto` da nota; (b) → `## Contexto` da nota; se vale para mais de um projeto, nota de conhecimento em `brain/notas/` com `dominio` e `forma`; (c) → memória (passo 4). Cada entrada em até 6 linhas no formato **Insight + Solução + Não fazer** (na memória, `**Why:**` é o Insight e `**How to apply:**` é a Solução; "Não fazer" entra como última linha quando houver). Camada sem material não escreve nada: escrever é exceção, não obrigação.
   - Com projeto: append datado (`- **AAAA-MM-DD** — …`) em `## Histórico` de `brain/notas/projetos/<slug>.md`. Decisões duráveis sobem para `## Contexto` da mesma nota.
   - Sem projeto: `brain/notas/diario/AAAA-MM-DD.md` (append se o arquivo do dia já existir).
   - **Achados de segurança** (só traz algo com o plugin opcional `security-guidance` instalado; sem ele sai vazio e segue): rodar `.claude/bin/achados --desde <data de início da sessão>`. Cada achado novo vira bullet em `## Pendências` da nota do projeto (ou entra no histórico como descartado, com o motivo). Achado que aparece no fim da sessão e não é registrado some com ela.
3. **Atualizar `STATUS.md`:** linha do projeto na tabela (Estado / Próxima ação / Bloqueio) e fila — máx. 3 itens por projeto; excedente vai para `## Pendências` da nota; itens concluídos saem.
4. **Memória:** para o que as três perguntas do passo 2 mandaram para memória, ANTES de criar rodar `.claude/bin/doctor`: se o check do índice de memórias estiver em WARN (MEMORY.md inchado), fundir memórias existentes em vez de acrescentar. Depois criar o arquivo em `brain/memoria/` + uma linha no `brain/memoria/MEMORY.md`.
5. **Gate do commit — `.claude/bin/doctor`:** só comitar com exit 0. Se houver FAIL, corrigir primeiro (fundir/apagar memórias, encurtar células do STATUS.md, consertar fila/marcadores) e rodar de novo até passar. Atualizar a linha `_Última atualização: AAAA-MM-DD_` do STATUS.md.
6. **Comitar o repo da raiz** — add POR CAMINHO (nunca `git add -A`), só os arquivos da camada OS tocados na sessão:

   ```
   git add <caminhos>
   git commit --only -m "sessão: <resumo em poucas palavras>" -- <caminhos>
   ```

   O `--only` comita exatamente esses caminhos e deixa intacto o que outra aba tiver em stage (sem ele, o commit varre o índice inteiro).

   Repos de projeto NÃO são comitados pelo /fim — só a pedido explícito de {{NOME}}.
7. **Soltar o trinco:** `.claude/bin/abas trinco soltar` — sempre, inclusive no caminho "nada a registrar" e quando um passo anterior falhou. (Aba que fecha sem soltar não trava ninguém: trinco de pid morto é trinco vazio.)
8. **Evidência:** mostrar a saída do doctor (exit 0) e de `git show --stat HEAD` no relatório final. Nada é dado por pronto sem essas saídas.
   - **Fechamento:** terminar com o bloco `Pode fechar esta aba: sim/não`, cobrindo (a) a raiz: commit; (b) cada repo tocado: ramo, limpo ou sujo, N à frente do GitHub, push sim/não; (c) processo, servidor ou agente desta aba ainda vivo; (d) o que o auto-commit do `SessionEnd` ainda levaria: `git status --porcelain -- brain STATUS.md CLAUDE.md .claude`; sem outra aba viva ele leva tudo isso, com outra aba viva só o que esta sessão tocou (ver com `.claude/bin/auto-commit --dry-run < payload`, payload `{"session_id":…,"transcript_path":…}`).

Nunca rodar `git push`.
