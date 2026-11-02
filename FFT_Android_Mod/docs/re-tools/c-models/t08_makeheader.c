/* Reconstruction of MakeHeader(int, int, CARD_HEADER*) (0x187264,
 * 688 B), per docs/REVERSE_ENGINEERING_NOTES.md section 678.
 *
 * First and only field evidence for CARD_HEADER -- the last of the
 * four types T08 (2026-10-31) listed with none at all (_Object,
 * ActionRequest and FFT_SAVE_DATA were closed in earlier slices this
 * session). Confirmed empirically against the real ELF via Unicorn
 * probing with distinct, recognizable values BEFORE writing this
 * model -- the dense GCC divide-by-constant codegen (smull/asr/rsb
 * triples for /10 and %10) was not hand-decoded instruction by
 * instruction; its net effect (plain integer /10, %10) was confirmed
 * by observing the real output bytes for known inputs instead,
 * exactly the project's own "empirical probing over continued manual
 * misreading" practice used elsewhere this session (T18/T26's double-
 * indirection bugs).
 *
 * Confirmed layout (byte offsets into CARD_HEADER; everything not
 * listed is NOT written by this function and NOT claimed to be any
 * particular size -- sizeof(CARD_HEADER) is NOT known beyond 0x100,
 * the highest offset this function itself touches):
 *   +0x00        'S'  (0x53)
 *   +0x01        'C'  (0x43)
 *   +0x02        0x11
 *   +0x03        0x01
 *   +0x04..+0x19 Fixed Shift-JIS title template, 22 B, decodes to
 *                "ＦＦＴ　ＦＩＬＥ　　　" ("FFT FILE" + 3 full-width
 *                spaces) -- confirmed by reading the real literal
 *                bytes at 0x308064 and decoding as Shift-JIS.
 *   +0x14..+0x17 Overwrites 2 of the template's 3 trailing spaces:
 *                (a0+1) as two full-width Shift-JIS digit characters
 *                (tens, units) -- NOT clamped (no cmp/movge for this
 *                one, confirmed by its absence, unlike the three
 *                values below).
 *   +0x1a..+0x1f "HH：" -- min(play_time.hours, 99) as two full-width
 *                digits + a full-width colon (0x8146).
 *   +0x20..+0x25 "MM：" -- min(play_time.minutes, 59), same shape.
 *   +0x26..+0x2b "SS　" -- min(play_time.seconds, 59) as two digits,
 *                followed by a full-width SPACE (0x8140), not a colon.
 *   +0x2c..+0x3f 20 B, verbatim copy of
 *                event_flag_table[read_eventflag(0x31)] (stride 20;
 *                the flag index 0x31=49 is a literal constant, read
 *                directly off the bytes, not inferred).
 *   +0x44..+0x5f Explicitly zeroed (memset), 28 B.
 *   +0x80..+0xff 128 B, verbatim copy from (g5_block + 0x20) -- a
 *                second external struct, single-indirection GOT
 *                access like event_flag_table, role not identified
 *                beyond "128 bytes read from offset +0x20 of it".
 *
 * `a1` (the function's second int parameter) is read nowhere in the
 * real body -- confirmed by its total absence from the disassembly
 * after the initial register move -- and is likewise unused here,
 * kept only to match the real signature's shape.
 *
 * read_eventflag, the global play_time triple, event_flag_table and
 * g5_block are all passed in as already-resolved parameters/function
 * pointers instead of replaying their own GOT-indirection chains
 * inside this file, for the same host/ARM pointer-width reasons as
 * every other c-model in this directory.
 */
#include <stdint.h>
#include <string.h>

typedef int32_t (*read_eventflag_fn)(int32_t flag_index);

static const uint8_t TITLE_TEMPLATE[22] = {
    0x82, 0x65, 0x82, 0x65, 0x82, 0x73, 0x81, 0x40, 0x82, 0x65, 0x82, 0x68,
    0x82, 0x6b, 0x82, 0x64, 0x81, 0x40, 0x81, 0x40, 0x81, 0x40,
};

static void write_fullwidth_digit(uint8_t *dest, int32_t digit) {
    dest[0] = 0x82;
    dest[1] = (uint8_t)(0x4f + digit);
}

static void write_two_digit_number(uint8_t *dest, int32_t value) {
    write_fullwidth_digit(dest, (value / 10) % 10);
    write_fullwidth_digit(dest + 2, value % 10);
}

void MakeHeader_model(
    int32_t a0, int32_t a1, uint8_t *out,
    const int32_t *play_time /* [0]=hours [1]=minutes [2]=seconds */,
    read_eventflag_fn read_eventflag,
    const uint8_t *event_flag_table /* stride 20 */,
    const uint8_t *g5_block) {
    (void)a1; /* confirmed unused by the real function body */

    out[0x00] = 'S';
    out[0x01] = 'C';
    out[0x02] = 0x11;
    out[0x03] = 0x01;

    memset(out + 0x44, 0, 0x1c);

    memcpy(out + 0x04, TITLE_TEMPLATE, sizeof(TITLE_TEMPLATE));

    int32_t n0 = a0 + 1; /* NOT clamped, confirmed */
    write_two_digit_number(out + 0x14, n0);

    int32_t hours = play_time[0];
    if (hours >= 99) {
        hours = 99;
    }
    write_two_digit_number(out + 0x1a, hours);
    out[0x1e] = 0x81;
    out[0x1f] = 0x46; /* full-width colon */

    int32_t minutes = play_time[1];
    if (minutes >= 59) {
        minutes = 59;
    }
    write_two_digit_number(out + 0x20, minutes);
    out[0x24] = 0x81;
    out[0x25] = 0x46; /* full-width colon */

    int32_t seconds = play_time[2];
    if (seconds >= 59) {
        seconds = 59;
    }
    write_two_digit_number(out + 0x26, seconds);
    out[0x2a] = 0x81;
    out[0x2b] = 0x40; /* full-width space, not a colon */

    int32_t flag_result = read_eventflag(0x31);
    memcpy(out + 0x2c, event_flag_table + (int64_t)flag_result * 20, 20);

    memcpy(out + 0x80, g5_block + 0x20, 0x80);
}
