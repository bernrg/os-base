#!/usr/bin/env python3
"""Coletor de melhoria contínua — extrai sinais de atrito do transcript da sessão.

Modos:
  (sem args)   hook de SessionEnd: lê o JSON do evento no stdin, extrai sinais do
               transcript e appenda UMA linha JSON no ledger. NUNCA sai com !=0 —
               fim de sessão jamais bloqueia.
  --backfill   varre ~/.claude/projects/*/*.jsonl e appenda sessões ausentes.
  --selftest   testes embutidos contra fixtures; exit 0 se tudo passa.

Ledger: só append; dedup por session_id é na LEITURA (última linha vence).
"""
import json
import os
import re
import sys
import tempfile
from collections import Counter

OS_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LEDGER = os.path.join(OS_DIR, ".claude", "melhoria", "ledger.jsonl")
PROJECTS_DIR = os.path.expanduser("~/.claude/projects")

CORRECAO_RX = re.compile(
    r"\b(n[aã]o era isso|n[aã]o [eé] isso|errado|est[aá] errado|na verdade|"
    r"pare\b|para de|refa[zç]|desfa[zç]|volta atr[aá]s|n[aã]o fa[cç]a|"
    r"n[aã]o quero|em vez disso|wrong|instead|undo|stop)\b",
    re.I,
)
DENY_RX = re.compile(
    r"doesn't want to proceed|user rejected|denied by the Claude Code auto mode classifier",
    re.I,
)


