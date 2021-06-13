#!/usr/bin/env python3

import re

def replace_flag_by_letter(op, fmu) :
    r = re.compile("flag\[\d{,2}\]")
    flags = re.findall(r, op)
    result = op
    for f in flags :
        result = result.replace(f, fmu[f])
    
    return result

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN"
unknowns = list(alphabet)
list_operations = []
with open("list_operations.txt", 'r') as f :
    list_operations = f.read().split("&&")

flags_matches_unknowns = [f"flag[{i}]" for i in range(40)]
flags_matches_unknowns = dict(zip(flags_matches_unknowns, unknowns)) 
#print(flags_matches_unknowns)
flags_matches_unknowns["flag[0]"] = str(ord('2'))
flags_matches_unknowns["flag[1]"] = str(ord('4'))
flags_matches_unknowns["flag[2]"] = str(ord('7'))
flags_matches_unknowns["flag[3]"] = str(ord('C'))
flags_matches_unknowns["flag[4]"] = str(ord('T'))
flags_matches_unknowns["flag[5]"] = str(ord('F'))
flags_matches_unknowns["flag[6]"] = str(ord('{')) 
flags_matches_unknowns["flag[39]"] = str(ord('}'))

"""
i = alphabet.index('i')
flags_matches_unknowns[f"flag[{i}]"] = "4015 / (123 - z)"

k = alphabet.index('k')
flags_matches_unknowns[f"flag[{k}]"] = "-3933 / (u - 123)"

m = alphabet.index('m')
flags_matches_unknowns[f"flag[{m}]"] = "(3350 / 67 + (98 / (51 - v)))"

n = alphabet.index('n') # -100 / 50 + M
flags_matches_unknowns[f"flag[{n}]"] = "108 / (t - 50)"

o = alphabet.index('o')
flags_matches_unknowns[f"flag[{o}]"] = "110 / (K - 100)"

p = alphabet.index('p')
flags_matches_unknowns[f"flag[{p}]"] = "(M - 8)"

A = alphabet.index('A')
flags_matches_unknowns[f"flag[{A}]"] = "98 / (51 - v)"

E = alphabet.index('E')
flags_matches_unknowns[f"flag[{E}]"] = "400 / (n - 50)"

H = alphabet.index('H')
flags_matches_unknowns[f"flag[{H}]"] = "100"

I = alphabet.index('I')
flags_matches_unknowns[f"flag[{I}]"] = "51"

M = alphabet.index('M') # M = 8 + p
flags_matches_unknowns[f"flag[{M}"] = "-112 / (52 - n)"
"""

equations = []
for op in list_operations :
    equations.append(replace_flag_by_letter(op, flags_matches_unknowns))


print('\n'.join(i for i in equations))


