#!/usr/bin/python3

salt = b"f789bbc328a3d1a3"

import string
import hashlib

for i in range(1000000000000) :
    result = hashlib.md5(salt + str(i).encode("utf-8"))
    if i % 100000 == 0 :
        print(i)
    if result.hexdigest().startswith("0e") | result.hexdigest().startswith("00e") :
        if all(char in string.digits for char in result.hexdigest()[2:]) :
            print(i, result.hexdigest())
            exit()
