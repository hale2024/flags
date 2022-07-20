from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = """
//   most_common_byte(src_addr, size):
//       b = 0
//       i = 0
//       for i <= size-1:
//           curr_byte = [src_addr + i]
//           [stack_base - curr_byte] += 1
//       b = 0
//
//       max_freq = 0
//       max_freq_byte = 0
//       for b <= 0xff:
//           if [stack_base - b] > max_freq:
//               max_freq = [stack_base - b]
//               max_freq_byte = b
//
//       return max_freq_byte


// rdi = src_addr
// rsi = size


push rbp
mov rbp, rsp


// i
mov rcx, 0
// curr_byte
mov rax, 0
jmp first_for

first_for:
    // if i < size
    cmp rcx, rsi
    jge second_part

    xor rdx, rdx
    mov rdx, rdi
    // rdx = src_addr + i
    add edx, ecx

    // curr_byte = [src_addr+i]
    xor rax, rax
    mov al, byte ptr [rdx]

    // [stack_base - curr_byte] += 1
    mov rdx, rbp
    sub rdx, rax
    mov r12b, byte ptr [rdx]
    inc r12b
    mov byte ptr [rdx], r12b

    // i++
    inc rcx

    jmp first_for

second_part:
    // b
    mov rbx, 0
    // max_freq
    mov rcx, 0
    // max_freq_byte
    mov rax, 0
    jmp second_for

second_for:
    // if b <= 0xff
    cmp ebx, 0xff
    jg end

    mov rdx, 0
    mov rdx, rbp
    // rdx = stack_base - b
    sub rdx, rbx
    // if [stack_base - b] > max_freq
    cmp byte ptr [rdx], cl
    jle second_for
    // max_freq = [stack_base - b]
    mov cl, byte ptr [rdx]
    // max_freq_byte = b
    mov eax, ebx

    // b++
    inc rbx

    jmp second_for

end:
    mov rsp, rbp
    pop rbp
    ret
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
