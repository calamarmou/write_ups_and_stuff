#!/usr/bin/python3

from binascii import *

def letter_ratio(input_bytes):

	ascii_text_chars = list(range(97, 123)) + [32]
	nb_letters = sum([ x in ascii_text_chars for x in input_bytes])

	return nb_letters / len(input_bytes)


def is_probably_text(input_bytes):

    r = letter_ratio(input_bytes)

    return r if r > 0.7 else False

def bxor(s1, s2) :
	
	return bytes([ x^y for (x,y) in zip(s1, s2)])

def bxor_byte(s, c) :

	keystream = c * len(s)
	return bxor(s, keystream)

def bxor_allchars(s) :

	allchars = [bytes([i]) for i in range(0, 256)]
	res = []

	for c in allchars : 
		#print("Testing {} against {}".format(s[0:15], c))
		byte_xor = bxor_byte(s, c)
		#print(byte_xor.decode("ascii"))
		score_is_text = is_probably_text(byte_xor)
		if  score_is_text is not False :
			#res.append("Key : ".encode("utf-8") + c + " | Message : ".encode("utf-8") + byte_xor +
			#	" | Original message : ".encode("utf-8") + s)
			msg = { "key" : c.decode("utf-8"),
					"message" : byte_xor.decode("utf-8"), 
					"original" : hexlify(s).decode("utf8"),
					"score" : score_is_text }
			#print(msg)
			res.append(msg)
	return res
    
def bxor_repeating_key(input, key) :

	rotation = 0
	res = "".encode("utf-8")

	for char in input :
		res += bxor(bytes([char]), bytes([key[rotation]]))
		rotation = (rotation + 1) % len(key)

	return res

if __name__ == "__main__" :

	"""
	A = unhexlify('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
	B = bytes([1])
	print(bxor_byte(A, B))
	"""
	
	#####
	# Exo 4
	####
	"""
	with open("exo4_trial.txt", 'r') as f :
		for line in f.readlines() :
			line_bytes = unhexlify(line.strip())
			decoded_strings = bxor_allchars(line_bytes)
			if len(decoded_strings) >= 1 :
				for elem in decoded_strings :
					print(elem)
	"""

	#####
	# Exo 5
	#####
	
	input = "lolmdrkikou xd!!!!!!!!!!!".encode("utf-8")
	key = "ICE".encode("utf-8")
	decrypt = bxor_repeating_key(input, key)
	print(hexlify(decrypt).decode("utf-8"))
	

	#####
	# Exo 6
	#####
	