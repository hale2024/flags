from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

"""
sum = 0
i = 1
for i <= n:
    sum += i
    i += 1
"""

"""
rdi = 1st qword
rsi = n
rax = sum
rbx = i
"""

"""
0000000000001119 <main>:
    1119:	55                   	push   rbp
    111a:	48 89 e5             	mov    rbp,rsp
    111d:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
    1124:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
    112b:	c7 45 fc 0a 00 00 00 	mov    DWORD PTR [rbp-0x4],0xa
    1132:	eb 0a                	jmp    113e <main+0x25>
    1134:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1137:	01 45 f4             	add    DWORD PTR [rbp-0xc],eax
    113a:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
    113e:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1141:	3b 45 fc             	cmp    eax,DWORD PTR [rbp-0x4]
    1144:	7e ee                	jle    1134 <main+0x1b>
    1146:	b8 00 00 00 00       	mov    eax,0x0
    114b:	5d                   	pop    rbp
    114c:	c3                   	ret
"""

# assembly goes here, most of the rest is boilerplate
assembly = """
xor rax, rax
xor r12, r12

loop:
    cmp r12, rsi
    jge end
    mov ebx, dword ptr [rdi]
    add rax, rbx
    add rdi, 4
    inc r12
    jmp loop

end:
    div rsi
"""

# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )
