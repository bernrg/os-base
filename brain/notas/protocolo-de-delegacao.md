---
tipo: conhecimento
dominio: [os-pessoal]
forma: [arbitragem]
criado: {{HOJE}}
status: madura
---

# Protocolo de delegação

O julgamento de orquestração escrito como artefato. A sessão principal orquestra; executores implementam.

## Quando delegar

- **Delegar:** implementação com >1 arquivo ou lógica nova. Paralelo só com arquivos disjuntos.
- **Não delegar:** edição trivial; leitura ampla (usar o agente Explore); decisão de escopo (é de {{NOME}}).

## Tiering

- O modelo da sessão principal NUNCA roda como sub-agent — só orquestra.
- O executor default é o modelo mais barato que dá conta: exige spec completa no prompt e aceite executável.
- **O modelo forte** entra onde o erro custa caro: dinheiro, revisão, destilação de memória, aceite reprovado após 1 retry.
- **Modelo e effort por papel nos subagentes Claude** moram em `.claude/agents/`: `executor-sonnet` (Sonnet 5, effort high), `revisor-sonnet` (Sonnet 5, xhigh), `revisor-fable` (Fable 5.1, xhigh; tasks de risco e revisão final do ramo). A chamada de subagente só troca o modelo; o effort vem da definição, e sem definição o subagente **herda o effort da sessão**. Definição nova só aparece numa sessão nova ("Agent type not found" na mesma sessão).

## Pack do executor

`brain/notas/projetos/packs/<slug>.md` (≤4.000 chars), destilado do `## Contexto` da nota antes da PRIMEIRA delegação do projeto. Blocos: **Invariantes**, **Armadilhas**, **Mapa** (arquivos/paths), **Aceite** (comandos), **Proibições**.

## Anatomia do prompt de executor — 8 elementos, nesta ordem

1. **Identidade + disciplina mínima** — quem ele é nesta tarefa e o rigor esperado.
2. **Tarefa em uma frase** — o resultado, não o método.
3. **Contexto a ler antes de escrever** — caminhos absolutos, pack primeiro (executor não herda a conversa).
4. **Entregas numeradas** — path exato de cada uma; decisões já resolvidas, não abertas.
5. **Regras invioláveis** — cada uma com a razão.
6. **Validação obrigatória** — comandos que o executor RODA e cola a saída. Aceite sem comando executável não é aceite.
7. **Proibições padrão** — git commit/push/add -A, arquivos fora do escopo. Quem comita é a sessão principal, depois da revisão.
8. **Formato do retorno** — dado bruto para o orquestrador, não relatório bonito.

## Durante a espera

- Ao disparar trabalho em segundo plano (subagente, workflow, extração longa): dar o **ETA em horário de relógio** ("por volta de 09:40"), **lendo `date` antes**, com a base da estimativa e as etapas que vêm depois. ETA de cabeça sai errado.
- Progresso se mede pelo disco, nunca lendo o transcript do agente: `git status --short` + `stat -f '%Sm %N' -t '%H:%M:%S'` nos arquivos tocados. Última escrita há mais de 5 min sem notificação = provável travamento; dizer isso e propor o `SendMessage`.
- A cada notícia do agente, reafirmar o ETA do que falta.

## Revisão obrigatória antes de qualquer commit

- Ler o diff INTEIRO (não o relatório do executor).
- Conferir que os aceites rodaram de verdade (saída colada).
- Procurar o que o relatório não diz: `git status` atrás de arquivos não mencionados.
- Camada OS tocada → rodar `.claude/bin/doctor`.
- Reprovou → devolver ao MESMO executor com o achado, não consertar à mão.
