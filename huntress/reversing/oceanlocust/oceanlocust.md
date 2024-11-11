# Ocean Locust

Wow-ee zow-ee!! Some advanced persistent threats have been doing some tricks with hiding payloads in image files!

We thought we would try our hand at it too.

**NOTE: this challenge includes a debug build of the binary used to craft the image, as well as a release build... so you may choose to go an easier route or a harder route ;)**

**Attachments: ocean_locust.7z**

---

This challenge immediately interested me because of the first line implying the involvement of some form of custom image steganography. Extracting the .7z file, you see the two .exes described as well as an image that presumably contains the flag encoded in some way.

![the files png-challenge-debug.exe, png-challenge.exe, and inconspicuous.png in a file manager](https://github.com/mythemeria/ctf-writeups/blob/main/images/included%20files.png?raw=true)

At first, I attempted to solve this by looking at it in a bunch of reverse engineering tools like Ghidra and IDA. Unfortunately, I had little success understanding… basically anything within either of the binaries due to my lack of experience reversing. I instead worked out how to run it so I could find the parts of the code responsible for
+ encoding the flag
+ inserting it into the image

By messing around with the .exe a bit, I was able to work out the arguments required from the error messages:

![image of a terminal executing the command to add the executable permission to png-challenge.exe and then trying to run it. it outputs error messages complaining about a missing image file path and flag](https://github.com/mythemeria/ctf-writeups/blob/main/images/working%20out%20args.png?raw=true)

It seems it takes an input image path and some text. It does some mystery stuff and outputs an image that seems similar and is named based on the name of the input image.

You’ll notice that I use an img.png for this, which is an image that is the same as the inconspicuous.png image but plain white. I chose to do this because I didn’t want to introduce any extra variables that might make it harder to understand the output.

Now of course there has to be some kind of difference between the two images, and that difference would contain the encoded flag. So I did a diff:

![image of running the command diff -au between img.png and encoded img.png and piping the output to a file which is then viewed with the terminal hex editor xxd](https://github.com/mythemeria/ctf-writeups/blob/main/images/diff.png?raw=true)

Unfortunately, this wasn’t useful to me because I didn’t know enough about the PNG file structure to understand what it meant or how to narrow down the diff to what I cared about. I had little understanding of how the PNG file was structured, but as it’s a common file format there should be information online about it. So I tracked down the [PNG spec](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html) and got to reading. I recommend reading that before continuing because it’ll be necessary to understand the rest of this writeup.

It turns out that PNG data is separated into chunks, so I looked for [a tool](https://www.nayuki.io/page/png-file-chunk-inspector) that would allow me to visualise PNG chunk data. This would let me find the differences I care about a lot faster.

![The linked website open in two browser windows side by side, showing the difference between an example img.png and encoded img.png](https://github.com/mythemeria/ctf-writeups/blob/main/images/chunk%20comparison.png?raw=true)

Sure enough, this was very useful! The difference between the files on first glance is there seems to be 8 new chunks of the same size, with a strange chunk type label. I tossed the img.png and some other random images that were on my pc into the .exe a few more times and compared them. From looking at these, I was able to determine that 8 new chunks were introduced and the order of the 3rd to 2nd last chunks was randomised. The 8 new chunks were consistently named ‘biT{letter}’ for the letters a-h. The contents of the chunks was also consistent between files, so the chunk biTa (for example) would look the same across all files.

At this point I realised I might not need to look at any disassembly at all for this challenge, so I focused on trying to understand how the image encoding worked. From my interest in cryptography I knew there were a number of questions I needed to answer to understand the encoding process.

---

#### _Does it always output the same thing given the same input?_

Already knew this from before - the chunks are rearranged but their content is the same

---

#### _How many bytes change in the output when you change one byte of the input? This question is important because modern crypto reliably changes about half of the output based on any change in the input, this is important as it makes the effect of changes indistinguishable from randomness. If it’s modern crypto, I would likely need to find an AES key in the binary or something._

No! (confirmation I don't need to look at any more ASM)

---

#### _Are the biT{letter} chunks always present and in the same quantity?_

For the most part, yes, however there is some weirdness for some input text sizes which seems like it could be a bug. I chose to ignore the sizes where this was the case because I already know the size of the input.

---

#### _Which byte or bytes change in the output when you change a byte in the input?_

With a bit of testing you can work out that the bytes correspond in this way:

`./png-challenge.exe img.png 0123456789abcdefghijklmnopqrstuvwxyzAB` <- same size as flag

```
biTa  52 58 66 52 56  0 1 2 3 4
biTb  57 5f 63 5a 5b  5 6 7 8 9
biTc  03 0b 37 07 07  a b c d e
biTd  04 0e 3c 0d 08  f g h i j
biTe  09 05 39 0b 0d  k l m n o
biTf  12 18 26 15 16  p q r s t
biTg  17 1f 23 1f 1b  u v w x y
biTh  18 28 16 c2 c8  z A B - -
```
---

#### _Do letters always encode to the same thing regardless of position?_

No. this means it’s not a simple substitution cipher.

---

At this point, we have enough information to break this cipher. If it were a simple substitution cipher, we could just work out which input byte corresponds to each output byte and reverse the substitution on the flag data. Since it’s not a simple substitution cipher, it’s a bit more annoying because we also need to consider position of the byte.

Luckily working out what input byte corresponds to what output byte for every position is computationally trivial, espectially since the flag is limited to certain characters. All we need to do is encode all the possible characters in all positions and see when the byte matches the one in the flag:

```python
def encode_data(data):
  os.system(f"./png-challenge.exe img.png {data}")
  # note this orders the chunks biTa-biTh
  chunks = read_png_chunks('encoded img.png')
  res = b''
  for chunk in chunks:
	res += chunk['data']
  return res

flag = ['?' for _ in range(40)]
lookup = {}
for c in 'abcdefgl{}0123456789':
  enc = encode_data(c * 40)
 
  res = ''
  for i in range(40):
	if enc[i] == flagdata[i]:
  	flag[i] = c
    
  print(''.join(flag)[:38])
```
