# GoCrackMe1

TENNNNNN-HUT!

Welcome to the Go Dojo, gophers in training!

Go malware is on the rise. So we need you to sharpen up those Go reverse engineering skills. We've written three simple CrackMe programs in Go to turn you into Go-binary reverse engineering ninjas!

First up is the easiest of the three. Go get em!

**Attachments: GoCrackMe1.zip**

---

I'm a bit of a noob with RE but eager to learn since crypto stuff so often hides behind it. This was the first time I had tried to reverse a go binary and I spent a long time just trying to find the resources I needed to learn the basics. So instead of going over all the ways I dawdled around not knowing what to do, it's probably more interesting to start by summarising the things I learnt from this challenge (and later gocrackmes) since that's probably more useful to anyone reading this.

#### There are a lot of reversing tools

Unlike other software where they mostly do the same thing so most people will just pick one tool or another, I found I needed to use a number of RE tools because each one had areas they excelled at. IDA's graph mode was super useful for visualising program flow without having to get into the weeds of the assembly. I preferred Ghidra's interface for finding strings and it largely had better tooling for renaming variables in decompiled code to make it easier to understand. GDB is great for seeing what's in registers and memory. Binja seems to have more readable decompilation and has a graph view of decompiled code (as opposed to IDA where the graph is disassembly)

#### Difficulty mostly comes from knowing where to look

There's a LOOOOOOOT of functions in a binary, most of them being low-level library functions that you wouldn't see in the source code. You don't care about this for the most part, but understanding it is helpful for harder challenges. The hard part about reversing go is that it just includes all the library functions and if you strip it, it's much harder to tell which distinguish these from the functions you care about.

#### Your main tools for reversing are breakpoints and patching.

Setting breakpoints will let you stop the execution at a specific point and look at the memory and registers at that exact instruction. You can also step forward by an instruction at a time. I found the latter thing especially useful for getting familiar with the assembly.

Patching the binary is helpful to modify the program flow. If there's some kind of logic check that stops you from reaching a part of the code you want to get to, it effectively doesn't exist if you can patch the binary. Unlike source code, you need to care about the size of your modification and keep changes to something that takes up the same number of bytes.

#### You do actually need to learn assembly

It just makes it far easier to spot what you're looking for if you actually know what the instructions are doing. Though I went in with some basic knowledge of assembly, that was not enough. I didn't know how strings were typically handled, and as a result, I could not spot the points in the disassembly that handled the flag string. I highly recommend the book [Practical Reverse Engineering](https://www.amazon.com.au/Practical-Reverse-Engineering-Reversing-Obfuscation/dp/1118787315) to learn assembly. I also found [this x86 reference](https://ref.x86asm.net/geek32.html) super useful for looking up instructions I didn't know.

---

### Now that's out of the way, let's get onto how we can use what we've learnt to solve gocrackme1.

First things first, we run the code to see what it does.

![running the program in the terminal](https://github.com/mythemeria/ctf-writeups/blob/main/huntress/images/running%20gcm1.png?raw=true)

To get an overview of the program, we first open it up in IDA. Looking at the function list on the left, is seems the binary is not stripped as we can still see all the function names.

![list of unstripped function names in a IDA](https://github.com/mythemeria/ctf-writeups/blob/main/huntress/images/function%20names.png?raw=true)

There's some guides online that will tell you that the user code main function in a go binary is main_main, so we go straight there:

![the view when we go to the main_main function](https://github.com/mythemeria/ctf-writeups/blob/main/huntress/images/main_main.png?raw=true)

Now, just reading through the assembly is quite slow and tedious, so instead we look for important things. You'll notice that at the bottom there's an "Access denied!" string, so presumably this part of the code gets executed as part of how it printed that line earlier.

![zoom in on ida graph where the access denied string is](https://github.com/mythemeria/ctf-writeups/blob/main/huntress/images/access%20denied.png?raw=true)

The program flow shows that there's some check that determines whether this path executes (.text:00000000004836CF jz short loc_483719), so what happens if we patch the binary to make the jump do the opposite? Looking up on the x86 reference, the opposite instruction to jz is jnz

To patch, we go to Edit -> patch program -> assemble

![patching bytes to replace jz with jnz](https://github.com/mythemeria/ctf-writeups/blob/main/huntress/images/jnz%20patch.png?raw=true)

The binary won't actually be changed without applying the patch, so go to Edit -> patch program -> apply patches to input file and click ok

Running the program, we see this:

![omg it's the flag](https://github.com/mythemeria/ctf-writeups/blob/main/huntress/images/gcm1%20flag.png?raw=true)