
;;; initialization
mov 1 0                       ; init counter as 0, reg#1 is used to compare iteration times
movl 2 ascii_addr             ; init input pointer, reg#2 is used to read data from memory[reg#2]
movl 3 output_addr            ; init output pointer, reg#3 is used to write data to memory[reg#3]


;;; do-while loop
label loop                    ; iterate 11 times

lea 4 2                       ; load data from memory[reg#2] to reg#4
st 4 3                        ; save data from reg#4 to memory[reg#3]

add 2 4                       ; input pointer + 1, by reg#2 + 4
add 3 4                       ; output pointer + 1, by reg#3 + 4

add 1 1                       ; counter + 1
cmpi 1 11                     ; compare reg#1 > 11
bnzl loop                     ; jump to label [loop] or move out

;;; stop
halt

label ascii_addr
data 0x48 0x65 0x6C 0x6C 0x6F ; ascii code for [Hello]
data 0x20                     ; ascii code for space
data 0x57 0x6F 0x72 0x6C 0x64 ; ascii code for [World]

label output_addr
