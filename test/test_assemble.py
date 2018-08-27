from src.assembler.assembler import assemble


def test_assemble_exe():
    assemble_file = '../data/test.asm'
    assemble(assemble_file)


test_assemble_exe()
