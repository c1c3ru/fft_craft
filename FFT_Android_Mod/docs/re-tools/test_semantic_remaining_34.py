"""Synthetic opcode and machine-state regression tests for issue #388."""
import unittest
from unittest import mock
import semantic_remaining_34 as loop
import semantic_evidence


def words(*items):
    return b"".join(item.to_bytes(4, "little") for item in items)


class Remaining34Tests(unittest.TestCase):
    def test_str_word_then_bx_lr_strict_decoder(self):
        for word, base, source, offset in (
            (0xe5801000, 0, 1, 0),
            (0xe5810004, 1, 0, 4),
            (0xe583200c, 3, 2, 12),
            (0xe5800000, 0, 0, 0),
        ):
            with self.subTest(word=hex(word)):
                spec=loop.decode_store(words(word,0xe12fff1e),0xa1000)
                self.assertIsNotNone(spec)
                self.assertEqual((spec['base'],spec['source'],spec['offset']),
                                 (base,source,offset))

    def test_unknown_writes_and_nonreturns_are_excluded(self):
        for word in (0x15801000, 0xe5a01000, 0xe4801000,
                     0xe5c01000, 0xe5901000, 0xe5841000,
                     0xe5804000, 0xe5801002, 0xe5801104):
            with self.subTest(word=hex(word)):
                self.assertIsNone(loop.decode_store(words(word,0xe12fff1e),0xa1000))
        self.assertIsNone(loop.decode_store(words(0xe5801000,0xe12fff10),0xa1000))
        self.assertIsNone(loop.decode_store(words(0xe5801000,0xe12fff1e),0xa1002))
        self.assertIsNone(loop.decode_store(words(0xe5801000),0xa1000))

    def test_reference_models_pointer_aliasing(self):
        spec=loop.decode_store(words(0xe5800000,0xe12fff1e),0xa1000)
        regs,val=loop.reference(0x12345678,spec)
        self.assertEqual(regs[0],loop.BASE)
        self.assertEqual(val,loop.BASE)

    def test_real_unicorn_runs_isolated_synthetic_store(self):
        cases=((0xe5801000, 0), (0xe5810004, 4),
               (0xe583200c, 12), (0xe5800000, 0))
        for word,off in cases:
            with self.subTest(opcode=hex(word)):
                address=0xa1000
                raw=words(word,0xe12fff1e)
                spec=loop.decode_store(raw,address)
                row={'address':f'{address:08x}','size':8,'raw_hex':raw.hex(),
                     'contract':spec}
                def checked_reader(binary,start,size):
                    if (start,size)!=(address,8):
                        raise ValueError('unexpected ELF read')
                    return raw
                with mock.patch.object(semantic_evidence,'read_function',
                                       side_effect=checked_reader):
                    for seed in (0,0x12345678,0xffffffff):
                        for flags in (0,0x40000000,0x90000000):
                            loop.execute(None,row,seed,flags)

    def test_stale_checkpoint_identity_and_no_certification(self):
        state=loop.build('a'*64,'b'*64,[],[])
        self.assertEqual(state['new_certificates'],0)
        self.assertIn('Certificados originais: inalterados',loop.render(state))
        self.assertEqual(state['rounds'],[])


if __name__=='__main__':
    unittest.main()
