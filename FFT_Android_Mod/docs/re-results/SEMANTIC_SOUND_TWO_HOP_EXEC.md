# sound_request: dois saltos ARM executados no Unicorn

ELF SHA-256: bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc

Janelas A32 originais executadas:
- 0x26b374 -> 0x2168e0: branch B original
- 0x2168e0 -> 0x271314: segundo branch B original
- 0x271314: parada ANTES da instrucao; efeito posterior desconhecido

Microexecucoes Unicorn verificadas: 8 (4 estados R0 x 2 estados CPSR).

Os registradores, flags e memoria sentinela foram preservados.
Nao houve leitura/escrita de dados nos dois saltos.
Nenhuma equivalencia de funcao, efeitos de som ou retorno foi certificada.

Limites: registros e memoria sinteticos; o destino final nao foi executado.
