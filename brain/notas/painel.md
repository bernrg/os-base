---
tipo: conhecimento
dominio: [os-pessoal]
forma: []
criado: {{HOJE}}
status: madura
---

# Painel do vault

Visões sob demanda (fora do núcleo). **Dataview é plugin: nenhuma query é fonte de verdade — só visão.** Sob cada bloco há o **fallback sem plugin** (comando que dá a mesma resposta em markdown/terminal).

## 1. Notas órfãs (sem link de entrada nem de saída)

```dataview
LIST
FROM "brain/notas"
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
```
Fallback: `for f in $(find brain/notas -name '*.md'); do grep -Lq '\[\[' "$f" && echo "$f"; done`

## 2. Notas que compartilham `forma` entre `dominio` diferentes (candidatas a cruzamento)

```dataview
TABLE dominio, forma, status
FROM "brain/notas"
WHERE forma
FLATTEN forma AS f
SORT f ASC
```
Leitura: mesma `forma` aparecendo em linhas de domínios distintos = par candidato. Fallback: `.claude/bin/nota --forma=<f>` e olhar os domínios que voltam.

## 3. Notas dormentes há >45 dias

```dataview
TABLE status, criado, dateformat(file.mtime, "yyyy-MM-dd") AS ultimo_toque
FROM "brain/notas"
WHERE status = "dormente" AND file.mtime <= date(today) - dur(45 days)
```
Fallback: `.claude/bin/nota --status=dormente` (e o check 8 do doctor cobra staleness por git).

## 4. Pendências nas notas de projeto (conferir com o marcador `(+N na nota)` da fila)

```dataview
TABLE length(filter(file.lists, (l) => contains(l.section.subpath, "Pendências"))) AS pendencias
FROM "brain/notas/projetos"
```
Fonte de verdade da conferência é o **check 4 do doctor** — esta query é só o olho rápido. Fallback: `.claude/bin/doctor` (linha "pendências").

## 5. Cruzamentos ainda em `status: semente`

```dataview
LIST
FROM "brain/notas/cruzamentos"
WHERE tipo = "cruzamento" AND status = "semente"
```
Fallback: `.claude/bin/nota --status=semente | grep cruzamentos/`

## 6. Gerador de par aleatório (ritual semanal)

```dataviewjs
const ns = dv.pages('"brain/notas"').where(p => p.forma && p.forma.length);
const pick = () => ns[Math.floor(Math.random() * ns.length)];
const a = pick(); let b = pick();
for (let i = 0; i < 20 && (!b || b.file.path === a.file.path); i++) b = pick();
dv.paragraph(`**Choque da semana:** [[${a.file.name}]] × [[${b.file.name}]]`);
```
Fallback sem plugin: `.claude/bin/nota --forma=<f>` e escolher, a olho, duas de domínios diferentes.

## 7. Departamentos (dono único do mapeamento dominio→departamento)

Um departamento é um grupo de termos do vocabulário de `dominio` (`brain/REGRAS.md`). O OS nasce com um só: **OS** = metodo, os-pessoal. Cada termo novo de `dominio` entra aqui ao nascer, num departamento que já existe ou num novo (copie o bloco abaixo e troque os termos).

### OS
```dataview
TABLE dominio, forma, status FROM "brain/notas"
WHERE contains(dominio, "metodo") OR contains(dominio, "os-pessoal")
```
Fallback: `.claude/bin/nota --dominio=metodo` e `.claude/bin/nota --dominio=os-pessoal`

### Sem departamento (dominio ainda não mapeado acima)
```dataview
LIST FROM "brain/notas"
WHERE dominio AND !contains(dominio, "metodo") AND !contains(dominio, "os-pessoal")
```
Fallback: comparar `.claude/bin/nota --dominio=<termo novo>` com a lista deste bloco
