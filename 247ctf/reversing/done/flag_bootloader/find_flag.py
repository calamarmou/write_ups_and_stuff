#!/usr/bin/env python3

with open("instructionlist.txt", 'r') as f :
    instructions = [l.strip().split() for l in f.readlines()]
    print(instructions)
    result = ""

    for i in range(0, len(instructions), 2) :
        al_value = instructions[i][1].split(',')[1]
        al_value = int(al_value, 16)
        second_value = instructions[i+1][1].split(',')[1]
        second_value = int(second_value, 16)

        values = f"al : {al_value}, second : {second_value}"

        if instructions[i + 1][0] == "sub" :
            print(f"SUB {values}")
            al_value -= second_value
            print(al_value)
        elif instructions[i + 1][0] == "xor" :
            print(f"XOR {values}")
            al_value ^= second_value
            print(al_value)
        elif instructions[i + 1][0] == "add" :
            al_value += second_value
        result += str(al_value)

result = "247CTF{" + result.replace('0x', '')  + "}"
print(f"{result}, length : {len(result)}")
