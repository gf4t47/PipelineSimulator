import sys

from src.simulator.cpu import DATA_MEMORY_BOUNDARY
from src.util.converter import inst_to_bytes, imme_to_int, inst_to_int
from src.util.log import log_err, log


# noinspection PyUnusedLocal
def _op_nop(cpu: 'Cpu', inst: bytearray)->int:
    """
    nop                     no operation
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    log("nop")
    return 4


def _op_ld(cpu: 'Cpu', inst: bytearray)->int:
    """
    ld <Tr> <Ar>            load data from address
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    tr = inst[1]
    sr = inst[2]
    addr = cpu.register[sr]
    if addr < 0 or addr > DATA_MEMORY_BOUNDARY * 2:
        log_err("segment fault on address 0x%x", cpu.register[sr])

    if addr >= DATA_MEMORY_BOUNDARY:
        log_err("invalid read io(0x%x value=0x%x)!", cpu.register[tr], addr - DATA_MEMORY_BOUNDARY)
    else:
        cpu.register[tr] = inst_to_int(cpu.memory[addr: addr + 4])

    log("load from r%d(0x%x value=0x%x) to r%d", sr, addr, cpu.register[tr], tr)
    return 4


def _op_movi(cpu: 'Cpu', inst: bytearray)->int:
    """
    movi <Tr> <imme>        move imme to reg
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    tr = inst[1]
    imme = imme_to_int(inst[2: 4])
    cpu.register[tr] = imme
    log("set 0x%x to r%d", cpu.register[tr], tr)
    return 4


def _op_st(cpu: 'Cpu', inst: bytearray)->int:
    """
    st <Dr> <Ar>            store data to address
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    tr = inst[1]
    sr = inst[2]
    addr = cpu.register[sr]
    if addr < 0 or addr > 8192:
        log_err("segment fault on address 0x%x", cpu.register[sr])

    if addr >= DATA_MEMORY_BOUNDARY:
        if addr == DATA_MEMORY_BOUNDARY:
            log_err("invalid addr(%c)", (inst_to_bytes(cpu.register[tr])[0]))
        else:
            log_err("invalid io(0x%x)!", (cpu.register[tr]))
    else:
        cpu.memory[addr: addr + 4] = inst_to_bytes(cpu.register[tr])

    log("store r%d(0x%x) to 0x%x", tr, cpu.register[tr], addr)
    return 4


def _op_inc(cpu: 'Cpu', inst: bytearray)->int:
    """
    inc <Tr>                Tr+1
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    tr = inst[1]
    cpu.register[tr] += 1
    log("inc r%d to 0x%x", tr, cpu.register[tr])
    return 4


def _op_cmpi(cpu: 'Cpu', inst: bytearray)->int:
    """
    cmpi <Sr>, <imme>       compare with imme
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    tr = inst[1]
    imme = imme_to_int(inst[2: 4])
    cpu.pstate &= 0
    if cpu.register[tr] > imme:
        cpu.pstate |= 0x2  # bigger than bit
    elif cpu.register[tr] == imme:
        cpu.pstate |= 0x1  # zero bit

    log("compare r%d(0x%x) with 0x%x, pstate=0x%x", tr, cpu.register[tr], imme, cpu.pstate)
    return 4


def _op_bnz(cpu: 'Cpu', inst: bytearray)->int:
    """
    bz <imme>               relative branch to address
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    imme = imme_to_int(inst[2: 4])
    if cpu.pstate & 0x1:
        log("branch untaken")
        return 4
    else:
        log("branch to %x", imme)
        return imme


# noinspection PyUnusedLocal
def _op_halt(cpu: 'Cpu', inst: bytearray)->None:
    """
    halt                    halt the cpu
    :param cpu: 'Cpu' instance
    :param inst: one instruction
    """
    log("halt")
    sys.exit(0)


"""
ld <Tr> <Ar>            load data from memory (address hold by Address Register) to Temporary Register
movi <Tr> <imme>        move immediate value to Temporary Register
st <Dr> <Ar>            store data from Data Register to memory (address hold by Address Register)
inc <Tr>                Temporary Register += 1
cmpi <Sr>, <imme>       compare Temporary Register with immediate value, store result in Flag Register
bnz <imme>              relative branch to address if Flag Register is non-zero
nop                     no operation
halt                    halt the cpu
"""
inst_set = [
    ('nop', _op_nop),       # instruction[0] == 0
    ('ld', _op_ld),         # instruction[0] == 1
    ('movi', _op_movi),     # instruction[0] == 2
    ('st', _op_st),         # instruction[0] == 3
    ('inc', _op_inc),       # instruction[0] == 4
    ('cmpi', _op_cmpi),     # instruction[0] == 5
    ('bnz', _op_bnz),       # instruction[0] == 6
    ('halt', _op_halt)      # instruction[0] == 7
]
