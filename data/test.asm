; test assemble file for simple cpu

nop
mov 1 0
movl 2 data_addr ; move data_addr value to reg 2
movl 3 io_addr
lea 3 3

label loop
nop
lea 4 2
st 4 3
add 2 1
add 1 1
cmpi 1 10
nop
bnzl loop

nop
halt

label data_addr
; data 0x30 0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3a 0x3b
data 0x30313233 0x34353637 0x38393a3b
data 9 0x12345678 0x12 0x33
data 1

label io_addr
data 4095
