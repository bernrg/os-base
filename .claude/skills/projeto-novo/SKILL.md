---
name: projeto-novo
description: Carimba um projeto novo — pasta na raiz com repo git próprio, linha no .gitignore da raiz, linha no STATUS.md e nota em brain/notas/projetos/. Valida os quatro passos com evidência.
---

# /projeto-novo <slug> — carimbar projeto novo

Convenção (do CLAUDE.md): novo projeto = pasta na raiz com repo próprio + linha no `.gitignore` da raiz + linha no `STATUS.md` + nota do projeto. Sem exceção.

Entrada: slug em kebab-case e uma frase do que o projeto é. Se faltar algum dos dois, perguntar antes de executar.

**Projeto pessoal** (fora do trabalho): a pasta é `pessoal/<slug>/` em vez de `<slug>/`. O passo 2 não se aplica (a raiz já ignora `/pessoal/`; o doctor confere), e no passo 1 e na validação 1 troca-se `<slug>` por `pessoal/<slug>`. A nota segue em `brain/notas/projetos/<slug>.md`, só com arquitetura e decisões: rotina, saúde e finanças ficam em `brain/privado/`.

Passos (na raiz):

1. `mkdir <slug> && git -C <slug> init`. **Projeto que já existe em outro lugar** (um site que outra pessoa começou, um repo no GitHub): em vez disso, `git clone <url> <slug>`; os passos 2 a 4 e a validação são os mesmos, e a primeira entrada do histórico diz de onde veio.
2. Adicionar a linha `/<slug>/` à seção "Projetos" do `.gitignore` da raiz, se ainda não existir. **A barra inicial não é enfeite:** sem ela o padrão casa qualquer subpasta homônima em qualquer nível — `loja/` capturaria `assets/loja/`, que é versionado pelo repo da raiz de propósito. É o que o comentário da seção manda, e todas as linhas de lá seguem.
3. Adicionar ao `STATUS.md`: linha na tabela de projetos (link para a nota | Estado | Próxima ação | Bloqueio) e, se já houver pendências, itens na fila (máx. 3).
4. Criar `brain/notas/projetos/<slug>.md` com `## Contexto` (o que é), `## Pendências` e `## Histórico` (primeira entrada datada: projeto criado).

Validação (obrigatória — a saída aparece no relatório):

```
test -d <slug>/.git && echo "1) repo proprio ok"
grep -n "^/<slug>/" .gitignore && echo "2) gitignore ok"
grep -n "<slug>" STATUS.md && echo "3) STATUS ok"
test -f brain/notas/projetos/<slug>.md && echo "4) nota ok"
.claude/bin/doctor && echo "5) doctor ok"
```

Só declarar concluído se as quatro verificações passarem E o doctor sair com exit 0 (é o passo final de validação — ele confere painel, fila, gitignore e índice de uma vez).

Por fim, comitar a camada OS — add por caminho (`.gitignore`, `STATUS.md`, a nota) com mensagem `projeto: <slug> criado`. Nunca rodar `git push`.
