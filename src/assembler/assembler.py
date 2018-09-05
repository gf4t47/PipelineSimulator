"""
  Copyright (C) 2018 Kenneth Lee. All rights reserved.
  Modifications copyright (C) 2018 <Laserfiche/Kern Ding>

 TLicensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import os
from typing import Tuple, Callable, List

from src.assembler.instruction import make_inst_map, relocate_label
from src.util.converter import inst_to_bytes
from src.util.log import log


COMMENT_SYMBOL = ';'


def parse_line(line: str, pc: int, inst_map: {str: Tuple[Callable, bool, List]}):
    log(f"encode: {line}")
    code = line.split(COMMENT_SYMBOL, 1)[0]  # remove inline comments
    words = code.split()
    key = words[0].strip()
    if key not in inst_map:
        raise KeyError(f"No operation {key} in instruction set")
    encoder, require_pc, info = inst_map[key]
    return encoder(words[1::], *info, pc) if require_pc else encoder(words[1::], *info)


def parse_file(lines: [str]):
    pc = 0
    labels = {}
    records = []
    inst_map = make_inst_map(labels, records)

    instructions = []
    for line in lines:
        words = line.strip()
        if words and (not words.isspace()) and (not words.startswith(COMMENT_SYMBOL)):
            count, inst = parse_line(words, pc, inst_map)
            if not isinstance(inst, list):
                instructions.append(inst)
            else:
                instructions.extend(inst)
            pc += count

    for record in records:
        r_pc, _, _, r_label, _ = record
        if r_label not in labels:
            raise KeyError(f"cannot find label {r_label}")

        instructions[r_pc] = relocate_label(record, labels[r_label], inst_map)
        log("relocate %x (label=%s on 0x%x) with inst(%x)", r_pc, r_label, labels[r_label], instructions[r_pc])

    return instructions


def assemble(path: str, extn='.bin'):
    f = open(path)
    instructions = parse_file(f.readlines())
    f.close()

    filename, _ = os.path.splitext(path)
    of = open(filename + extn, "w+b")
    assert of

    for inst in instructions:
        of.write(inst_to_bytes(inst))
    of.close()
