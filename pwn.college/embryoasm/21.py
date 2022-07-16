from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = """
cmp rdi, 0
je rdi_zero
jmp count

count:
    mov rsi, [rdi]
    cmp rsi, 0
    je end
    inc rax
    inc rdi
    jmp count

rdi_zero:
    xor rax, rax

end:
    nop
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
