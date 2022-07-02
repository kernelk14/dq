#!/usr/bin/env pypy3
import os
from collections import deque
import sys
import getopt


# prog = "5 6 + write 10 11 - write"
stack = deque()
str_stack = deque()
lab_stack = deque()
tok = {}
lab = {}
if len(sys.argv) < 2:
    print("ERROR: No file specified")
prog = sys.argv[1]

file = open(prog, 'r')
reader = file.read()

tokens = ['write', '+', '-', '"']

program = [
    word for line in reader.splitlines() if not line.lstrip().startswith('#')
    for word in line.split(' ') if len(word) > 0
]
p = os.path.splitext(prog)
out_file_path = p[0] + '.cpp'
out = open(out_file_path, 'w')
#prog = sys.argv[2]
# file = open(prog, 'r')
# reader = file.read()

 #tokens = ['write', '+', '-', '"']
# print(str(tokens))
# program = [
#     word for line in reader.splitlines() if not line.lstrip().startswith('#')
#     for word in line.split(' ') if len(word) > 0
# ]
# print(program)
# for ip in range(len(program)):
#     word = program[ip]
#     if word.endswith(':'):
#         word = word[:-1]
#         if word in lab:
#             raise RuntimeError(f"Label `{word}` already defined")
#         lab[ip] = word
# while ip < len(program):
def interpret(program):
    ip = 0
    # while ip < len(program):
    for ip in range(len(program)):
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
                # print(stack)
                a = stack.pop()
                b = stack.pop()
                stack.append(int(a) + int(b))
            except IndexError as e:
                print(f"ERROR: Instruction `{code}`, {e}")
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
                # print(stack)
                a = stack.pop()
                b = stack.pop()
                stack.append(int(a) - int(b))
            except IndexError as e:
                print(f"ERROR: Instruction `{code}`, {e}")
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
        elif code == '*':
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a) * int(b))
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
        elif code == 'drop':
            stack.pop()
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

def com(program):    
    ip = 0
    out.write("#include <iostream>\n")
    out.write("int main(void) {\n")
    for ip in range(len(program)):
        code = program[ip]
        if code.endswith(':'):
            code = code[:-1]
            for code in lab:
                raise RuntimeError(f"Label {code} already defined.")
            lab[code] = ip
    stack = deque()
    # while ip < len(program):
    assert ip < len(program), "The program exceeds the number of instruction."
    # print(len(program))
    # print(ip)
    for ip in range(len(program)): 
        print(stack)
        code = program[ip]
        if code.endswith(':'):
           ip += 1
           continue
        if code == 'write':
            a = stack.pop()
            out.write(f"std::cout << {a} << std::endl;\n")
            print(f"`{code}`: Write Completed.")
            ip += 1
        elif code == '+':
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a) + int(b))
            print(f"`{code}`: Added objects inside the stack.")
            # out.write(f"std::cout << {int(a)} + {int(b)} << endl;\n")
            ip += 1
        elif code == '-':
            a = stack.pop()
            b = stack.pop()
            stack.append(a - b)
            print(f"`{code}`: Subtracting objects inside the stack.")
            ip += 1
        elif code == '*':
            a = stack.pop()
            b = stack.pop()
            stack.append(a * b)
            ip += 1
        elif code.startswith('0x'):
            #print("warning: parsing a hexadecimal.")
            stack.append(code)
            ip += 1
        elif code == 'hwrite':
            try:
                print(stack)
                a = stack.pop()[2:]
                print(a)
                bo = bytes.fromhex(a)
                a_s = bo.decode('ASCII')
                out.write(f"std::cout << \"{a_s}\" << std::endl;\n")
            except IndexError:
                raise RuntimeError("ERROR: You are writing nothing")
                # exit(1)
            ip += 1
        elif code == 'goto':
            print(f"Goto Stack: {stack}")
            a = stack.pop()
            ip = a
        else:
            try:
                stack.append(int(code))
                print(f"`{code}`: Stack Updated.")
                print(stack)
                ip += 1
            except ValueError:
                stack.append(lab[code])
                ip += 1
            # ip += 1
        # ip += 1
    print(stack)
    ip += 1
    out.write("}\n")
    # assert False, "Compiling programs not implemented."

def usage():
    print("./main.py [args] <filename>")
com(program)