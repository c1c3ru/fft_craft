"""Minimal synthetic ELF32/ARM .so builder, for tests that need a real file
pyelftools can parse (jtable.py/struct_pass.py read sections directly from
disk) without depending on the real, large libgl2jni.so binary.
"""
import struct

ELF_HEADER_SIZE = 52
SHDR_SIZE = 40
TEXT_VADDR = 0x1000  # chosen so sh_addr == sh_offset, keeping va_to_off trivial


def build_elf(text_bytes: bytes) -> bytes:
    """One PROGBITS '.text' section at TEXT_VADDR (== its file offset),
    containing exactly `text_bytes`, plus the NULL and .shstrtab sections
    pyelftools requires to enumerate anything at all.
    """
    shstrtab = b"\x00.text\x00.shstrtab\x00"
    text_off = TEXT_VADDR
    shstrtab_off = text_off + len(text_bytes)
    shoff = shstrtab_off + len(shstrtab)

    e_ident = b"\x7fELF" + bytes([1, 1, 1, 0]) + b"\x00" * 8
    ehdr = e_ident + struct.pack(
        "<HHIIIIIHHHHHH",
        3, 40, 1, 0, 0, shoff, 0, ELF_HEADER_SIZE, 0, 0, SHDR_SIZE, 3, 2,
    )
    assert len(ehdr) == ELF_HEADER_SIZE

    null_shdr = struct.pack("<10I", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    text_shdr = struct.pack(
        "<10I", 1, 1, 0x6, TEXT_VADDR, text_off, len(text_bytes), 0, 0, 4, 0,
    )  # sh_type=SHT_PROGBITS, sh_flags=SHF_ALLOC|SHF_EXECINSTR
    shstrtab_shdr = struct.pack(
        "<10I", 7, 3, 0, 0, shstrtab_off, len(shstrtab), 0, 0, 1, 0,
    )  # sh_type=SHT_STRTAB

    body = bytearray()
    body += ehdr
    body += b"\x00" * (text_off - len(ehdr))
    body += text_bytes
    body += shstrtab
    body += null_shdr + text_shdr + shstrtab_shdr
    return bytes(body)
