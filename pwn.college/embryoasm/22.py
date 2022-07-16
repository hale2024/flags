from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = """
xor rax, rax

// if src_addr != 0
cmp rdi, 0
je end
jmp while_loop

while_loop:
    // if [src_addr] != 0
    cmp byte ptr [rdi], 0
    je end

    // if [src_addr] <= 90
    cmp byte ptr [rdi], 90
    jg incr_src_addr

    // save rdi in r12, and do rdi = [rdi]
    mov r12, rdi
    mov rdx, [rdi]
    mov rdi, rdx

    // save rax
    mov r8, rax

    // call foo([rdi])
    mov r10, 0x403000
    call r10
    // now return value will be in rax

    // restore rdi
    mov rdi, r12

    // [src_addr] = foo([src_addr])
    mov byte ptr [rdi], al

    // restore rax
    mov rax, r8

    // rax += 1
    inc rax
    // end-if
    jmp incr_src_addr

    jmp while_loop

incr_src_addr:
    inc rdi
    jmp while_loop

end:
    ret
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
