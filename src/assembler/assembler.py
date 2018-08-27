import os
from typing import Tuple, Callable, List

from src.assembler.instruction import inst_set_wrapper, relocate_label
from src.util.log import log


def _parse_line(line: str, pc: int, inst_set: {str: Tuple[Callable, List]}):
    log(f"encode: {line}")
    words = line.split()
    key = words[0].strip()
    if key not in inst_set:
        raise KeyError(f"No operation {key} in instruction set")
    encoder, info = inst_set[key]
    return encoder(words[1::], *info, pc)


def _parse_file(path: str):
    f = open(path)
    pc = 0
    labels = {}
    records = []
    inst_set = inst_set_wrapper(labels, records)

    instructions = []
    for line in f.readlines():
        if not line.isspace() and not line.startswith('#'):
            count, inst = _parse_line(line.strip(), pc, inst_set)
            if count == 1:
                instructions.append(inst)
            else:
                instructions.extend(inst)
            pc += count

    for record in records:
        r_pc, _, _, r_label, _ = record
        if r_label not in labels:
            raise KeyError(f"cannot find label {r_label}")

        log("relocate %x (label=%s on 0x%x) with inst(%x)" % (r_pc, r_label, labels[r_label], instructions[r_pc]))
        instructions[r_pc] = relocate_label(record, labels[r_label], inst_set)

    f.close()
    return instructions


def assemble(path: str):
    instructions = _parse_file(path)
    filename, _ = os.path.splitext(path)
    of = open(filename + '.exe', "w+b")
    assert of
    for inst in instructions:
        of.write(inst.to_bytes(4, 'little', signed=False))
    of.close()
