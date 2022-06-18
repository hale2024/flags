from pwn import *


challenge_binary = "/challenge/embryoio_level55";

cat = process(["/usr/bin/grep", "pwn"]);
io = process(challenge_binary, stdout=cat.stdin);

print(cat.interactive());
