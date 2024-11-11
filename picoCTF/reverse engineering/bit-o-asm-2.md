# Bit-O-Asm-2

Can you figure out what is in the `eax` register? Put your answer in the picoCTF flag format: `picoCTF{n}` where `n` is the contents of the `eax` register in the decimal number base. If the answer was `0x11` your flag would be `picoCTF{17}`.

---

The assembly dump contains the following:

```asm
<+0>:     endbr64 
<+4>:     push   rbp
<+5>:     mov    rbp,rsp
<+8>:     mov    DWORD PTR [rbp-0x14],edi
<+11>:    mov    QWORD PTR [rbp-0x20],rsi
<+15>:    mov    DWORD PTR [rbp-0x4],0x9fe1a
<+22>:    mov    eax,DWORD PTR [rbp-0x4]
<+25>:    pop    rbp
<+26>:    ret
```

The last time eax is written to is this line: `eax,DWORD PTR [rbp-0x4]`. This means whatever is at the address `rbp-0x4` before that line is what will be written to eax. The line before this one writes `0x9fe1a` to `rbp-0x4`, and converting that to decimal, we get 654874.
