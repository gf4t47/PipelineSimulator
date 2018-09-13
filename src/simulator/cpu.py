from src.simulator.instruction import inst_set, DATA_MEMORY_BOUNDARY
from src.util.log import log_err


class Cpu:
    def __init__(self, mem: bytearray)->None:
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
    def register(self)->[int]:
        return self._reg

    @property
    def memory(self)->bytearray:
        return self._mem

    def _fetch(self)->bytearray:
        """
        get one instruction from memory
        :return: instruction: bytearray(4)
        """
        if self.pc < 0 or self.pc > DATA_MEMORY_BOUNDARY:
            log_err(f"sys abort due to invalid pc: {self.pc}")

        op = self.memory[self.pc]
        if op >= len(inst_set):
            log_err(f"sys abort due to invalid inst op: {op}")

        return self.memory[self.pc: self.pc + 4]

    def run(self, max_step: int)->bytearray:
        """
        execute binary instructions from memory
        :param max_step: max step threshold, otherwise CPU will be on fire
        :return: memory states after the execution
        """
        count_step = 0

        while count_step < max_step:
            inst = self._fetch()
            _, inst_handler = inst_set[inst[0]]
            try:
                self.pc += inst_handler(self, inst)
            except RuntimeError:
                return self.memory
            count_step += 1

        log_err(f"cpu too hot ({max_step}), exit")
        return self.memory
