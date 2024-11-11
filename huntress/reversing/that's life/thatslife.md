# That's Life

Put on some lofi beats, run this game, stare at the terminal, and let life start to make sense. Don't think too hard about the solution, it's in there somewhere.

---

Though this challenge had a container, the container just provided a download for the executable 'gameoflife' and an upload to submit a "solving file" to get the flag

![that's life container]()

Running the program it asks you to zoom out to see the full program, so I used lxterminal instead of my usual urxvt since zoom is easier on that one. It seems the program is some modification of [conway's game of life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life) except with colours. Apparently there was also a small chance cells could randomly come back to life but I didn't notice this during the challenge.

![program running]()

While running, another file 'game_state.pb' was created and the file size would change continuously as it ran. Presumably it was being repeatedly regenerated.

![game state file]()

Opening gameoflife in IDA, we can thankfully still see the function names, and thereby easily separate out the library functions. However, since we have the game of life running, it seems the difficulty will partly be separating out the game logic from whatever actually determines the win condition.

![function names in ida]()

Speaking of, what actually is the win condition and what do they mean by "solving file"? Conway's game of life doesn't have a win state, which threw me a bit. The most likely thing is the game_state and there's something in the code that determines whether a given game_state is a winning state. Since I didn't have any better leads I went with this assumption and tried to find some logic that might confirm this.

Sure enough, in main_main we see a string that implies the existence of a winning state:

![Congratulations, you won! string in main_main]()

So how do we get this to execute? Well, you can see above this block there are 2 conditional jumps we care about:

```asm
cmp     rcx, rdx
jge     short loc_5642E7
```

and

```asm
test    sil, sil
jnz     loc_5643F7
```

So the winning game state will lead to (rcx >= rdx) && (sil != 0) after some logic sets these variables.

Since rcx is generally used as a counter in loops, we can assume that only sil will matter and the first condition will just be true at the end of some loop. You ran step through the code with breakpoints to confirm this is the case. I should also note that from running the code we find the loop is basically this for loop:

```js
for (let rcx = 0; rcx < 12; rxc++) {
  // some logic
}
```

So where is sil set? Clicking sil highlights all the other parts of the other instances where sil is mentioned in the disassembly of main_main, and it seems the only other locations it's set are here:

![esi is set to 1]()

and here:

![there's a block that contains xor esi, esi]()

xoring a number with itself just sets it to zero, so it seems we just need to work out how to avoid this block of code to keep it at the 1 value that it's set at before the repeating loop.

Let's summarise our understanding of the logic so far. We have have a loop that repeats 12 times and at the end of the loop, we have either achieved the win condition or we do some mystery stuff before going back to the loop again. Most likely this mystery stuff is just saving and loading the game state and then progressing to the next grid, but since it seems we don't need to care about this to reach the winning state, I ignore it for now.

My next focus is working out how to avoid that `xor esi, esi` code block.

I'm going to simplify the assembly for the checks a bit here because those runtime panics are clearly not something we care about:

```asm
mov     r8, rcx
shl     rcx, 5
mov     r9, cs:qword_7154B0
mov     r10, [r9+rcx]

lea     r10, [r10+r10*2]
mov     r12, [rcx+r9+8]
mov     r10, [rax+r10*8]

shl     r12, 4
movzx   r11d, byte ptr [r10+r12]
test    r11b, r11b                ; r11b should be non-zero
jz      short loc_564390

mov     r10, [r12+r10+8]
mov     r11, [r9+rcx+10h]
cmp     r11, r10
jnz     short loc_564390          ; r11 should be equal to r10
```

From setting breakpoints in the code, I realised pretty fast that in the second to last block, r12 didn't really change but r10 was set at runtime and differed between runs. I then proceeded to waste a bunch of time working out exactly how the runtime values were set instead of taking a moment to understand what they were. It turns out these were addresses for cells in the game of life! I worked this out when I realised that the dimensions of the struct were the same as the dimensions of the grid.

These cells are stored in an array of columns with the value in rax pointing to the start of the array. If you have the offset of the base offset then the amount added to that doesn't change between runs. So if you set a breakpoint at *0x56436F and calculate r10-rax, you can add that number back to rax to get the offset of the cell that's checked in any given run of the program.

![python interactive terminal to calculate the array offsets]()

We want to find out what the value is for each step in the loop, so we set that breakpoint and write down the values of r12 and r10-rax for all 12 steps of the loop.

So the next thing is to try setting the cells manually to see if it reaches the win condition.

I start by setting a break point in gdb at the start of the loop and grab the value in rax. I put this into a little python interactive terminal I've been using to do basic math and functions so I can get the offsets for r10. Since this is just a recreation it doesn't really show just how I was using the interactive terminal for all kinds of useful stuff:

![using python interactive terminal to work out variables]()



