from src.os.os import process


def execute(executable_file: str)->bytearray:
    return process(executable_file)
