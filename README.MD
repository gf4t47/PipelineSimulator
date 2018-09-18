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
  * You are NOT building the assembly-to-binary compiler that is provided with the code in assembler.py.  You are only building the CPU simulator which executes on the binary file.
  * Please write this code as if you were writing it for work and you will be evaluated on the quality of CPU Simulator code. Feel free to provide comments or auxiliary documentation explaining your design choices and trade-offs. 
  * Please expect that your CPU Simulator code will be tested against a small set of test binaries, built from the same assembly instruction set, using the same assembler.
  
You can use the [assembler.py](./src/assembler/assembler.py) provided to generate binary file from from a string of assembly instructions. The assembly language in this project is an abridgment based on YASM, see more detail in [Specification](##Specification)
## Example
There is a [sample](./sample) directory including both [assemble file](./sample/hello_world.asm) and [binary file](./sample/hello_world.bin), with an [unit test](./sample/sample_test.py) to show what is the expectation for your implementation.
## Specification
### register files
```
r0=0                 # place holder for function call result, is NOT required in this project 
r1-r12               # register 1~12 are general purpose registers for your usage
r13-pc               # program counter 
r14-lr               # place holder for link register, is NOT required in this project
r15-st               # Flag Register (aka CPU state register), used to in CPU to decide branch instruction result
```
### instruction set
```
lea <Tr> <Ar>        # load data from memory (memory address hold by Address Register) to Temporary Register
mov <Tr> <imme>      # move immediate value to Temporary Register
st <Dr> <Ar>         # store data from Data Register to memory (memory address hold by Address Register)
add <Tr> <imme>      # Add immediate value to Temporary Register
cmpi <Tr> <imme>     # compare Temporary Register larger than immediate value, store result in Flag Register
bnz <imme>           # relative branch to address if Flag Register is non-zero
nop                  # no operation
halt                 # halt the cpu
```
### pseudo code
pseudo code is not real instruction to be executed in CPU, they are consumed by assembler, assembler will use them to generate real instructions in above instruction set. 
```
data <imme>...       # define data (could be multiple data in one line), could be use to define data in memory
label <name>         # define label, as a reference for followed pseudo code to relocate
bnzl <label>         # label version of bnz, resolve labeled address as immediate value
movl <label>         # label version of mov, resolve labeled address as immediate value
```
### instruction encoding
**word wide: 32bit, little endian**
```
bytes[0] operation code
bytes[1] output register
bytes[2] input register 1
bytes[3] input register 2
bytes[2,3] immediate value  # short wide: 16bit, little endian, signed
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
