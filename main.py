#!/usr/bin/env python3
import os
from collections import deque
import sys

if len(sys.argv) < 2:
    print("ERROR: No file specified")
    exit(1)
prog = sys.argv[1]

ip = 0
# prog = "5 6 + write 10 11 - write"
stack = deque()
str_stack = deque()
tok = {}

file = open(prog, 'r')
reader = file.read()

program = [word
    for line in reader.splitlines()
    if not line.lstrip().startswith('//')
    for word in line.split(None)
    if len(word) > 0]

# print(program)

for ip in range(len(program)):
    code = program[ip]
    # print(f"Main Stack: {stack}")
    # print(f"String Stack: {str_stack}")
    #print(dir(code))
    # print(f"{ip}: {program[ip]}")
    if code.isdigit():
        stack.append(code)
        ip += 1
        # print(stack)
    elif code == '+':
        a = stack.pop()
        b = stack.pop()
        stack.append(int(a) + int(b))
        ip += 1
        # print(stack)
    elif code == 'write':
        a = stack.pop()
        print(a)
        ip += 1
         #print(stack)
    elif code == '-':
        a = stack.pop()
        b = stack.pop()
        stack.append(int(a) - int(b))
        ip += 1
    elif code.startswith('"'):
        str_stack.append(program[ip]) 
        ip += 1
    elif code.endswith('"'):
        a = " ".join(str_stack)
            # a = str_stack.pop()
        stack.append(a)
        print("Stack reached here.")
        print(f"Main Stack: {stack}")
        ip += 1
    else:
        print(f"Unknown token `{program[ip]}` in pos {ip}")
        if program[ip].endswith('"'):
            print("FIXME: Maybe you forgot to pass it as a string?")
    ip += 1
