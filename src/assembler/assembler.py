import os
from typing import Tuple, Callable, List

from src.assembler.instruction import make_inst_set, relocate_label
from src.util.converter import inst_to_bytes
from src.util.log import log


def parse_line(line: str, pc: int, inst_set: {str: Tuple[Callable, List]}):
    log(f"encode: {line}")
    words = line.split()
    key = words[0].strip()
    if key not in inst_set:
        raise KeyError(f"No operation {key} in instruction set")
    encoder, info = inst_set[key]
    return encoder(words[1::], *info, pc)


def parse_file(lines: [str]):
    pc = 0
    labels = {}
    records = []
    inst_set = make_inst_set(labels, records)

    instructions = []
    for line in lines:
        words = line.strip()
        if words and (not words.isspace()) and (not words.startswith('#')):
            count, inst = parse_line(words, pc, inst_set)
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

    return instructions


def assemble(path: str):
    f = open(path)
    instructions = parse_file(f.readlines())
    f.close()

    filename, _ = os.path.splitext(path)
    of = open(filename + '.exe', "w+b")
    assert of

    for inst in instructions:
        of.write(inst_to_bytes(inst))
    of.close()
