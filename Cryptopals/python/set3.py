#!/usr/bin/python3

import binascii
import base64
from aes_functions import *
from xorfunctions import is_probably_text
from Crypto.Util.number import long_to_bytes
from string import printable
import sys 

one_time_key = gen_random_key()

##########
# Fonctions de l'exo 17 : Padding oracle
##########

def encrypt_cookie() :

	global one_time_key

	strings = [ b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
				b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
				b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
				b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
				b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
				b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
				b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
				b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
				b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
				b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]

	plaintext = strings[random.randint(0, len(strings) - 1)]
	plaintext = b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic="
	l = len(plaintext.decode())
	print("Chosen string of length {} : {}".format(l, plaintext.decode()))
	plaintext = pkcs7_padding(plaintext)
	print(f"Chosen string padded before encryption : {plaintext}")

	try :
		ciphertext = aes_cbc_encryption(plaintext, one_time_key)
	except Exception as e:
		print(e)

	return ciphertext

def aes_cbc_padding_oracle(ciphertext) :

	global one_time_key
		
	plaintext = aes_cbc_decryption(ciphertext, one_time_key)

	try :
		return is_pkcs7_padding_correct(plaintext)
	except AssertionError as e :
		return False

def split_into_blocks(data, chunk = 16) :

	blocks = []
	for i in range(0, len(data), chunk) :
		blocks.append(data[i : i + chunk])

	return blocks


def get_trailing_bits(cipherblock, padding) :
	# This function returns a sequence of bytes made in such a way that when XOR'ed against the
	# previous cipherblock, it will give the padding value equals to padding + 1
	# So for instance if I have the sequence ABCDEFGHIJKLMXXX, I want to know what XXX needs to be so 
	# for the next round of padding oracle (4), I can be sure MXXX ^ YYYY will give 04h 04h 04h 04h.

	dk_c2 = b"" # This is what comes out of the deciphering function
	for byte in cipherblock :
		dk_c2 += bytes([byte ^ padding])
	#print(f"dk_c2 : {dk_c2}")
	# Now that I know what dk_c2 is, I need to know what to XOR it against so the resulting plaintext ends
	# with padding + 1

	trailing_bits = b""
	for byte in dk_c2 :
		for b in range(0, 256) :
			if byte ^ b == (padding + 1) :
				trailing_bits += bytes([b])

	#print(f"trailing_bits : {trailing_bits}")

	return trailing_bits # These will be the last bytes of c1_prime in recover_plaintext()


def recover_plaintext(ciphertext) :

	iv_and_texts = split_into_blocks(ciphertext)
	iv 		= iv_and_texts[0]
	blocks 	= iv_and_texts[1:]
	
	block_count = 0
	final_plaintext = b""

	while block_count < len(blocks) :
		if block_count == 0 :
			c1 = iv 
			c2 = blocks[0]
		else :
			c1 = blocks[block_count - 1]
			c2 = blocks[block_count]

		padding_round = 1
		tmp_plaintext = b""
		trailing_bits_for_padding = b""

		while padding_round <= 16 :
			for X in range(256) :
				c1_prime = c1[:16 - padding_round] + bytes([X]) + trailing_bits_for_padding
				# c1_prime is the block we're tampering with, X is the byte we're flipping and 
				# trailing_bits are the rest of the block made so that when XOR'ed against Dk(C2), it renders
				# good padding

				try :
					padding_ok = aes_cbc_padding_oracle(iv + c1_prime + c2)
					tmp_plaintext += bytes([X ^ padding_round ^ c1[16 - padding_round]])
					break
				except IncorrectPadding :
					pass
				except Exception as e :
					print(f"Plaintext giving exception : ", tmp_plaintext)
					print(e)

			trailing_bits_for_padding = get_trailing_bits(c1_prime[-padding_round:], padding_round)
			padding_round += 1

		final_plaintext += tmp_plaintext[::-1]
		block_count += 1
	
	print("Before unpadding : ", final_plaintext)
	return final_plaintext

##########
# Fonctions de l'exo 18 : Implement CTR
##########

def my_own_ctr(k, ciphertext, n) :
	ct = ciphertext
	key = k
	nonce = n
	c = 0
	counter = (c).to_bytes(8, byteorder="little")
	plaintext = b""

	for i in range(0, len(ct), 16) :
		nonce_counter = nonce + counter 
		keystream = AES.new(key, AES.MODE_ECB).encrypt(nonce_counter)
		for pair in zip(ct[i:i+16], keystream) :
			plaintext += bytes([pair[0] ^ pair[1]])
		c += 1
		counter = (c).to_bytes(8, byteorder="little")

	return plaintext

