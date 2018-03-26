nop
jmp $+0x40
lea eax,[ebp-0x40C]
mov bl,[eax]
cmp bl,0x23
jne $+0x21
mov bl,[eax+0x1]
cmp bl,0x21
jne $+0x17
mov byte ptr [eax],0x20
mov byte ptr [eax+1],0x20
nop
nop
nop
push eax
call $-400
nop
nop
nop
jmp $+0xB
nop
nop
nop
nop
jmp $+0x3c
nop
nop
nop
nop
nop
nop
nop
nop
jmp $+0x49