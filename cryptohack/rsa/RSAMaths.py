#!/usr/bin/python3

from decimal import *
import math

def is_square(a) :
    if a < 0 :
        return False
    sqr = Decimal(a).sqrt()
    return ((sqr - math.floor(sqr)) == 0)

class Factorisation() :

    def __init__(self) :
        pass

    def fermat(self, n) :
        a = Decimal(n).sqrt()
        bsq = a * a - n
        while not is_square(bsq) :
            a += 1
            bsq = a * a - n

        return a - Decimal(bsq).sqrt()

if __name__ == "__main__" :
    factor = Factorisation()
    #print(factor.fermat(7894561230))
