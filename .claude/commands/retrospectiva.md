---
description: Retrospectiva semanal em brain/notas/semanas/ — o que andou, o que travou e os focos da próxima semana.
---

# /retrospectiva — a semana

Manutenção é ritual de sessão, não daemon: o TCC do macOS nega ao launchd ler `~/Documents`, então um robô agendado nunca rodaria.

Rodar quando o `doctor` acusar `manutenção: retrospectiva há Nd`, ou no domingo.

1. **Coletar a semana** — raiz e cada repo de projeto:
   ```
   git log --since='7 days ago' --oneline
   for nota in brain/notas/projetos/*.md; do slug=$(basename "$nota" .md);
     for d in "$slug" "pessoal/$slug"; do
       [ -d "$d/.git" ] && git -C "$d" log --since='7 days ago' --oneline; done; done
   ```
2. Nenhum commit em lugar nenhum → dizer isso e parar. Semana vazia não vira nota.
3. **Ler o contexto**: a fila do `STATUS.md` e as ~5 memórias mais recentes de `brain/memoria/`.
4. **Escrever `brain/notas/semanas/AAAA-MM-DD.md`** (data de hoje), com: o que andou por projeto, decisões tomadas, o que travou, e **1 a 3 focos** para a próxima semana — coerentes com a fila, não com o desejo.
5. **Comitar só a nota da semana**: `git add brain/notas/semanas/AAAA-MM-DD.md`, mensagem `digest: semana de AAAA-MM-DD`. NUNCA `git push`, NUNCA `git add -A`.
6. Rodar `.claude/bin/doctor` e **relatar** a saída. FAIL em check que você não tocou é para relatar, não para consertar — nunca editar arquivo do núcleo só para o doctor passar.

O `doctor` mede o atraso pelo **nome do arquivo mais recente** em `brain/notas/semanas/`, não por stamp. O arquivo é o registro; se ele não existe, a semana não foi escrita.
