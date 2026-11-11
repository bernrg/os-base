---
description: Destila auto-commits de SessionEnd que ficaram sem /fim — histórico na nota do projeto e STATUS.md atualizado.
---

# /destilar — o que ficou sem `/fim`

Manutenção é ritual de sessão, não daemon: o TCC do macOS nega ao launchd ler `~/Documents`, então um robô agendado nunca rodaria. Aqui o trabalho acontece na sessão, com {{NOME}} presente. (O marco se chama `zelador` por herança: é o texto que o `doctor` e o `heartbeat` procuram no `git log`.)

Rodar quando o `doctor` acusar `manutenção: N auto-commit(s) sem /fim`.

1. **Levantar o que vazou** — o marco é o último commit de destilação, não um stamp:
   ```
   marco=$(git log -1 --format=%H --grep='^zelador: destilado')
   git log ${marco:+$marco..HEAD} --fixed-strings \
       --grep='sessão: auto-commit (SessionEnd)' --format='%h %ad' --date=short
   ```
   Sem marco na história, a faixa é a história inteira.
2. Lista vazia → dizer isso e parar. Não inventar trabalho.
3. **Examinar `git show` de cada commit** e aplicar as regras do `/fim` (ler `.claude/skills/fim/SKILL.md`) ao que ficou sem destilar. Commits demais para uma sessão: destilar do mais antigo para o mais novo e comitar o que fez — o marco do passo 6 registra até onde chegou.
4. **Escrever o histórico datado** no `## Histórico` da nota do projeto tocado (append, nunca reescrever), ou em `brain/notas/diario/AAAA-MM-DD.md` quando o commit não pertencer a projeto nenhum.
5. **Atualizar o `STATUS.md`**: fila, tabela e `_Última atualização_`.
6. **Comitar por caminho**, mensagem **literal** `zelador: destilado de AAAA-MM-DD`. NUNCA `git push`, NUNCA `git add -A`.
7. Rodar `.claude/bin/doctor` e **relatar** a saída. FAIL em check que você não tocou **não é seu para consertar** — nunca editar arquivo do núcleo só para fazer o doctor passar.

A mensagem do passo 6 é o marco que o passo 1 procura da próxima vez. Sem ela, o mesmo trabalho reaparece inteiro; com ela escrita antes do trabalho, o trabalho se perde. Por isso ela vem **depois**.
