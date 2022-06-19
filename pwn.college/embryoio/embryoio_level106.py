from pwn import *


bin_name = "/challenge/embryoio_level106"
io = process(bin_name, stdin=open("myfifo", "rb"), stdout=open("another", "wb"));
io.interactive()
