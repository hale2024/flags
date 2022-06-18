from pwn import *


challenge_binary = "/challenge/embryoio_level57";

rev = process(["/usr/bin/rev"]);
io = process(challenge_binary, stdout=rev.stdin);

print(rev.interactive());
