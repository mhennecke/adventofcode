import hashlib

key = 'ckczppom'

i = 0
while True:
    h = hashlib.md5((key + str(i)).encode())
    if h.hexdigest()[:6] == '000000':
        break
    i += 1

print(h.hexdigest())
print(i)
