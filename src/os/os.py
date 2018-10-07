from src.simulator.cpu import Cpu
from src.simulator.instruction import DATA_MEMORY_BOUNDARY


def _load(path: str)->bytearray:
    """
    load binary file
    :param path: binary file path
    :return: memory as bytearray
    """
    with open(path, mode='rb') as f:
        mem = bytearray(f.read())
        size = len(mem)
        due = DATA_MEMORY_BOUNDARY * 2 - size
        if due < 0:
            raise RuntimeError(f'memory out of range: {size} > {DATA_MEMORY_BOUNDARY * 2}')
        elif due > 0:
            mem[size: DATA_MEMORY_BOUNDARY * 2] = bytes([0]) * due

        return mem


def process(file: str)->bytearray:
    """
    1. init memory from binary executable file
    2. init CPU from memory
    3. execute the CPU
    :param file: binary file path
    :return: memory after execution
    """
    mem = _load(file)
    cpu = Cpu(mem)
    return cpu.run(1000)
