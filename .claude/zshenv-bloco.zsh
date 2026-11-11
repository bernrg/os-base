# >>> os: bloco do Bash tool do Claude Code (posto por .claude/bin/instalar) >>>
# O Bash tool do Claude Code é zsh NÃO-interativo (`zsh -c`); a cada chamada só este arquivo é lido.
# Sem a linha abaixo, glob sem match e `echo ====` (expansão =cmd) abortam a linha inteira, em
# silêncio: o comando sai com "Exit code 1" e saída pela metade. O terminal interativo não muda.
# NOMATCH desligado, não NULL_GLOB: com NULL_GLOB, `rm -rf pasta/*.x` sem match vira `rm -rf` solto.
# Guarda: doctor, check "zsh do Bash tool".
[[ -o interactive ]] || unsetopt EQUALS NOMATCH
# O macOS não tem `timeout` (GNU coreutils); reserva por perl. Só some se um `timeout` de verdade entrar no PATH.
# Aceita `timeout N[.N][s|m|h] cmd …` (fração arredonda para cima; 0 = sem prazo); o resto sai 125.
# Estouro: TERM no grupo do comando (netos inclusive), KILL até 2 s depois, sai 124 como o GNU.
# Guarda: doctor, check "timeout no Bash tool".
(( $+commands[timeout] )) || timeout() {
  local d=$1 n m=1
  case $d in
    (<->|<->.<->|<->s|<->.<->s) n=${d%s} ;;
    (<->m|<->.<->m) n=${d%m}; m=60 ;;
    (<->h|<->.<->h) n=${d%h}; m=3600 ;;
    (*) print -u2 "timeout: só 'timeout N[s|m|h] comando' (sem opções); recebeu '$d'"; return 125 ;;
  esac
  shift
  (( $# )) || { print -u2 "timeout: falta o comando"; return 125 }
  perl -e '
    my $t = shift; $t = int($t) + ($t > int($t) ? 1 : 0);
    my $pid = fork; die "timeout: fork: $!\n" unless defined $pid;
    if (!$pid) { setpgrp(0, 0); exec { $ARGV[0] } @ARGV;
                 print STDERR "timeout: $ARGV[0]: $!\n"; exit($!{ENOENT} ? 127 : 126) }
    $SIG{ALRM} = sub { kill "TERM", -$pid;
                       for (1 .. 20) { last if waitpid($pid, 1) > 0; select(undef, undef, undef, 0.1) }
                       kill "KILL", -$pid; exit 124 };
    $SIG{$_} = sub { kill "TERM", -$pid; exit 143 } for qw(TERM INT HUP);   # quem mata o timeout mata o comando
    alarm $t if $t > 0;
    waitpid($pid, 0);
    exit($? & 127 ? 128 + ($? & 127) : $? >> 8);
  ' -- "$(( n * m ))" "$@"
}
# <<< os: bloco do Bash tool do Claude Code <<<
