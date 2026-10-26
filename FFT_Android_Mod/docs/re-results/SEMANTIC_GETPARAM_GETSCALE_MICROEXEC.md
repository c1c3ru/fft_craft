# Original ARM GetParam / GetScale — microexecuted contracts

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Two invocation modes are tested: from each callee entry with a synthetic LR, or through the actual original caller **BL**. The experiment stops on return before the next caller instruction.

## CFFT_STATE::GetParam(int)

Three original ARM opcodes: add 14 to r1, load indexed word from the r0 base table with a four-byte stride, return via BX LR. Verified exact data read, r0 return, r1 change, other register/flag preservation and neighboring canaries.
**GetParam microexecutions: 64/64 PASS.**

## CGX_SCREEN_CORRECT::GetScale(float*)

Four original ARM opcodes: CMP output pointer with zero; only if non-null, load a word at r0+4 and store to [r1], then return via BX LR. Null output performs no data reads/stores. Verified destination, conditional state, NZCV flags and canaries.
**GetScale microexecutions: 32/32 PASS.**

**Combined GetParam/GetScale microexecutions: 96/96 PASS.**

## Unverified

- Table contents and object/float destination are synthetic inputs.
- No caller code after the returning BL was executed.
- Sound playback and UI effects after these getters remain unknown.
- Tested local effects are NOT a complete semantic-equivalence proof.
