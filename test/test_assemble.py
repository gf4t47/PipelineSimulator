from src.assembler.assembler import assemble


def test_assemble_exe():
    assemble_file = '../data/test.s'
    assemble(assemble_file)


test_assemble_exe()
