#!/usr/bin/python3

from binascii import *
from xorfunctions import *
import base64

"""
def hamming_distance(a, b):
    return sum(bin(byte).count('1') for byte in bxor(a,b))
"""

def hamming_distance(input1, input2) :

	hamming = 0

	for c1, c2 in zip(input1, input2) :
		bc1 = f"{c1:8b}"
		bc2 = f"{c2:8b}"

		for b1, b2 in zip(bc1, bc2) :
			if b1 != b2 :
				hamming += 1

	return hamming
	
def guess_keysize(cipher) :

	keysizes = list(range(2, 41))
	list_ham_dist = []
	score = 0
	nbChunks = 0

	for size in keysizes :
		nbChunks = len(cipher) / size
		score = sum(hamming_distance(cipher[i:i+size], cipher[i+size:i+2*size]) for i in range (0, len(cipher) - size, size))
		score /= size 
		score /= nbChunks

		list_ham_dist.append([score, size])
		score = 0

	#print(list_ham_dist)
	list_ham_dist.sort()
	return list_ham_dist[:3]

def break_vigenere(input) :
	
	print("Breaking Vigenere...")
	print("Computing Hamming distances...")
	likely_keysizes = guess_keysize(input) 
	print("Possible key sizes : " + ", ".join(str(k[1]) for k in likely_keysizes))

	# Break the ciphertext into blocks of KEYSIZE length
	list_ciphertext_by_keysize = []

	for ks in likely_keysizes :
		print("Trying with a keysize of {} bytes...".format(ks[1]))
		blocks = [input[i : i + ks[1]] for i in range(0, len(input), ks[1])] 
		list_ciphertext_by_keysize.append(blocks)

	# Make a block that is the first byte of every block, and a block that is 
	# the second byte of every block, and so on.
	for element in list_ciphertext_by_keysize :
		transposed_blocks = []
		key = ""

		#print("\nlen element : {}, element[0:5] : {}, len element[0] : {}\
				#".format(len(element), element[0:5], len(element[0])))
		for byteIndex in range(0, len(element[0])) :
			for i in range(0, len(element)) :
					try :
						transposed_blocks.append(element[i][byteIndex])
					except IndexError :
						pass
			
			res_bxor = bxor_allchars(bytes(transposed_blocks))
			
			if len(res_bxor) > 0 :
				# If there's only one result...
				if len(res_bxor) ==  1 :
					key += res_bxor[0]["key"]
				# If there are several possible keys, pick the one with the best score
				else :
					highest_score = 0
					highest_score_index = 0
					for i in range(len(res_bxor)) :
						if res_bxor[i]["score"] > highest_score :
							highest_score = res_bxor[i]["score"]
							highest_score_index = i

					key += res_bxor[highest_score_index]["key"]

			transposed_blocks *= 0

		if len(key) > 0 :
			print("####################")
			print("Your key might be '{}' !".format(key))
			print("####################")
			print("Does it make sense ?\n")
			print("##### Deciphered text #####")
			print(bxor_repeating_key(input, key.encode("utf-8")).decode("utf-8"))
			print("##### End of deciphered text #####")




if __name__ == "__main__" :

	#####
	# Exo 6.2
	#####
	"""
	ham = hamming_distance(b"this is a test", b"wokka wokka!!!") # Must be equal to 37
	print(ham)
	"""

	with open("exo6.txt", 'r') as f :
		file = base64.b64decode(f.read())
		break_vigenere(file)
		

