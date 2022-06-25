#!/usr/bin/env pypy3
import os
from collections import deque
import sys

if len(sys.argv) < 2:
    print("ERROR: No file specified")
    exit(1)
prog = sys.argv[1]

# prog = "5 6 + write 10 11 - write"
stack = deque()
str_stack = deque()
lab_stack = deque()
tok = {}
lab = {}

file = open(prog, 'r')
reader = file.read()

tokens = ['write', '+', '-', '"']
# print(str(tokens))
program = [word
    for line in reader.splitlines()
    if not line.lstrip().startswith('#')
    for word in line.split(' ')
    if len(word) > 0]
# print(program)
for ip in range(len(program)):
    word = program[ip]
    if word.endswith(':'):
        word = word[:-1]
        if word in lab:
            raise RuntimeError(f"Label `{word}` already defined")
        lab[ip] = word
# while ip < len(program):
ip = 0
while ip < len(program):
    code = program[ip]
    if code.endswith(':'):
        # print(f"Deque Values: {stack}")
        assert code.endswith(':')
        # code = code[:-1]
        # print(f"label: {code}")
        if code in lab:
            raise RuntimeError(f"Label {code} is already defined")
            # ip += 1
        code = code[:-1]
        lab[code] = ip
        lab_stack.append(lab[code])
        # calling_lab = lab[code]
        print(f"Labels: {lab}")
        print(f"Label Stack: {lab_stack}")
        ip += 1
    # print(stack)
    # print(program)
    elif code.isdigit():
        stack.append(code)
        ip += 1
        # print(stack)
    elif code == '+':
        try:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
        except IndexError:
            print(f"Instruction `{code}`")
        ip += 1
        # print(stack)
    elif code == 'write':
        tok[ip] = code
        try:
            if stack.count == 0:
                raise IndexError("You are popping from an empty deque.")
            else:
                a = stack.pop()
                print(a)
        except IndexError:
            raise RuntimeError("ERROR: You are writing nothing")
            # exit(1)
        ip += 1
         #print(stack)
    elif code == 'hwrite':
        try:
            a = stack.pop()[2:]
            bo = bytes.fromhex(a)
            a_s = bo.decode('ASCII')
            print(a_s)
        except IndexError:
            raise RuntimeError("ERROR: You are writing nothing")
            # exit(1)
        ip += 1
    elif code == '-':
        try:
            a = stack.pop()
            b = stack.pop()
            stack.append(a - b)
        except IndexError:
            print(f"Instruction `{code}`")
        ip += 1
    elif code == 'goto':
        print(f"Label Stack: {lab_stack}")
        try:
            a = lab_stack.pop()
            ip = a
            print(f"Next label definition is located in pos {ip}")
            lab_stack.append(a)
        except IndexError as e:
            print(f"ERROR: instruction `{code}` in pos {ip}: {e}")
            ip += 1
            exit(1)
        ip += 1
    
    elif code.startswith('"'):
        str_stack.append(program[ip])
        while not code.endswith('"'):
            try:
                str_stack.append(program[ip])
                ip += 1
                if code.endswith('"'):
                    a = " ".join(str_stack)
                    stack.append(a)
            except IndexError:
                raise RuntimeError("You are calling to an empty deque")
            ip += 1
        ip += 1
            # print(tok)
    elif code.endswith('"'):
        a = " ".join(str_stack)
            # a = str_stack.pop()
        stack.append(a)
        print("Stack reached here.")
        print(f"Main Stack: {stack}")
        ip += 1
    # Introduce Hexadecimals
    elif code.startswith('0x'):
         #print("warning: parsing a hexadecimal.")
        stack.append(code)
        ip += 1
    # print(f"Label IP: {lab[ip]}")
    
    elif code.startswith('0b'):
        stack.append(code)
        ip += 1
    elif code == lab[code]:
        # print(calling_lab)
        try:
            print(True)
            ip = lab[ip]
        except KeyError:
            print(f"ERROR: in pos {ip}:\n\tOh no, maybe the lexer thinks that this is a label.")
        ip += 1
    else:
        try:
            if code == lab[code]:
                ip += 1
                continue
        except ValueError:
            stack.append(int(code))
        ip += 1
    ip += 1 
# while ip < len(program):
#     word = program[ip]
#     if word.endswith(':'):
#         ip += 1
#        continue
