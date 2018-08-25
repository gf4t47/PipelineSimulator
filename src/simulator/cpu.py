from src.simulator.instruction import op_nop, op_ld, op_movi, op_st, op_inc, op_cmpi, op_bnz, op_halt
from src.util.log import log_err

inst_set = [
    ['nop', op_nop],
    ['ld', op_ld],
    ['movi', op_movi],
    ['st', op_st],
    ['inc', op_inc],
    ['cmpi', op_cmpi],
    ['bnz', op_bnz],
    ['halt', op_halt]
]


# noinspection PyPep8Naming
class cpu:
    def __init__(self):
        self.pc = 0
        self.reg = [0] * 12
        self.pstate = 0
        self.mem = None

    def load_program(self, path):
        f = open(path, mode='rb')
        self.mem = bytearray(f.read())
        f.close()

    def fetch(self):
        if self.pc < 0 or self.pc > 4096:
            log_err("sys abort due to invalid pc: %d" % self.pc, quited=True)

        op = self.mem[self.pc]
        if op >= len(inst_set):
            log_err("sys abort due to invalid inst op: %x" % op, quited=True)

        return self.mem[self.pc:self.pc + 4]

    def run(self, max_step):
        i = 0
        while i < max_step:
            inst = self.fetch()
            self.pc += inst_set[inst[0]][1](self, inst)
            i += 1
        log_err("cpu too hot (%d), exit" % max_step, quited=True)
