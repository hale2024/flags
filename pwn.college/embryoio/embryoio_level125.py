from pwn import *


# script.sh just contains the binary name
io = process(["bash", "script.sh"])

while True:
    # try to receive the challenge prompt
    try:
        io.recvuntil(b"send the solution for: ")
    except:
        # if we get an exception then we probably have
        # no more challenges to solve.
        # In that case, just print the output since it 
        # should contain the flag
        print(io.recv().decode())

    # receive the expression
    out = io.recv().decode()
    print(out)
    # evaluate/calculate
    res = eval(out)
    # convert to string
    send = f"{str(res)}\n"
    # send the encoded string
    io.send( send.encode() )
