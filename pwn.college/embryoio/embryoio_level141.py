from pwn import *

io = remote("localhost", 1065)

for i in range(0, 5):
    # try to receive the challenge prompt
    io.recvuntil(b"send the solution for: ")

    # receive the expression
    out = io.recv().decode()
    # evaluate/calculate
    res = eval(out)
    # convert to string
    send = f"{str(res)}\n"
    # send the encoded string
    io.send( send.encode() )

print( io.recvall().decode() )
