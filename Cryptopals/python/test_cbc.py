#!/usr/bin/python3
from aes_functions import *
key = gen_random_key()
secret = b"jamais o grand jamais je ne mangerai d'huitres sur le sol de cette cuisine, m'entendez-vous ?"
enc = aes_cbc_encryption(secret, key)
print(aes_cbc_decryption(enc, key))
