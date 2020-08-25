import re

a = "> <string>(1)<module>()"
b = re.compile(r"> <string>\((\d+)\)<module>\(([\w|\W]*)\)")

c = b.match(a)

d, f = c.groups()
print(d, f)

a = 'pid 17240\r\n'
b = re.compile(r"pid (\d+)\r\n")
c = b.match(a)
print(c.groups())