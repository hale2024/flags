import os
from pwn import *

fd2 = os.dup2(sys.stdin.fileno(), 74);
os.set_inheritable(fd2, True);

io = process("/challenge/embryoio_level107", stdin=os.fdopen(fd2), close_fds=False);

io.interactive();
