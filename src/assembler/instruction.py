from typing import Tuple, List, Callable

from src.util.log import log


def _to_imme(word: str) -> int:
    """
    convert word in assemble to immediate value
    :param word: input string
    :return: immediate value
    """
    imme = int(word, 0)
    if imme < -0x7fff or imme > 0x7fff:
        raise ValueError(f"bad imme {word}")
    return imme


def _to_reg(word: str, target_reg: bool) -> int:
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


def _to_int(inst: bytearray) -> int:
    return int.from_bytes(inst, 'little', signed=False)


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
    log(f"{op}, {tr}, {sr1}, {sr2} -> {_to_int(inst)}")
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
    inst[2: 4] = imme.to_bytes(2, 'little')
    log("%d, %d, %d -> %x", op, tr, imme, _to_int(inst))
    return inst


# noinspection PyUnusedLocal
def encode_no_op(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, _to_int(_assemble_reg_inst(op_code, 0, 0, 0))


def encode_reg_imme(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, _to_int(_assemble_imme_inst(op_code, _to_reg(words[0], target_reg=True), _to_imme(words[1])))


def encode_reg_reg(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, _to_int(_assemble_reg_inst(op_code, _to_reg(words[0], target_reg=True), _to_reg(words[1], target_reg=False), 0))


def encode_reg(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, _to_int(_assemble_reg_inst(op_code, _to_reg(words[0], target_reg=True), 0, 0))


def encode_imme(words: [str], op_code: int) -> Tuple[int, int]:
    return 1, _to_int(_assemble_imme_inst(op_code, 0, _to_imme(words[0])))


def prepare_mem_data(words: [str]) -> Tuple[int, List[int]]:
    return len(words), [int(word, 0) for word in words]


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
            records.append((pc, op_key, _to_reg(words[0], target_reg=True), words[1], absolute_addr))
        else:
            records.append((pc, op_key, 0, words[0], absolute_addr))
        log("(pc=%x) set relocate item", pc)
        return 1, 0

    return add_record


def inst_set_wrapper(labels: {str: int}, records: [Tuple[int, str, int, str, bool]]):
    """
    [ op : [coder, op_code]
    [ pseudo : [coder, with_tr, op_key, is_abs_addr]
    :param labels: all labels { name: pc }
    :param records: [(pc, op, tr, label_name, absolute_flag)]
    :return: instruction set assembler
    """

    """
    ld <Tr> <Ar>            #load
    movi <Tr> <imme>        #move imme
    st <Dr> <Ar>            #store data to address
    inc <Tr>                #Tr+1
    cmpi <Tr>, <immu>       #compare with imme
    bnz <immu>              #relative branch to address
    nop                     #no operation
    halt                    #halt the cpu
    data <imme_byte>...     #data definition
    ldl <Tr> <label>        #label version of ld
    label <name>            #define label
    bnzl <label>            #label version of bnz
    movil <Tr> <label>      #label version of movi
    """
    inst_set = {
        'nop': (encode_no_op, [0]),
        'ld': (encode_reg_reg, [1]),
        'movi': (encode_reg_imme, [2]),
        'st': (encode_reg_reg, [3]),
        'inc': (encode_reg, [4]),
        'cmpi': (encode_reg_imme, [5]),
        'bnz': (encode_imme, [6]),
        'halt': (encode_no_op, [7]),
        'data': (prepare_mem_data, []),
        'label': (label_wrapper(labels), []),
        'bnzl': (record_wrapper(records), [False, 'bnz', False]),
        'movil': (record_wrapper(records), [True, 'movi', True])
    }

    return inst_set


def relocate_label(record: Tuple[int, str, int, str, bool], label_addr: int, inst_set: {str: Tuple[Callable, List[int]]}):
    """
    :param inst_set: op_key -> op_code
    :param record: (pc, op, tr, label_name, absolute_flag)
    :param label_addr:
    """
    pc, op, tr, label, is_abs_addr = record
    jump_addr = label_addr if is_abs_addr else label_addr - pc
    jump_addr *= 4
    inst = _assemble_inst(inst_set[op][1][0], tr)
    inst[2:4] = jump_addr.to_bytes(2, 'little', signed=True)
    return _to_int(inst)