def _texto(content):
    """Texto plano de um campo content (string ou lista de blocks)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def extrair(transcript_path, session_id, cwd=""):
    intent = ""
    erros = interrupcoes = negacoes = exit1 = 0
    sigs, corrections, skills = [], [], []
    edit_tops = []
    ts_end = None
    with open(transcript_path, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                e = json.loads(linha)
            except Exception:
                continue
            if e.get("timestamp"):
                ts_end = e["timestamp"]
            if not cwd and e.get("cwd"):
                cwd = e["cwd"]
            content = (e.get("message") or {}).get("content")
            if e.get("type") == "user":
                # Injeção do harness (corpo de skill, saída de comando, descrição
                # de imagem) chega como mensagem `user` com isMeta; a fala real
                # do dono carrega promptSource e nunca tem isMeta.
                if e.get("isMeta"):
                    continue
                if isinstance(content, list):
                    for b in content:
                        if isinstance(b, dict) and b.get("type") == "tool_result":
                            txt = _texto(b.get("content"))
                            if b.get("is_error"):
                                sig = (txt.strip().splitlines() or ["(erro sem texto)"])[0][:160]
                                # exit 1 é balde ambíguo (grep sem match vs falha real):
                                # campo próprio, fora da métrica que ordena sessões.
                                if sig.rstrip() == "Exit code 1":
                                    exit1 += 1
                                else:
                                    erros += 1
                                    if sig not in sigs and len(sigs) < 5:
                                        sigs.append(sig)
                            # Negação real chega sempre com is_error; sem o gate,
                            # output legítimo de ssh ("Permission denied") conta.
                            if b.get("is_error") and DENY_RX.search(txt):
                                negacoes += 1
                txt = _texto(content).strip()
                if not txt:
                    continue
                if "[Request interrupted" in txt:
                    interrupcoes += 1
                    continue
                if txt.startswith("<"):  # wrappers de comando/sistema
                    continue
                if txt.startswith("This session is being continued from a previous conversation"):
                    continue             # resumo de compactação: texto do sistema
                if not intent:
                    intent = txt[:200]
                elif CORRECAO_RX.search(txt) and len(corrections) < 5:
                    corrections.append(txt[:200])
            elif e.get("type") == "assistant" and isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_use" \
                            and b.get("name") in ("Edit", "Write"):
                        fp = (b.get("input") or {}).get("file_path") or ""
                        if fp:
                            rel = os.path.relpath(fp, OS_DIR)
                            if not rel.startswith("..") and os.sep in rel:
                                edit_tops.append(rel.split(os.sep)[0])
                    elif isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
                        s = (b.get("input") or {}).get("skill")
                        if s and s not in skills:
                            skills.append(s)
    # Pasta modal dos Edit/Write vence (o cwd é sempre a raiz, por regra do CLAUDE.md);
    # sem edits em pasta de projeto, vale o cálculo por cwd de sempre.
    NAO_PROJETO = {".claude", "brain", "documentos", "assets", "docs", "arquivo"}
    projeto = "-"
    modal = [t for t, _n in Counter(edit_tops).most_common() if t not in NAO_PROJETO]
    if modal:
        projeto = modal[0]
    elif cwd:
        rel = os.path.relpath(cwd, OS_DIR)
        if rel == ".":
            projeto = "raiz"
        elif not rel.startswith(".."):
            projeto = rel.split(os.sep)[0]
        else:
            projeto = os.path.basename(cwd)
    return {
        "session_id": session_id,
        "ts_end": ts_end,
        "projeto": projeto,
        "intent": intent,
        "erros": erros,
        "exit1": exit1,
        "interrupcoes": interrupcoes,
        "negacoes_permissao": negacoes,
        "error_sigs": sigs,
        "corrections": corrections,
        "skills": skills,
    }


def appender(rec):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def ids_no_ledger():
    ids = set()
    if os.path.isfile(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            for l in f:
                try:
                    ids.add(json.loads(l).get("session_id"))
                except Exception:
                    pass
    return ids


def modo_hook():
    try:
        dados = json.load(sys.stdin)
        sid = dados.get("session_id") or ""
        tp = dados.get("transcript_path") or ""
        if sid and tp and os.path.isfile(tp):
            appender(extrair(tp, sid, dados.get("cwd") or ""))
    except Exception:
        pass
    sys.exit(0)


def modo_backfill():
    vistos = ids_no_ledger()
    novos = 0
    if not os.path.isdir(PROJECTS_DIR):
        print("backfill: ~/.claude/projects/ não existe")
        return
    for proj in sorted(os.listdir(PROJECTS_DIR)):
        pdir = os.path.join(PROJECTS_DIR, proj)
        if not os.path.isdir(pdir):
            continue
        for fn in sorted(os.listdir(pdir)):
            if not fn.endswith(".jsonl"):
                continue
            sid = fn[:-6]
            if sid in vistos:
                continue
            try:
                appender(extrair(os.path.join(pdir, fn), sid))
                novos += 1
            except Exception as exc:
                print(f"aviso: {fn}: {exc}", file=sys.stderr)
    print(f"backfill: {novos} sessão(ões) nova(s) no ledger")


FIXTURE = [
    {"type": "user", "isMeta": True, "message": {"content":
        "Base directory for this skill: /x/skills/tdd\n\nIf a skill applies, stop. Use it instead."}},
    {"type": "user", "timestamp": "2026-07-20T10:00:00Z", "cwd": OS_DIR,
     "message": {"content": "Quero montar o painel de vendas da loja"}},
    {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "fim"}}]}},
    {"type": "user", "message": {"content": [
        {"type": "tool_result", "is_error": True,
         "content": [{"type": "text", "text": "Error: comando falhou\ndetalhe irrelevante"}]}]}},
    {"type": "user", "message": {"content": "[Request interrupted by user]"}},
    {"type": "user", "message": {"content": "não é isso, refaz o header da tabela"}},
    {"type": "user", "message": {"content": [
        {"type": "tool_result", "is_error": True,
         "content": [{"type": "text", "text": "The user doesn't want to proceed with this tool use."}]}]}},
    {"type": "user", "message": {"content": [
        {"type": "tool_result", "is_error": True,
         "content": [{"type": "text", "text": "Exit code 1\nsaída parcial do pipe"}]}]}},
    {"type": "user", "message": {"content": [
        {"type": "tool_result", "is_error": True,
         "content": [{"type": "text", "text": "Exit code 127\nzsh: command not found"}]}]}},
    {"type": "user", "message": {"content": [
        {"type": "tool_result",
         "content": [{"type": "text", "text": "ssh: Permission denied (publickey)."}]}]}},
    {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Edit",
         "input": {"file_path": os.path.join(OS_DIR, "site-painel", "app", "app.py")}}]}},
    {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Write",
         "input": {"file_path": os.path.join(OS_DIR, "site-painel", "migra.py")}}]}},
    {"type": "user", "timestamp": "2026-07-20T10:30:00Z", "message": {"content": "ok, agora ficou bom"}},
]


def modo_selftest():
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        for e in FIXTURE:
            f.write(json.dumps(e) + "\n")
        caminho = f.name
    try:
        r = extrair(caminho, "selftest-001")
        assert r["session_id"] == "selftest-001", r
        assert r["intent"].startswith("Quero montar o painel"), r
        assert r["erros"] == 3, r
        assert r["exit1"] == 1, r
        assert r["error_sigs"] == [
            "Error: comando falhou",
            "The user doesn't want to proceed with this tool use.",
            "Exit code 127",
        ], r
        assert r["interrupcoes"] == 1, r
        assert r["negacoes_permissao"] == 1, r
        assert r["corrections"] == ["não é isso, refaz o header da tabela"], r
        assert r["skills"] == ["fim"], r
        assert r["projeto"] == "site-painel", r
        assert r["ts_end"] == "2026-07-20T10:30:00Z", r
    finally:
        os.unlink(caminho)

    # Teste do fallback: sessão sem edits
    FIXTURE2 = [{"type": "user", "timestamp": "2026-07-20T10:00:00Z", "cwd": OS_DIR,
                 "message": {"content": "sessão sem edits"}}]
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        for e in FIXTURE2:
            f.write(json.dumps(e) + "\n")
        caminho2 = f.name
    try:
        r2 = extrair(caminho2, "selftest-002")
        assert r2["projeto"] == "raiz", r2   # sem edits, vale o cwd
    finally:
        os.unlink(caminho2)

    # Resumo de compactação: texto do sistema, não do dono —
    # não vira intent nem correção, mesmo com "na verdade" no corpo
    resumo = ("This session is being continued from a previous conversation that ran out of context. "
              "Summary: ... na verdade o pedido era outro ...")
    FIXTURE3 = [{"type": "user", "timestamp": "2026-07-20T10:00:00Z", "cwd": OS_DIR,
                 "message": {"content": resumo}},
                {"type": "user", "message": {"content": "Quero conferir o deploy"}},
                {"type": "user", "message": {"content": resumo}}]
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        for e in FIXTURE3:
            f.write(json.dumps(e) + "\n")
        caminho3 = f.name
    try:
        r3 = extrair(caminho3, "selftest-003")
        assert r3["intent"] == "Quero conferir o deploy", r3
        assert r3["corrections"] == [], r3
    finally:
        os.unlink(caminho3)

    print("selftest ok")
    print("linha de exemplo:", json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        modo_selftest()
    elif "--backfill" in sys.argv:
        modo_backfill()
    else:
        modo_hook()
