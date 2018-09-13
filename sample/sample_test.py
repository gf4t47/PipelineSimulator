import pytest

from src.assembler.assembler import assemble
from src.os.os import execute


@pytest.mark.parametrize("assemble_name", [
    'sample/hello_world.asm'
])
def test_hello_world(assemble_name):
    executable = assemble(assemble_name)
    mem = execute(executable)
    assert mem is not None

    expected = 'HelloWorld'
    output = ''
    for index in range(1, len(expected) + 1):
        byte = mem[- (4 * index): - (4 * index) + 4] if index != 1 else mem[- (4 * index):]
        output += chr(int.from_bytes(byte, 'little', signed=False))

    print(output)
    assert expected == output[::-1]
