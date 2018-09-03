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
ld <Tr> <Ar>       # load data from memory (address hold by Address Register) to Temporary Register
movi <Tr> <imme>   # move immediate value to Temporary Register
st <Dr> <Ar>       # store data from Data Register to memory (address hold by Address Register)
inc <Tr>           # Temporary Register += 1
cmpi <Tr> <imme>   # compare Temporary Register with immediate value, store result in Flag  Register
bnz <imme>         # relative branch to address if Flag Register is non-zero
nop                # no operation
halt               # halt the cpu
```
### pseudo code
```
data <imme_byte>...     # define data
label <name>            # define label
bnzl <label>            # label version of bnz
movil <label>           # label version of movi
```
### instruction encoding
```
bytes[0] operation code:

|value  |operation|
|:------|:--------|
| 0     | nop
| 1     | ld
| 2     | movi
| 3     | st
| 4     | inc
| 5     | cmpi
| 6     | bnz
| 7     | halt

bytes[1] output register
bytes[2] input register 1
bytes[3] input register 2
bytes[2,3] immediate value
```
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
