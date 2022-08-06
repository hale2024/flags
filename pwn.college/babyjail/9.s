.global _start
.intel_syntax noprefix
_start:
# chmod("A", 0777)
lea ebx, [eip+flag]
mov ecx, 0x1ff
mov eax, 15
int 0x80

# exit(0)
xor ebx, ebx
mov eax, 1
int 0x80

flag:
    .byte 0x41
