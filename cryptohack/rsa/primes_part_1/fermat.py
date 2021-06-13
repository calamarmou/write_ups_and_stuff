#!/usr/bin/python3

import math

def is_square(a) :
    root = math.sqrt(a)
    if int(root + 0.5) ** 2 == a :
        return True
    else :
        return False

def fermat_factor(n) :
    a = math.ceil(math.sqrt(n))
    bsq = a * a - n
    while not math.modf(math.sqrt(bsq)) == 0.0 :
        a += 1
        bsq = a * a - n
    return a - sqrt(bsq)

if __name__ == "__main__" :
    n = 510143758735509025530880200653196460532653147
    print(fermat_factor(n))
