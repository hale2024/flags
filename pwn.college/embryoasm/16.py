from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = """
mov rax, [rsp]
add rax, [rsp+8]
add rax, [rsp+16]
add rax, [rsp+24]
mov rcx, 4
div rcx
push rax
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
