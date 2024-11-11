# Bit-O-Asm-3

Can you figure out what is in the `eax` register? Put your answer in the picoCTF flag format: `picoCTF{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `picoCTF{17}`.

---

The assembly dump contains the following:

```asm
<+0>:     endbr64 
<+4>:     push   rbp
<+5>:     mov    rbp,rsp
<+8>:     mov    DWORD PTR [rbp-0x14],edi
<+11>:    mov    QWORD PTR [rbp-0x20],rsi
<+15>:    mov    DWORD PTR [rbp-0xc],0x9fe1a
<+22>:    mov    DWORD PTR [rbp-0x8],0x4
<+29>:    mov    eax,DWORD PTR [rbp-0xc]
<+32>:    imul   eax,DWORD PTR [rbp-0x8]
<+36>:    add    eax,0x1f5
<+41>:    mov    DWORD PTR [rbp-0x4],eax
<+44>:    mov    eax,DWORD PTR [rbp-0x4]
<+47>:    pop    rbp
<+48>:    ret
```

This one requires a fair number more steps than the last one, so let's break it down.

The last time eax is written to is at +44, but if you look at the previous 2 instructions, you'll notice it's pretty much just copying eax to eax. So we'll ignore everything after +36.

+32 and +36 both show operations on some value that was already in eax, so we look to where it was written to before this, which was at +29. The value pointed to by `rbp-0xc` is the initial value in eax, which is 0x9fe1a (from +15).

Now we have that initial value, we do the multiplication with the value pointed to by `rbp-0x8` (0x4 from +22) and add 0x1f5. The final value in eax is 2619997.