##########
# Fonctions de l'exo 19 : Break fixed-nonce CTR mode using substitutions
##########
valid_chars = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \'-,;.?:!"
key_counter = 1
memorized_keystreams = []

def len_of_shortest_line(ciphers, excluded_length = -1) :
	l = len(ciphers[0])

	for elem in ciphers[1:] :
		if len(elem) <= excluded_length :
			continue
		if len(elem) < l :
			l = len(elem)

	return l 

def compute_nb_keys(dict_of_bytes) :
	result = 1
	for key in dict_of_bytes.keys() :
		result *= len(dict_of_bytes[key])
	return result 

def build_keys_from_bytes_and_score(ciphertext, sets_of_bytes, start = b"") :

	global key_counter, memorized_keystreams 
	
	if len(sets_of_bytes) == 0: # We built a whole key so we can try to decrypt
		print(f"Trying key {key_counter}\r", end = "")
		sys.stdout.flush()
		plaintext = b""
		upper_limit = len(start)
		for i in range(0, len(ciphertext), upper_limit) :
			for pair in zip(start, ciphertext[i: i + upper_limit]) :
				plaintext += bytes([pair[0] ^ pair[1]])
		key_counter += 1
		if is_probably_text(plaintext[:upper_limit]) :
			print(f"Key number {key_counter - 1} : ", plaintext[:upper_limit])
			r = input("Memorize ?")
			if r == 'y' :
				memorized_keystreams.append(start)
		return

	key = start

	for elem in sets_of_bytes[0] :
		build_keys_from_bytes_and_score(ciphertext, sets_of_bytes[1:], start = key + elem)

def break_aes_ctr(ciphertexts) :
	ciphers = []
	for c in ciphertexts :
		ciphers.append(base64.b64decode(c)) # OK

	if len(memorized_keystreams) == 0 :
		shortest_length = len_of_shortest_line(ciphers)
		memorized = False
	else :
		shortest_length = len_of_shortest_line(ciphers, len(memorized_keystreams[0]))
		memorized = True
	i = 0 
	keystream = b""
	possible_keystream_bytes = {}

	while i < shortest_length :
		transposed_chars = b""
		for lines in ciphers :
			if len(lines) < shortest_length :
				continue
			transposed_chars += bytes([lines[i]]) # OK

		transposed_chars_xored = b""
		for n in range(256) :
			for char in transposed_chars :
				transposed_chars_xored += bytes([char ^ n])

			if all(c in valid_chars for c in transposed_chars_xored) :
				if i in possible_keystream_bytes.keys() :
					possible_keystream_bytes[i].append(bytes([n]))
				else :
					possible_keystream_bytes[i] = [bytes([n])]

			transposed_chars_xored = b""
		i += 1

	print("Possible keystream bytes : ", possible_keystream_bytes) # OK
	print(f"Nombre total de clés possibles : {compute_nb_keys(possible_keystream_bytes)}")
	if memorized :
		for elem in memorized_keystreams :
			build_keys_from_bytes_and_score(b"".join(c for c in ciphers), list(possible_keystream_bytes.values()), start = elem)
	else :
		build_keys_from_bytes_and_score(b"".join(c for c in ciphers), list(possible_keystream_bytes.values()))
	return b"pet"

##########
##########

if __name__ == "__main__" :

	#####
	# Exo 17
	#####
	
	"""
	cipher = encrypt_cookie()
	print("Let's start the attack...")
	result = recover_plaintext(cipher)
	print(base64.b64decode(pkcs7_unpad(result)))
	"""

	#####
	# Exo 18
	#####
	"""
	key = b"YELLOW SUBMARINE"
	nonce = (0).to_bytes(8, byteorder = "little")
	cipher = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")

	print("Plaintext final : ", my_own_ctr(key, cipher, nonce))
	"""

	#####
	# Exo 19
	#####

	nonce = (0).to_bytes(8, byteorder = "little")
	
	# That part is just for generating the file with encrypted strings against an unknown key
	"""
	secrets = ""
	with open("set3chall19.txt", 'r') as f : 
		secrets = f.read().split('\n')

	with open("set3chall19_encrypted.txt", 'wb') as f : 
		for s in secrets :
			plain_secret = base64.b64decode(s)
			encrypted_secret = my_own_ctr(one_time_key, plain_secret, nonce)
			print(encrypted_secret)
			f.write(base64.b64encode(encrypted_secret) + b'\n')
	"""

	# Now we actually attack the cipher by recovering the plaintexts without knowing the key

	with open("set3chall19_encrypted.txt", 'r') as f :
		secrets = f.read().split('\n')[:-1]

		plaintext = break_aes_ctr(secrets)
		print(plaintext)


