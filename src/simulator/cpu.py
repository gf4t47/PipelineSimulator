from src.simulator.instruction import inst_list
from src.util.log import log_err


class Cpu:
    def __init__(self, mem: bytearray):
        self._pc = 0
        self._reg = [0] * 12
        self._pstate = 0
        self._mem = mem

    @property
    def pc(self)->int:
        return self._pc

    @pc.setter
    def pc(self, value: int)->None:
        self._pc = value

    @property
    def pstate(self)->int:
        return self._pstate

    @pstate.setter
    def pstate(self, value: int):
        self._pstate = value

    @property
    def reg(self)->[int]:
        return self._reg

    @property
    def mem(self)->bytearray:
        return self._mem

    def fetch(self)->bytearray:
        """
        get one instruction from memory
        :return: instruction
        """
        if self.pc < 0 or self.pc > 4096:
            log_err(f"sys abort due to invalid pc: {self.pc}")

        op = self.mem[self.pc]
        if op >= len(inst_list):
            log_err(f"sys abort due to invalid inst op: {op}")

        return self.mem[self.pc: self.pc + 4]

    def run(self, max_step: int):
        """
        execute binary instructions from memory
        :param max_step:
        :return:
        """
        count_step = 0
        while count_step < max_step:
            inst = self.fetch()
            self.pc += inst_list[inst[0]][1](self, inst)
            count_step += 1
        log_err(f"cpu too hot ({max_step}), exit")
