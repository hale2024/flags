from pwn import *


# script.sh just contains the binary name
io = process(["bash", "script.sh"])

for i in range(0, 50):
    # try to receive the challenge prompt
    io.recvuntil(b"send the solution for: ")

    # receive the expression
    out = io.recv().decode()
    print(out)
    # evaluate/calculate
    res = eval(out)
    # convert to string
    send = f"{str(res)}\n"
    # send the encoded string
    io.send( send.encode() )

io.interactive()
