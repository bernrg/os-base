# os-base

Modelo de **OS pessoal** para trabalhar com o Claude Code: uma pasta raiz que indexa os seus projetos, guarda o que não é código e ensina ao Claude como você trabalha, com as regras de segurança ligadas na máquina.

Este repositório é só a **arquitetura**: as regras, os rituais e os scripts. Não traz informação de ninguém. `brain/CONTEXTO.md`, `brain/SOUL.md` e a memória nascem em branco e são preenchidos na instalação, com você.

## O que vem dentro

| Peça | Para quê |
|---|---|
| `CLAUDE.md` | As regras que o Claude lê em toda sessão: segurança, git, evidência, fonte oficial, um dono por informação |
| `STATUS.md` | Painel único: sua fila e a tabela de projetos |
| `brain/` | Segundo cérebro em markdown (abre no Obsidian): quem você é, notas por projeto, diário, memória |
| `.claude/bin/guarda` | Roda antes de todo comando: **nega** push forçado, apagar pasta sem backup ou projeto inteiro, e commit com senha; **pergunta** antes de push, de publicar e de descartar trabalho sem commit |
| `.claude/bin/doctor` | Audita o OS. É o portão de todo commit da raiz |
| `.claude/bin/instalar` | Liga o clone à sua máquina (memória, shell, guardas). Roda de novo sempre que o doctor reclamar da máquina |
| `/fim`, `/entrega`, `/projeto-novo` | Fechar a sessão, conferir antes de dizer "pronto", nascer um projeto |
| `/clash`, `/destilar`, `/retrospectiva`, `/melhoria`, `/abas` | Cruzar ideias, manutenção semanal, melhoria contínua, várias abas |

Uma página que explica tudo: `brain/notas/como-uso-meu-os.md`.

## Como instalar

Precisa de: macOS, Claude Code, `git` e `python3` (os dois vêm com as Ferramentas de Linha de Comando da Apple: `xcode-select --install`).

Abra o Claude Code em qualquer pasta e cole:

> Instale meu OS pessoal a partir do modelo `https://github.com/bernrg/os-base`. Clone em `~/Documents/OS` (se a pasta já existir, pare e me avise) e siga a seção "Instalação (roteiro para o Claude)" do `README.md` do clone, passo a passo, na ordem. Estou começando: antes de cada passo, me diga em uma frase o que ele faz. Não pule a entrevista e não rode `git push`.

## Instalação (roteiro para o Claude)

Você é o Claude Code instalando este OS para a pessoa que colou o pedido. Ela é a dona do OS. Siga na ordem; em cada passo, uma frase do que vai acontecer antes de executar.

