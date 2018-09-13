
;;; initialization
mov 1 0                       ; init counter as 0, reg#1 is used to compare iteration times
movl 3 ascii_end              ; init output pointer, reg#3 is used to write data to memory[reg#3]
movl 2 ascii_end              ; init input pointer, reg#2 is used to read data from memory[reg#2]
add 2 -4                      ; input pointer - 1 since we initialized it from the tail of ascii memory


;;; do-while loop
label loop                    ; to iterate 11(len("Hello World")) times

nop                           ; affect nothing, just to show the meaning of a meaningless operation :)

lea 4 2                       ; load data from memory[reg#2] to reg#4
st 4 3                        ; save data from reg#4 to memory[reg#3]

add 2 -4                      ; input pointer - 1, by reg#2 - 4
add 3 4                       ; output pointer + 1, by reg#3 + 4

add 1 1                       ; counter + 1
cmpi 1 11                     ; compare reg#1 > 11, store comparison result into Flag Register
bnzl loop                     ; jump to label [loop] or move out according to Flag Register

;;; stop
halt

data 0x48 0x65 0x6C 0x6C 0x6F ; ascii code for [Hello]
data 0x20                     ; ascii code for space
data 0x57 0x6F 0x72 0x6C 0x64 ; ascii code for [World]

label ascii_end
