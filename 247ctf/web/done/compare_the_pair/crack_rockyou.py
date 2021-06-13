#!/usr/bin/python3

import requests
import hashlib
import string

password_hash = "0e902564435691274142490923013038"
salt = b"f789bbc328a3d1a3"
base_path = "/opt/SecLists/Passwords/Leaked-Databases/"
file_list = ["rockyou-05.txt",
"rockyou-10.txt",
"rockyou-15.txt",
"rockyou-20.txt",
"rockyou-25.txt",
"rockyou-30.txt",
"rockyou-35.txt",
"rockyou-40.txt",
"rockyou-45.txt",
"rockyou-50.txt",
"rockyou-55.txt",
"rockyou-60.txt",
"rockyou-65.txt",
"rockyou-70.txt",
"rockyou-75.txt",
"../darkc0de.txt"]

for l in file_list :
    print(f"Opening {l}")
    with open(base_path + l) as f :
        for elem in f.readlines() :
            result = hashlib.md5(salt + elem.strip().encode("utf-8")).hexdigest()
            if result.startswith("0e") | result.startswith("00e") :
                if all(char in string.digits for char in result[2:]) :
                    print(elem)
                    exit()
