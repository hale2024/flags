from pwn import *


challenge_binary = "/challenge/embryoio_level54";

cat = process("/usr/bin/cat");
io = process(challenge_binary, stdout=cat.stdin);

print(cat.interactive());
