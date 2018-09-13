import pytest

from src.assembler.assembler import assemble
from src.index import execute


@pytest.mark.parametrize("asm_file, expected", [
    ('sample/hello_world.asm', 'Hello World')
])
def test_memory_to_str(asm_file, expected):
    executable = assemble(asm_file)
    mem = execute(executable)
    assert mem is not None

    output = ''
    for index in range(1, len(expected) + 1):
        byte = mem[- (4 * index): - (4 * index) + 4] if index != 1 else mem[- (4 * index):]
        output += chr(int.from_bytes(byte, 'little', signed=False))

    assert expected == output[::-1]
