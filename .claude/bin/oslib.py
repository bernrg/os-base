#!/usr/bin/env python3
"""oslib — lógica de manutenção compartilhada entre doctor e heartbeat.

Dono único: o filtro de auto-commits, o espelho do índice de memórias e a
idade da retrospectiva moram aqui; doctor e heartbeat só consomem.
`python3 oslib.py --selftest` roda os testes embutidos (cria repo git em tmp).
"""
import datetime
import os
import re
import subprocess
import sys


def git(root, *args, entrada=None):
    return subprocess.run(["git", "-C", root, *args],
                          capture_output=True, text=True, input=entrada)


def autocommits_sem_fim(root):
    """Hashes de auto-commits (SessionEnd) desde o último marco 'zelador: destilado',
    IGNORANDO os que só tocam .claude/melhoria/ledger.jsonl — coletor trabalhando
    não é sessão sem /fim."""
    marco = git(root, "log", "-1", "--format=%H", "--grep=^zelador: destilado").stdout.strip()
    faixa = [f"{marco}..HEAD"] if marco else []
    hashes = git(root, "log", *faixa, "--fixed-strings",
                 "--grep=sessão: auto-commit (SessionEnd)", "--format=%h").stdout.split()
    reais = []
    for h in hashes:
        arquivos = git(root, "show", "--name-only", "--format=", h).stdout.split()
        if arquivos != [".claude/melhoria/ledger.jsonl"]:
            reais.append(h)
    return reais


def indice_memorias(root):
    """(memórias sem linha no MEMORY.md, linhas do MEMORY.md sem arquivo)."""
    mem_dir = os.path.join(root, "brain", "memoria")
    if not os.path.isdir(mem_dir):
        return [], []
    arquivos = sorted(f for f in os.listdir(mem_dir)
                      if f.endswith(".md") and f != "MEMORY.md")
    idx_p = os.path.join(mem_dir, "MEMORY.md")
    idx = ""
    if os.path.isfile(idx_p):
        with open(idx_p, encoding="utf-8") as f:
            idx = f.read()
    links = [l for linha in idx.splitlines() if linha.lstrip().startswith("- ")
             for l in re.findall(r"\]\(([^)]+\.md)\)", linha)]
    sem_linha = [f for f in arquivos if f not in links]
    quebrados = [l for l in links if not os.path.isfile(os.path.join(mem_dir, l))]
    return sem_linha, quebrados


def retro_dias(root):
    """Dias desde a última retrospectiva (maior data AAAA-MM-DD.md em
    brain/notas/semanas/). Nome fora do padrão (ex.: template.md) é ignorado na
    conta, não vence por ordem alfabética. None só se a pasta não existir, estiver
    vazia, ou nenhum nome parsear como data."""
    sem_dir = os.path.join(root, "brain", "notas", "semanas")
    semanas = sorted(f for f in os.listdir(sem_dir)
                     if f.endswith(".md")) if os.path.isdir(sem_dir) else []
    datas = []
    for f in semanas:
        try:
            datas.append(datetime.date.fromisoformat(os.path.splitext(f)[0]))
        except ValueError:
            continue
    if not datas:
        return None
    return (datetime.date.today() - max(datas)).days


def retro_devida(root):
    """Frase do que falta, ou None. OS recém-instalado não deve retrospectiva: sem nenhuma
    escrita ainda, a conta parte do commit de instalação (`instalação: …`), ou do primeiro
    commit do repo. Marco é o commit, nunca um stamp."""
    dias = retro_dias(root)
    if dias is not None:
        return f"retrospectiva há {dias}d" if dias > 7 else None
    marco = git(root, "log", "-1", "--format=%ct", "--grep=^instalação:").stdout.strip()
    if not marco:
        marco = (git(root, "log", "--reverse", "--format=%ct").stdout.split() or [""])[0]
    if not marco:
        return None                      # repo sem commit: nada aconteceu ainda
    idade = (datetime.date.today() - datetime.date.fromtimestamp(int(marco))).days
    return "retrospectiva nunca escrita" if idade > 7 else None


def _selftest():
    import shutil
    import tempfile
    d = tempfile.mkdtemp()
    try:
        run = lambda *a: subprocess.run(a, cwd=d, capture_output=True, text=True)
        run("git", "init", "-q")
        run("git", "config", "user.email", "t@t")
        run("git", "config", "user.name", "t")
        os.makedirs(os.path.join(d, ".claude", "melhoria"))
        os.makedirs(os.path.join(d, "brain", "memoria"))
        with open(os.path.join(d, "x.md"), "w") as f:
            f.write("x")
        run("git", "add", "x.md")
        run("git", "commit", "-qm", "zelador: destilado")
        # auto-commit que só toca o ledger → ignorado
        with open(os.path.join(d, ".claude/melhoria/ledger.jsonl"), "w") as f:
            f.write("{}\n")
        run("git", "add", ".claude/melhoria/ledger.jsonl")
        run("git", "commit", "-qm", "sessão: auto-commit (SessionEnd)")
        # auto-commit que toca o brain → conta
        with open(os.path.join(d, "brain/memoria/MEMORY.md"), "w") as f:
            f.write("# MEMORY\n- [X](x.md) — gancho\n")
        run("git", "add", "brain/memoria/MEMORY.md")
        run("git", "commit", "-qm", "sessão: auto-commit (SessionEnd)")
        reais = autocommits_sem_fim(d)
        assert len(reais) == 1, reais
        sem_linha, quebrados = indice_memorias(d)
        assert sem_linha == [] and quebrados == ["x.md"], (sem_linha, quebrados)
        assert retro_dias(d) is None
        assert retro_devida(d) is None, "repo de hoje não deve retrospectiva"
        velho = {**os.environ, "GIT_COMMITTER_DATE": "2020-01-01T12:00:00", "GIT_AUTHOR_DATE": "2020-01-01T12:00:00"}
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "instalação: OS de teste"],
                       cwd=d, env=velho, capture_output=True)
        assert retro_devida(d) == "retrospectiva nunca escrita", retro_devida(d)
        os.makedirs(os.path.join(d, "brain", "notas", "semanas"))
        with open(os.path.join(d, "brain/notas/semanas/2020-01-05.md"), "w") as f:
            f.write("x")
        assert retro_dias(d) > 7
        assert retro_devida(d).startswith("retrospectiva há "), retro_devida(d)
        # nome fora do padrão (ex.: template.md) não pode vencer no sorted()[-1]
        # nem virar None: é só ignorado na conta, a data válida mais recente vale.
        with open(os.path.join(d, "brain/notas/semanas/template.md"), "w") as f:
            f.write("x")
        assert retro_dias(d) > 7
        print("oslib selftest ok")
    finally:
        shutil.rmtree(d)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
