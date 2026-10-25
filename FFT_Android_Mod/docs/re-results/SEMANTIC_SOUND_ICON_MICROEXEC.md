# Bounded ARM sound dispatcher and icon-position prologue execution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

## SysSE_PlayDef(int) and preceding tail calls

Three original unconditional ARM B trampolines followed by three SysSE_PlayDef instructions are executed. `r1 = input`, `r0 = 0`; `LR` and NZCV preserved and no data memory read/written.
**Sound dispatcher microexecutions: 10/10 PASS.**
Stops **before** `0x2b2b7c`; no audio API effect established.

## iOS_SetIconPosition() entry

Ten original ARM instructions executed from `0x2b8900`; nine register saves (36 bytes), 36-byte local stack allocation, one verified local store/read, four PC-relative literal reads.
Total stack-frame depth observed: 72 bytes.
**Icon prologue microexecutions: 10/10 PASS.**
Stops **before** `0x2b8928`, its first indexed global-pointer dereference. Does not execute any deeper icon algorithm or BL.

## Unknowns

Original ARM code/literals are used; stack and register inputs are synthetic. Actual sound effects, global pointer contents, large-function control flow, runtime aliases and full-function semantic equivalence have **not** been established.
