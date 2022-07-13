from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
nop = 'nop\n'
assembly = f"""
jmp my_label
{nop*0x51}
my_label:
    pop rdi
    mov rsi, 0x403000
    jmp rsi
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
