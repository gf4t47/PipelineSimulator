from src.simulator.cpu import Cpu


def _load(path: str)->bytearray:
    f = open(path, mode='rb')
    mem = bytearray(f.read())
    f.close()
    return mem


def process(file: str)->bytearray:
    mem = _load(file)
    cpu = Cpu(mem)
    return cpu.run(1000)
