from pwn import *


challenge_binary = "/challenge/embryoio_level56";

sed = process(["/usr/bin/sed", "s/pwn/pwn/g"]);
io = process(challenge_binary, stdout=sed.stdin);

print(sed.interactive());
