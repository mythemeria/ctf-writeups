# Bit-O-Asm-4

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
<+22>:    cmp    DWORD PTR [rbp-0x4],0x2710
<+29>:    jle    0x55555555514e <main+37>
<+31>:    sub    DWORD PTR [rbp-0x4],0x65
<+35>:    jmp    0x555555555152 <main+41>
<+37>:    add    DWORD PTR [rbp-0x4],0x65
<+41>:    mov    eax,DWORD PTR [rbp-0x4]
<+44>:    pop    rbp
<+45>:    ret
```

This bit of asm includes jump statements, so we can't just use our previous technique or following the code backwards. Looking at the two jumps, it seems the code flow differs based on the outcome of the comparison at +22. It seems there are two code paths, one subtracts 0x65 from the value pointed to by `rbp-0x4`, the other performs addition instead. This value is written to eax at +41, so we need to work out both what the value was previously, and what code path is taken.

The initial value of 0x9fe1a is set at +15. The comparison checks if this value is less than or equal to 0x2710 and if true, it performs addition, otherwise it performs subtraction. Since 0x9fe1a < 0x2710, we subtract 0x65 from 0x9fe1a to get the value in eax (654773).