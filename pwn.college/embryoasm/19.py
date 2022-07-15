from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = """
// default
cmp rdi, 3
jg default

// rax = rdi * 8
mov rax, rdi
mov rbx, 8
mul rbx

// rax = rsi + rdi * 8
add rax, rsi
jmp qword ptr [rax]

default:
    jmp qword ptr [rsi+32]

"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
