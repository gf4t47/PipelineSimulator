def inst_to_int(inst: bytearray) -> int:
    return int.from_bytes(inst, 'little', signed=False)


def inst_to_bytes(inst: int) -> bytes:
    return inst.to_bytes(4, 'little', signed=False)


def imme_to_bytes(imme: int)->bytes:
    return imme.to_bytes(2, 'little', signed=True)


def imme_to_int(imme: bytearray) -> int:
    return int.from_bytes(imme, 'little', signed=True)
