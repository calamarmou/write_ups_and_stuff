#!/usr/bin/python3

from Crypto.Cipher import AES
import base64
from binascii import unhexlify, hexlify
from attack_repeat_xor_key import hamming_distance

def aes_ecb_decryption(cipher, key) :
	
	decipher = AES.new(key, AES.MODE_ECB)
	return decipher.decrypt(cipher)

def aes_ecb_encryption(msg, key) :

	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(msg)

def detect_aes_ecb(cipher) :

	repetitions_per_string = []

	for elem in cipher.split('\n')[:-1] :
		identical_cipher_count = 0
		nb_strings_repeated = 0
		

		for i in range(0, len(elem), 4) :
			identical_cipher_count = elem.count(elem[i : i + 4])
			if identical_cipher_count >= 2 :
				nb_strings_repeated += 1

		repetitions_per_string.append((elem, nb_strings_repeated))
		nb_strings_repeated = 0

	return max(repetitions_per_string, key = lambda k : k[1])

if __name__ == "__main__" :

	#####
	# Exo 7
	#####
	"""
	key = b"YELLOW SUBMARINE"

	with open("challenge7.txt", 'r') as f :
		plaintext = aes_ecb_decryption(base64.b64decode(f.read()), key)

	print(plaintext.decode("utf-8"))
	"""

	#####
	# Exo 8
	#####

	"""
	with open("challenge8.txt", 'r') as f :
		text_ecb_encrypted = detect_aes_ecb(f.read())

	print("AES ECB encrypted text :\n{}".format(text_ecb_encrypted[0]))
	"""

	################################

	key = b"YELLOW SUBMARINE"

	print(aes_ecb_decryption(aes_ecb_encryption("lol j'aime le pate au saucisson!", key), key))