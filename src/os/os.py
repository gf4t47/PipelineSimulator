from src.simulator.cpu import Cpu


def _load(path: str)->bytearray:
    """
    load binary file
    :param path: binary file path
    :return: memory as bytearray
    """
    f = open(path, mode='rb')
    mem = bytearray(f.read())
    f.close()
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
