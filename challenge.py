#!/usr/bin/env python
import re
from collections import deque

# memory, registers, stack, terminal
m, rs, s, t = {}, [0] * 8, deque(), deque()


def r(a):
    if a < 32768:
        return a
    else:
        return rs[a-32768]


# def w(a, b):
#     if a < 32768:
#         m[a] = b
#     else:
#         rs[a-32768] = b

i = 0
with open("challenge.bin", "rb") as file:
    while b := file.read(2):
        m[i] = int.from_bytes(b, byteorder='little', signed=False)
        # if m[i] < 255:
        # print(chr(m[i]), end="")
        i += 1
# quit()
# d = {}
# with open("arch-spec") as file:
#     for line in file.readlines():
#         if match := re.findall(r"^(\w+): (\d+) ?(.*)", line.strip()):
#             optcode, number, abc = match[0]
#             d[int(number)] = (optcode, len(abc.split()))
# for i, x in enumerate((9, 32768, 32769, 4, 19, 32768)):
#     m[i] = x
# debug = False
i = 0
while i in m:
    # if debug:
    #     optcode, params = d[m[i]]
    #     print(rs, f"[{i}] {optcode:4}", end=" ")
    #     for j in range(params):
    #         print(f"{m[i+j+1]:5}", end=" ")
    #     print()
        # print(f"[{i}] opcode: {m[i]}, rs:", rs)
    if m[i] == 0:  # halt: 0
        break
    elif m[i] == 1:  # set: 1 a b
        rs[m[i+1]-32768] = r(m[i+2])
        i += 3
    elif m[i] == 2:  # push: 2 a
        s.append(r(m[i+1]))
        i += 2
    elif m[i] == 3:  # pop: 3 a
        rs[m[i+1]-32768] = s.pop()
        i += 2
    elif m[i] == 4:  # eq: 4 a b c
        rs[m[i+1]-32768] = 1 if r(m[i+2]) == r(m[i+3]) else 0
        i += 4
    elif m[i] == 5:  # gt: 5 a b c
        rs[m[i+1]-32768] = 1 if r(m[i+2]) > r(m[i+3]) else 0
        i += 4
    elif m[i] == 6:  # jmp: 6 a
        i = r(m[i+1])
    elif m[i] == 7:  # jt: 7 a b
        i = r(m[i+2]) if r(m[i+1]) != 0 else i + 3
    elif m[i] == 8:  # jf: 8 a b
        i = r(m[i+2]) if r(m[i+1]) == 0 else i + 3
    elif m[i] == 9:  # add: 9 a b c
        rs[m[i+1]-32768] = (r(m[i + 2]) + r(m[i + 3])) % 32768
        i += 4
    elif m[i] == 10:  # mult: 10 a b c
        rs[m[i+1]-32768] = (r(m[i + 2]) * r(m[i + 3])) % 32768
        i += 4
    elif m[i] == 11:  # mod: 11 a b c
        rs[m[i+1]-32768] = r(m[i + 2]) % r(m[i + 3])
        i += 4
    elif m[i] == 12:  # and: 12 a b c
        rs[m[i+1]-32768] = r(m[i + 2]) & r(m[i + 3])
        i += 4
    elif m[i] == 13:  # or: 13 a b c
        rs[m[i+1]-32768] = r(m[i + 2]) | r(m[i + 3])
        i += 4
    elif m[i] == 14:  # not: 14 a b
        rs[m[i+1]-32768] = (~r(m[i + 2]) & 32767)
        i += 3
    elif m[i] == 15:  # rmem: 15 a b
        rs[m[i+1]-32768] = m[r(m[i + 2])]
        i += 3
    elif m[i] == 16:  # wmem: 16 a b
        m[r(m[i + 1])] = r(m[i + 2])
        i += 3
    elif m[i] == 17:  # call: 17 a
        s.append(i + 2)
        i = r(m[i+1])
    elif m[i] == 18:  # ret: 18
        if s:
            i = s.pop()
        else:
            break
    elif m[i] == 19:  # out: 19 a
        print(chr(r(m[i + 1])), end="")
        i += 2
    elif m[i] == 20:  # in: 20 a
        if not t:
            t.extend(input("$ ") + "\n")
        rs[m[i+1]-32768] = ord(t.popleft())
        i += 2
    elif m[i] == 21:  # noop: 21
        i += 1
    else:
        print(f"TODO i: {i}, op: {m[i]}, a: {m[i+1]}")
        break

if i not in m:
    print(f"END [{i-1}] opcode: {m[i-1]}, rs:", rs)
