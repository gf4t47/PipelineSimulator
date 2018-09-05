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

from typing import Tuple, List, Callable

from src.util.converter import inst_to_int, imme_to_bytes
from src.util.log import log


def __str_to_imme(word: str) -> int:
    """
    convert word in assemble to immediate value
    :param word: input string
    :return: immediate value
    """
    imme = int(word, 0)
    if imme < -0x7fff or imme > 0x7fff:
        raise ValueError(f"bad imme {word}")
    return imme


def __str_to_reg(word: str, target_reg: bool) -> int:
    """
    convert word in assemble to register NO.
    :param word: input string
    :param target_reg: indicated it's a target register or not
    :return: register NO.
    """
    reg = int(word)
    if reg < 1 if target_reg else 0 or reg > 12:
        raise ValueError(f"bad register id: {word}")
    return reg


def _assemble_inst(op: int, tr: int) -> bytearray:
    inst = bytearray(4)
    inst[0] = op
    inst[1] = tr
    return inst


def _assemble_reg_inst(op: int, tr: int, sr1: int, sr2: int) -> bytearray:
    """
    assemble a instruction as [op, target register, source register 1, source register 2]
    :param op: operation code
    :param tr: target register
    :param sr1: source register 1
    :param sr2: source register 2
    :return: one instruction to be executed
    """
    inst = _assemble_inst(op, tr)
    inst[2] = sr1
    inst[3] = sr2
    log(f"{op}, {tr}, {sr1}, {sr2} -> {inst_to_int(inst)}")
    return inst


def _assemble_imme_inst(op: int, tr: int, imme: int) -> bytearray:
    """
    encode a instruction as [op, target register, immediate value low byte, immediate value high byte]
    :param op: operation
    :param tr: target register
    :param imme: a real word as value
    :return: one instruction to be executed
    """
    inst = _assemble_inst(op, tr)
    inst[2: 4] = imme_to_bytes(imme)
    log("%d, %d, %d -> %x", op, tr, imme, inst_to_int(inst))
    return inst


# noinspection PyUnusedLocal
def encode_no_op(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, inst_to_int(_assemble_reg_inst(op_code, 0, 0, 0))


def encode_reg_imme(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, inst_to_int(_assemble_imme_inst(op_code, __str_to_reg(words[0], target_reg=True), __str_to_imme(words[1])))


def encode_reg_reg(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, inst_to_int(_assemble_reg_inst(op_code, __str_to_reg(words[0], target_reg=True), __str_to_reg(words[1], target_reg=False), 0))


def encode_reg(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, inst_to_int(_assemble_reg_inst(op_code, __str_to_reg(words[0], target_reg=True), 0, 0))


def encode_imme(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, inst_to_int(_assemble_imme_inst(op_code, 0, __str_to_imme(words[0])))


def prepare_mem_data(words: [str]) -> (Tuple[int, int], Tuple[int, List[int]]):
    inst_list = [int(word, 0) for word in words]
    return (1, inst_list[0]) if len(inst_list) == 1 else (len(inst_list), inst_list)


def label_wrapper(labels: {str: int}) -> Callable:
    """
    :param labels: all labels { name: pc }
    :return: encoder func
    """

    def add_label(words: [str], pc: int) -> Tuple[int, List[int]]:
        label_key = words[0]
        if label_key in labels:
            raise KeyError(f"duplicated label: {label_key}")
        labels[label_key] = pc
        return 0, []

    return add_label


def record_wrapper(records: [Tuple[int, str, int, str, bool]]) -> Callable:
    """
    :param records: [(pc, op, tr, label_name, absolute_flag)]
    :return: encoder func
    """

    def add_record(words: [str], with_reg: bool, op_key: str, absolute_addr: bool, pc: int) -> Tuple[int, int]:
        if with_reg:
            records.append((pc, op_key, __str_to_reg(words[0], target_reg=True), words[1], absolute_addr))
        else:
            records.append((pc, op_key, 0, words[0], absolute_addr))
        log("(pc=%x) set relocate item", pc)
        return 1, 0

    return add_record


def make_inst_map(labels: {str: int}, records: [Tuple[int, str, int, str, bool]])->{str: Tuple[Callable, bool, List]}:
    """
    [ op : [coder, op_code]
    [ pseudo : [coder, with_tr, op_key, is_abs_addr]
    :param labels: all labels { name: pc }
    :param records: [(pc, op, tr, label_name, absolute_flag)]
    :return: instruction set assembler
    """

    """
    lea <Tr> <Ar>           load data from memory (address hold by Address Register) to Temporary Register
    mov <Tr> <imme>         move immediate value to Temporary Register
    st <Dr> <Ar>            store data from Data Register to memory (address hold by Address Register)
    add <Tr> <imme>         add immediate value to Temporary Register
    cmpi <Tr>, <imme>       compare Temporary Register with immediate value, store result in Flag Register
    bnz <imme>              relative branch to address if Flag Register is non-zero
    nop                     no operation
    halt                    halt the cpu
    data <imme_byte>...     define data
    label <name>            define label
    bnzl <label>            label version of bnz
    movl <Tr> <label>       label version of mov
    """
    inst_map = {
        'nop': (encode_no_op, False, [0]),
        'lea': (encode_reg_reg, False, [1]),
        'mov': (encode_reg_imme, False, [2]),
        'st': (encode_reg_reg, False, [3]),
        'add': (encode_reg_imme, False, [4]),
        'cmpi': (encode_reg_imme, False, [5]),
        'bnz': (encode_imme, False, [6]),
        'halt': (encode_no_op, False, [7]),
        'data': (prepare_mem_data, False, []),
        'label': (label_wrapper(labels), True, []),
        'bnzl': (record_wrapper(records), True, [False, 'bnz', False]),
        'movl': (record_wrapper(records), True, [True, 'mov', True])
    }

    return inst_map


def relocate_label(record: Tuple[int, str, int, str, bool], label_addr: int, inst_map: {str: Tuple[Callable, bool, List[int]]}):
    """
    :param inst_map: op_key -> op_code
    :param record: (pc, op, tr, label_name, absolute_flag)
    :param label_addr:
    """
    pc, op, tr, label, is_abs_addr = record
    jump_addr = label_addr if is_abs_addr else label_addr - pc
    jump_addr *= 4
    _, _, info = inst_map[op]
    inst = _assemble_imme_inst(info[0], tr, jump_addr)
    return inst_to_int(inst)
