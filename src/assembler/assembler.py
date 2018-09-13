import os
from typing import Tuple, Callable, List

from src.assembler.instruction import make_inst_map, relocate_label
from src.util.converter import inst_to_bytes
from src.util.log import log


COMMENT_SYMBOL = ';'


def parse_line(line: str, pc: int, inst_map: {str: Tuple[Callable, bool, List]})->(Tuple[int, int], Tuple[int, List[int]]):
    """
    1. remove outline or inline comments if exist
    2. split string line to words list
    3. lookup encoder by operation key(words[0])
    4. execute encoder to encode the instruction(s)
    :param line: one line of asm file
    :param pc: program counter
    :param inst_map: instruction encoder map
    :return: (count of address the pc should move, instruction(s) content)
    """
    code = line.split(COMMENT_SYMBOL, 1)[0]  # remove inline comments
    words = code.split()
    key = words[0].strip()
    if key not in inst_map:
        raise KeyError(f"No operation {key} in instruction set")
    encoder, require_pc, info = inst_map[key]
    return encoder(words[1::], *info, pc) if require_pc else encoder(words[1::], *info)


def parse_file(lines: [str])->[int]:
    """
    Two times scan approach
    1. generate instructions for real operation and data
    2. generate instruction place holder ([records], [labels]) for pseudo code
    3. relocate each [record] to fill the real instruction via looking up [pc] in [labels]
    :param lines: asm file to lines of string
    :return: all generated instructions as List[int]
    """
    pc = 0
    labels = {}
    records = []
    inst_map = make_inst_map(labels, records)

    instructions = []
    for line in lines:
        words = line.strip()
        if words and (not words.isspace()) and (not words.startswith(COMMENT_SYMBOL)):
            count, insts = parse_line(words, pc, inst_map)
            if not isinstance(insts, list):
                instructions.append(insts)
            else:
                instructions.extend(insts)
            pc += count

    for record in records:
        r_pc, _, _, r_label, _ = record
        if r_label not in labels:
            raise KeyError(f"cannot find label {r_label}")

        instructions[r_pc] = relocate_label(record, labels[r_label], inst_map)
        log("relocate %x (label=%s on 0x%x) with inst(%x)", r_pc, r_label, labels[r_label], instructions[r_pc])

    return instructions


def assemble(path: str, extn='.bin')->str:
    """
    1. from asm file generate the instructions
    2. write the instructions into file
    :param path: asm file path
    :param extn: binary/executable file extension
    :return: generated binary/executable file path
    """
    f = open(path)
    instructions = parse_file(f.readlines())
    f.close()

    filename, _ = os.path.splitext(path)
    executable = filename + extn
    of = open(executable, "w+b")
    assert of

    for inst in instructions:
        of.write(inst_to_bytes(inst))
    of.close()

    return executable
