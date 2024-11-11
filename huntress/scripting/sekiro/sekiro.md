# Sekiro

お前はもう死んでいる

---

Connecting to the challenge server, we see this:

![screenshot](https://github.com/mythemeria/ctf-writeups/blob/main/images/11112024-123709.png?raw=true)

It seems the server is running a terminal game inspired by the game Sekiro and rock-paper-scissors. You need to respond to the opponent's attacks in time, however it seems you need to type at inhuman speeds to do so. I may not be able to type this fast, but I can easily write a python script to do it for me. I messed around with it a bit so I could work out the correct response to each message and ended up with this:

```python
import pwn

host = 'challenge.ctf.games'
port = 30795

lookup = {'strike': 'block', 'advance': 'retreat', 'block': 'advance', 'retreat': 'strike'}

r = pwn.remote(host, port)

def parse_opponent_move(data):
  if 'Opponent move: ' in data:
    start_index = data.find('Opponent move: ') + len('Opponent move: ')
    end_index = data.find('\n', start_index)
    opponent_move = data[start_index:end_index]
    return opponent_move
  return None

while True:
  try:
    data = r.recv().decode('utf-8').strip()
  except Exception as e:
    break
  
  # dont bother if it's the little spinning wheel thing
  if len(data) <= 20:
    continue
  print(data)

  # gaming
  if 'Opponent' in data:
    opponent_move = parse_opponent_move(data)
    my_move = lookup[opponent_move]
    r.sendline(my_move.encode('utf-8'))
    print(my_move)
```

Eventually, it prints the flag. Yes, this is a little hacky but it works.