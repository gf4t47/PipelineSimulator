import pytest

from src.assembler.assembler import assemble
from src.index import execute

DATA_MEMORY_BOUNDARY = 4096


@pytest.mark.parametrize("asm_file, expected", [
    ('./hello_world.asm', 'Hello World')
])
def test_memory_to_str(asm_file, expected):
    executable = assemble(asm_file)
    mem = execute(executable)
    assert mem is not None
    assert DATA_MEMORY_BOUNDARY * 2 == len(mem)

    actual = ''
    for index in range(1, len(expected) + 1):
        address = DATA_MEMORY_BOUNDARY - index * 4
        byte = mem[address: address + 4]
        actual += chr(int.from_bytes(byte, 'little', signed=False))

    assert expected == actual
