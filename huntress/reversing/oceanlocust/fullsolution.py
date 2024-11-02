from Crypto.Util.number import bytes_to_long, long_to_bytes
import os

flagdata = b'\x04\x05\x35\x06\x19\x04\x0c\x37\x5a\x55\x01\x5f\x6d\x53\x00\x5a\x0c\x37\x5c\x06\x54\x5c\x36\x5d\x00\x00\x58\x64\x03\x07\x55\x0b\x36\x51\x57\x06\x59\x29\xc2\xc8'

# I got AI to write most of this part because I'm lazy and PNG is a well-known format
def read_png_chunks(file_path):
  chunks = ['' for _ in range(8)]

  with open(file_path, 'rb') as f:
    # Read the PNG signature (8 bytes)
    signature = f.read(8)
    if signature != b'\x89PNG\r\n\x1a\n':
      raise ValueError("Not a valid PNG file")

    while True:
      # Read the length of the chunk (4 bytes, big-endian)
      length_bytes = f.read(4)
      if len(length_bytes) == 0:
        break

      length = int.from_bytes(length_bytes, byteorder='big')
      chunk_type = f.read(4)
      data = f.read(length)
      crc = f.read(4)

      # Store the chunk in the list as a dictionary
      if chunk_type not in [b'IHDR', b'pHYs', b'IDAT', b'IEND']:
        # silly lil magic number that converts 'biTa' -> 0 / 'biTb' -> 1 etc
        chunks[(bytes_to_long(chunk_type) & 0x9d96ab9f) - 1] = {
          'length_bytes': length_bytes,
          'chunk_type': chunk_type,
          'data': data,
          'crc': crc
        }

  return chunks


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