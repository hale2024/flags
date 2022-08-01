.global _start
.intel_syntax noprefix
_start:
mov al, 0x5a
push 0x41
push rsp
pop rdi
jmp continue
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
continue:
mov esi, 0x1ff
syscall
