## Description
You will implement a CPU simulator to run a binary executable file and return the memory state as byte array after the execution.
```python
def execute(executable_file: str)->bytearray:
    """
    execute the binary executable file
    :param executable_file: file path
    :return: memory after the execution
    """
    pass
```
You can use the [assembler.py](./src/assembler/assembler.py) provided to generate binary file from assembling. The assemble language in this project is an abridgment based on YASM, see more detail in [Specification](##Specification)
## Example
There is a [sample](./sample/) directory including both [assemble file](./sample/hello_world.asm) and [binary file](./sample/hello_world.bin), with an [unit test](./sample/sample_test.py) to show what is the expectation for your implementation.
## Specification
### register files
word wide: 32bit, little endian
```
r0=0
r1-r12
r13-pc
r14-lr-link register
r15-st-cpu state: bit0-zero bit1-bigger than
```
### instruction set
```
lea <Tr> <Ar>      # load data from memory (address hold by Address Register) to Temporary Register
mov <Tr> <imme>    # move immediate value to Temporary Register
st <Dr> <Ar>       # store data from Data Register to memory (address hold by Address Register)
add <Tr> <imme>    # Add immediate value to Temporary Register
cmpi <Tr> <imme>   # compare Temporary Register larger than immediate value, store result in Flag Register
bnz <imme>         # relative branch to address if Flag Register is non-zero
nop                # no operation
halt               # halt the cpu
```
### pseudo code
```
data <imme>...          # define data (could be multiple data in one line)
label <name>            # define label
bnzl <label>            # label version of bnz, labeled address as immediate value
movl <label>            # label version of mov, labeled address as immediate value
```
### instruction encoding
```
bytes[0] operation code
bytes[1] output register
bytes[2] input register 1
bytes[3] input register 2
bytes[2,3] immediate value
```
#### operation encoding:
|bytes[0]|operation|
|:-------|:-------|
| 0      | nop     |
| 1      | lea     |
| 2      | mov     |
| 3      | st      |
| 4      | add     |
| 5      | cmpi    |
| 6      | bnz     |
| 7      | halt    |
### memory space
```
0-4095: memory
4096-8192: io space
    0: output
    4: input
others are invalid
```
### interrupt vector
```
0:       system reset
1024:    input port interrupt
```
