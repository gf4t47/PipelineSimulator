import pytest

from src.assembler.assembler import assemble
from src.index import execute


@pytest.mark.parametrize("assemble_name, expected", [
    ('sample/hello_world.asm', 'Hello World')
])
def test_memory_to_str(assemble_name, expected):
    executable = assemble(assemble_name)
    mem = execute(executable)
    assert mem is not None

    output = ''
    for index in range(1, len(expected) + 1):
        byte = mem[- (4 * index): - (4 * index) + 4] if index != 1 else mem[- (4 * index):]
        output += chr(int.from_bytes(byte, 'little', signed=False))

    assert expected == output[::-1]
