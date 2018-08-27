from src.os.operating_system import execute


def test_simulator():
    executable_file = '../data/test.bin'
    execute(executable_file)


test_simulator()
