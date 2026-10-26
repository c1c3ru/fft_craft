# ARM sound and icon — bounded pointer dereference microexecution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

## SysSE_Play(int,int) prologue to first BL

Executes 7 original ARM instructions at `0x2b2b7c..0x2b2b94`. Saves 8 registers (32 bytes), reserves 32 more stack bytes, reads one PC-relative literal and one derived pointer. Pre-call `r0` equals synthetic indexed pointer word and `r1=0x28`.
Sound next-boundary microexecutions: **30/30 PASS**.
Stops **before** `BL 0x28c320` at `0x2b2b98`. No heap allocator, audio backend or sound playback was executed.

## iOS_SetIconPosition() first global-pointer read

Executes 14 original ARM instructions from `0x2b8900` through `0x2b8934`, including `LDR r5, [r2,r3]` at `0x2b8928`. The indexed address comes from two original ELF literal words; adjacent canaries and 72-byte stack frame are verified. `r0` before call equals the controlled memory word.
Icon first-global-read microexecutions: **30/30 PASS**.
Stops **before** `BL 0xa6f28` at `0x2b8938`.

## Limitations

Global words, stack and arguments are synthetic. The two external calls are **not executed**; the post-call effects and full function semantics remain unverified. These microexecutions do not establish equivalence.
