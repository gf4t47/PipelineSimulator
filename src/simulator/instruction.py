"""
ld <Tr> <Ar>            #load
movi <Tr> <imme>        #move imme
st <Dr> <Ar>            #store data to address
inc <Tr>                #Tr+1
cmpi <Sr>, <immu>       #compare with imme
bz <immu>               #relative branch to address
nop                     #no operation
halt                    #halt the cpu
"""
import sys

from src.util.log import log_err, log


def op_nop(cpu, inst):
    log("nop")
    return 4


def op_ld(cpu, inst):
    tr = inst[1]
    sr = inst[2]
    addr = cpu.reg[sr]
    if addr < 0 or addr > 8192:
        log_err("segment fault on address 0x%x" % (cpu.reg[sr]), quited=True)

    if addr >= 4096:
        print("invalid read io(0x%x value=0x%x)!" % (cpu.reg[tr], addr - 4096))
    else:
        cpu.reg[tr] = int.from_bytes(cpu.mem[addr:addr + 4], 'little', signed=False)

    log("load from r%d(0x%x value=0x%x) to r%d" % (sr, addr, cpu.reg[tr], tr))

    return 4


def op_movi(cpu, inst):
    tr = inst[1]
    imme = int.from_bytes(inst[2:4], 'little', signed=True)
    cpu.reg[tr] = imme
    log("set 0x%x to r%d" % (cpu.reg[tr], tr))
    return 4


def op_st(cpu, inst):
    tr = inst[1]
    sr = inst[2]
    addr = cpu.reg[sr]
    if addr < 0 or addr > 8192:
        log_err("segment fault on address 0x%x" % (cpu.reg[sr]), quited=True)

    if addr >= 4096:
        if addr == 4096:
            print("%c" % (cpu.reg[tr].to_bytes(4, 'little')[0]), end='')
            # print("%x "%(cpu.reg[tr].to_bytes(4, 'little')[0]), end='')
        else:
            print("invalid io(0x%x)!" % (cpu.reg[tr]))
    else:
        cpu.mem[addr:addr + 4] = cpu.reg[tr].to_bytes(4, 'little')

    log("store r%d(0x%x) to 0x%x" % (tr, cpu.reg[tr], addr))

    return 4


def op_inc(cpu, inst):
    tr = inst[1]
    cpu.reg[tr] += 1
    log("inc r%d to 0x%x" % (tr, cpu.reg[tr]))
    return 4


def op_cmpi(cpu, inst):
    tr = inst[1]
    imme = int.from_bytes(inst[2:4], 'little', signed=True)
    cpu.pstate &= 0
    if cpu.reg[tr] > imme:
        cpu.pstate |= 0x2  # bigger than bit
    elif cpu.reg[tr] == imme:
        cpu.pstate |= 0x1  # zero bit

    log("compare r%d(0x%x) with 0x%x, pstate=0x%x" % (tr, cpu.reg[tr], imme, cpu.pstate))
    return 4


def op_bnz(cpu, inst):
    imme = int.from_bytes(inst[2:4], 'little', signed=True)
    if cpu.pstate & 0x1:
        log("branch untaken")
        return 4
    else:
        log("branch to %x" % imme)
        return imme


def op_halt(cpu, inst):
    log("halt")
    sys.exit(0)
