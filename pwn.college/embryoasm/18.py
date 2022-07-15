from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = """
// x = rdi, y = rax

// if [x] is 0x7f454c46
cmp dword ptr [rdi], 0x7f454c46
jne else_if
jmp if

if:
    xor rax, rax
    add eax, dword ptr [rdi+4]
    add eax, dword ptr [rdi+8]
    add eax, dword ptr [rdi+12]
    jmp exit
else_if:
    cmp dword ptr [rdi], 0x00005A4D
    jne else
    mov eax, dword ptr [rdi+4]
    sub eax, dword ptr [rdi+8]
    sub eax, dword ptr [rdi+12]
    jmp exit
else:
    mov rax, 1
    mul dword ptr [rdi+4]
    mul dword ptr [rdi+8]
    mul dword ptr [rdi+12]
    jmp exit

exit:
    nop
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
