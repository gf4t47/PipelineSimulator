from src.os.os import process


def test_simulator():
    executable_file = '../data/test.bin'
    process(executable_file)


test_simulator()
