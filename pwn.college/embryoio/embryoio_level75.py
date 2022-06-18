from pwn import *

io = pwnlib.tubes.process.process(argv=list(), executable="/challenge/embryoio_level75");

io.interactive();
