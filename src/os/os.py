from src.simulator.cpu import Cpu


def _load(path: str):
    f = open(path, mode='rb')
    mem = bytearray(f.read())
    f.close()
    return mem


def execute(file: str):
    mem = _load(file)
    cpu = Cpu(mem)
    cpu.run(1000)
