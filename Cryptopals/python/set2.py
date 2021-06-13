#!/usr/bin/python3

from aes_functions import *
from base64 import b64decode
from binascii import unhexlify, hexlify
from functools import reduce 

import sys

if __name__ == "__main__" :

	key = b"YELLOW SUBMARINE"

	#####
	# Exo 10
	#####

	"""
				iv = bytes([0] * 16)
			
				with open("challenge10.txt", 'r') as f :
					deciphered_text = aes_cbc_decryption(b64decode(f.read()), key, iv)
					print("".join(elem.decode("utf-8") for elem in deciphered_text))
				
			"""
	#####
	# Exo 11
	#####

	"""
	msg = bytes([5] * 128)

	for i in range(10) :
		msg_crypt = encryption_oracle(msg)
		if is_ecb_or_cbc(msg_crypt) :
			print("lol")
	"""

	#####
	# Exo 12
	#####

	#print(aes_ecb_baat_attack().decode("utf-8"))

	#####
	# Exo 13
	#####

	#ecb_cut_and_paste_attack()

	#####
	# Exo 14
	#####

	#a = aes_ecb_baat_attack_hard()
	#print(a.decode())

	#####
	# Exo 15
	#####

	
"""	try :
		msg = is_pkcs7_padding_correct(b"ICE ICE BABYMDRL\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f")
		print(msg)
	except AssertionError :
		print("Padding incorrect !")
	"""

	#####
	# Exo 16
	#####

	"""cipher = aes_cbc_encrypt_userdata(sys.argv[1])
				cipher_blocks = [cipher[i : i + 16] for i in range(0, len(cipher) - 16 + 1, 16)]
			
				corrupted_block = list(cipher_blocks[1])
				corrupted_block[0] ^= 4
				corrupted_block[6] ^= 2
				corrupted_block[11] ^= 4
				cipher_blocks[1] = bytes(corrupted_block)
			
				print("I am an admin ? {} !".format(aes_cbc_lookforadmin(reduce(lambda b1, b2 : b1 + b2, cipher_blocks))))"""