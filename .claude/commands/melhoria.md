---
description: Analisa o ledger de melhoria contínua e propõe mudanças no OS — nada é auto-aplicado.
---

# /melhoria — análise do ledger e propostas

Oito passos, nesta ordem:

1. **Carregar o ledger** `.claude/melhoria/ledger.jsonl` com python3: dedup por `session_id` (a última linha vence) e filtrar sessões com `ts_end` posterior ao stamp `.claude/melhoria/last-analysis` (se o stamp não existir, analisar tudo).
2. **Agregar por projeto:** erros/interrupções/negações de permissão por sessão; assinaturas de erro mais frequentes; correções recorrentes do dono — o sinal mais valioso do ledger; e as ~5 sessões com mais atrito. Ordenar o atrito por `erros`; `exit1` é contexto, não ordenação (metade é grep sem match).
3. **Reler os relatórios anteriores** em `brain/notas/melhorias/` e classificar cada proposta passada como **aplicada / pendente / rejeitada**. Proposta rejeitada em ≥2 relatórios não volta sem sinal novo.
4. **Mergulhar nos ~5 piores transcripts** (em `~/.claude/projects/`): ler os trechos ao redor dos erros e das correções, não o arquivo inteiro.
5. **Escrever o relatório** em `brain/notas/melhorias/AAAA-MM-DD.md` com as seções: **Panorama** (números do período), **Status das propostas** (das anteriores), **Padrões** (o que se repete) e **Propostas** — cada uma com **Sinal** (evidência do ledger/transcript), **Arquivo-alvo** e **Mudança** pronta para aplicar.
6. **Atualizar o stamp** `.claude/melhoria/last-analysis` com o timestamp ISO do momento da análise.
7. **Gravar o lembrete na fila:** acrescentar UM item ao bloco `[raiz]` da fila do `STATUS.md`, apontando o relatório — `- [raiz] Decidir as propostas do relatório de melhoria de AAAA-MM-DD (IDs das propostas)`. Um item por relatório, nunca um por proposta (teto de 3 por projeto); se já existe item de decisão de relatório anterior, fundi-lo neste.
8. **Comitar só esses paths** (relatório + stamp + `STATUS.md`), add por caminho, mensagem `melhoria: relatório AAAA-MM-DD`.

Nada é auto-aplicado: cada proposta vive no relatório até {{NOME}} aprovar.