1. **Pré-requisitos.** `git --version` e `python3 --version`. Faltou algum: pare e diga `xcode-select --install`.
2. **Nome.** Pergunte como ela quer ser chamada dentro do OS (é o nome que entra nas regras: "quem decide é …"). Se ela quiser outro nome de pasta que não `OS`, renomeie agora (`mv`), antes do passo 4: só letras sem acento, números e hífen.
3. **O OS é dela, não do modelo.** Dentro da pasta: `git remote remove origin`. A partir daqui, todo `cd` é por caminho absoluto.
4. **Ler as regras.** Leia `CLAUDE.md` inteiro. Elas valem desde já, em especial: nada de `git push`, `git add` sempre por caminho, segredo nunca em arquivo versionado.
5. **Ligar à máquina.** Avise que o próximo comando mexe em três lugares FORA da pasta, sem apagar nada: `~/.zshenv` e `~/.claude/settings.json` (com cópia de segurança de cada um) e a pasta de memória do Claude Code deste projeto em `~/.claude/projects/` (vira um atalho para `brain/memoria/`). Depois rode `.claude/bin/instalar "<nome dela>"`. Mostre a saída. O `doctor` do fim precisa sair sem nenhum `FAIL`; se sair com `FAIL`, leia a mensagem, conserte e rode `.claude/bin/instalar` de novo. `WARN` pode ficar.
6. **Entrevista.** Preencha `brain/CONTEXTO.md` e `brain/SOUL.md` perguntando a ela, **uma pergunta por vez, no máximo oito**, em linguagem simples. Cubra: quem ela é e o que faz; as frentes de trabalho (negócios, estudo, pessoal) e o papel dela em cada uma; as pessoas que aparecem no trabalho e o que cada uma cuida; o objetivo dos próximos meses; como ela quer que você fale e quando quer ser consultada antes de você agir; quanto ela já sabe de código e de git. Escreva curto (os dois arquivos são lidos em toda sessão) e tire os comentários `<!-- … -->` das seções preenchidas. **Nada sensível nesses arquivos**: senha, documento, endereço, saúde e finanças não entram (o lugar deles é `brain/privado/`, fora do git).
7. **Vocabulário.** Para cada frente de trabalho da entrevista, acrescente um termo em kebab-case ao bloco `VOCAB:dominio` de `brain/REGRAS.md` e ao bloco 7 de `brain/notas/painel.md`.
8. **Plugin (opcional, pergunte).** O `CLAUDE.md` usa as skills do plugin `superpowers` quando ele existe. Para instalar: `claude plugin install superpowers@claude-plugins-official`. Sem ele, o OS funciona igual.
9. **Primeiro commit dela.** Rode `.claude/bin/doctor` (sem `FAIL`) e comite por caminho, com a mensagem **literal** começando por `instalação:` (é o marco que a manutenção procura):
   ```
   git add CLAUDE.md STATUS.md README.md brain .claude
   git commit -m "instalação: OS de <nome>"
   ```
   Este `git add` de pastas inteiras vale só aqui, com a árvore recém-clonada e nenhuma outra sessão aberta. Não rode `git push`.
10. **Fechar.** Diga a ela: (a) fechar esta sessão e abrir o Claude Code **dentro da pasta do OS** (`cd ~/Documents/<pasta> && claude`), porque regras, memória e guardas só carregam em sessão nova; (b) a primeira coisa a pedir lá é "onde paramos?"; (c) para trazer um projeto que já existe (um site, por exemplo), pedir `/projeto-novo` com o endereço do repositório; (d) ao terminar de trabalhar, dizer "fechando".

## Depois de instalado

- **Sempre abra o Claude Code na raiz do OS.** Aberto dentro de um projeto, as regras não carregam inteiras (a guarda avisa).
- **A guarda perguntou:** leia o que o comando faz antes do sim. **A guarda negou:** não é para contornar; peça ao Claude que explique e mude o plano.
- **Pasta renomeada, Mac novo, ou `doctor` com `FAIL` de memória, zsh ou guardas:** `.claude/bin/instalar`.
- **O que o OS anota sozinho:** ao fechar uma sessão aberta dentro da pasta do OS, o coletor grava em `.claude/melhoria/ledger.jsonl` o começo do seu primeiro pedido, as suas correções e a contagem de erros. É o material do `/melhoria`. O arquivo é versionado: se o OS for para o GitHub, ele vai junto. Sessão aberta em outra pasta não é anotada.
- **Backup:** `brain/privado/` e `arquivo/` ficam fora do git de propósito e **não têm backup** neste desenho. Se guardar algo importante lá, ponha a pasta do OS num backup do Mac (Time Machine).
- **GitHub (opcional):** o OS funciona só local. Para ter cópia no GitHub, crie um repositório **privado** e peça o push ao Claude; a guarda vai pedir a sua confirmação.

## O que a guarda não faz

É cinto de segurança, não barreira. Ela lê o texto do comando: o que estiver em variável, `eval` ou dentro de um script não é visto, e por isso as mesmas regras continuam escritas no `CLAUDE.md`. A lista de padrões de segredo cobre os formatos comuns (chaves de API conhecidas, chave privada, string de conexão com senha, `senha = "…"` com valor de 12 ou mais caracteres misturando letra e número); senha fora desse molde passa, e texto que só parece senha pode ser barrado. Nos dois casos quem decide é você. Se a guarda falhar por dentro, ela deixa o comando seguir em vez de travar a máquina. Os testes dela rodam com `.claude/bin/guarda --selftest`.
