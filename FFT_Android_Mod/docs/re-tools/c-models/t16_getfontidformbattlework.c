/* Reconstruction of getFontIDFormBattleWork(int) (0x20e880, 64 B),
 * per docs/REVERSE_ENGINEERING_NOTES.md section 686.
 *
 * Walks a global singly-linked list (head resolved via GOT, a
 * standard address-of-pointer-variable double indirection); each
 * node has a `next` pointer at +0x0, a font id byte at +0x5, and a
 * pointer to a BWORK instance at +0x134 (skipped if null). Returns
 * the first node's font id byte whose BWORK's +0x1ac matches the
 * target, or -1 if the list is exhausted without a match.
 *
 * Real finding, a cross-session cross-reference confirmed by
 * address, not assumed: BWORK+0x1ac is ALREADY a confirmed field
 * (docs/re-baseline/types/bwork.h, "origByte1ac in
 * set_casting_status", NOTES sec. 653 -- feeds a "dir" value into
 * _changeAnimationStatus_). This function reads that exact same
 * offset of a BWORK pointed to from elsewhere, independently
 * confirming it is a real, meaningful byte field rather than
 * guessed from this function's own body alone. No claim is made
 * that this function's `target` parameter is itself a "direction";
 * only that it is compared against the same confirmed BWORK offset.
 *
 * `next`/`bwork` are native pointers (not ARM-width struct fields)
 * for the same host/ARM pointer-width reason as every other c-model
 * in this directory that chases real pointers -- see
 * test_t16_getfontidformbattlework.c for how the real ELF side
 * still builds a byte-exact ARM-shaped linked list.
 */
#include <stddef.h>
#include <stdint.h>

typedef struct Node {
    struct Node *next;
    uint8_t font_id;
    uint8_t *bwork;
} Node;

int32_t getFontIDFormBattleWork_model(int32_t target, Node *list_head) {
    Node *node = list_head;
    while (node != NULL) {
        if (node->bwork != NULL) {
            uint8_t byte_0x1ac = node->bwork[0x1ac];
            if ((int32_t)byte_0x1ac == target) {
                return node->font_id;
            }
        }
        node = node->next;
    }
    return -1;
}
