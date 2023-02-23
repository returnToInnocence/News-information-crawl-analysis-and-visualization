import uuid
a = uuid.uuid1().int >> 64
print(int(a) / 8)