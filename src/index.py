# noinspection PyUnusedLocal
from src.os.os import process


def execute(executable_file: str)->bytearray:
    """
    execute the binary executable file
    :param executable_file: file path
    :return: memory after the execution
    """
    return process(executable_file)
