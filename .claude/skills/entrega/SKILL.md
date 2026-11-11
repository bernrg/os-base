---
name: entrega
description: Checklist por entrega — confere o tipo da entrega (decisão, automação, documento, projeto) com evidência, fonte e segurança antes de dar por pronto. Gatilhos: "pronto", "feito", "terminei", "pode fechar", "entregue", "concluído". Disparo espontâneo quando a sessão vai declarar algo concluído.
---

# /entrega — checklist antes de declarar pronto

Roda por entrega. O `/fim` roda por sessão; um não chama o outro.

**Regra de ouro:** só marca `[x]` com evidência ("verifiquei X e deu Y"). "Acho que ficou bom" não é evidência, e grep valida forma, não verdade. Sem evidência, o item não recebe `[x]`.

## 1. Escolher o tipo (um)

- **Decisão:** está em `## Contexto` da nota, datada? A pendência do `STATUS.md` foi atualizada? A pessoa envolvida está alinhada?
- **Automação ou workflow:** rodou com dado real? O que acontece no erro, existe alerta? Credencial fora do texto e fora do repo? Nome e descrição se entendem em 30 dias?
- **Documento ou arquivo:** nome na convenção do OS (kebab-case, sem data salvo diário/semana)? A nota ou o `STATUS.md` aponta para ele? Segue `brain/REGRAS.md`, se é nota?
- **Projeto ou fase:** `STATUS.md` e nota atualizados? Aprendizado capturado nas três camadas do `/fim`?

## 2. Em toda entrega

- **Conteúdo:** cada afirmação de fato tem fonte apontável (citar a mais arriscada e onde está a fonte)? As partes da peça concordam entre si? O que foi verificado foi lido, não só varrido?
- **Segurança:** nenhum segredo, nenhum dado pessoal? Credencial em variável de ambiente ou em arquivo fora de qualquer repositório? Arquivo compartilhado sem dado sensível? Se tocou a camada OS, `.claude/bin/doctor` exit 0?

## Saída

```
Concluído: <1 linha>
[x] item — evidência
[ ] item — pulado porque
```

## Quando não usar

Resposta a pergunta, pesquisa, ou {{NOME}} disse "não precisa verificar".
- "pode fechar" querendo encerrar a sessão é /fim, não /entrega.
