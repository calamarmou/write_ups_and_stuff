#!/usr/bin/python3

from xorfunctions import *
import random 
from Crypto.Cipher import AES
import base64
from binascii import unhexlify, hexlify
from attack_repeat_xor_key import hamming_distance

super_key = b'\xea\xeb\xb0N\xc9\xcc\xb3\xb8\xf6\xeb\x86a\x02$\xa0S'
super_iv  = b'J\x89\xe0\x81&\xae\xcc\n\x98\x8bn\xc4\xc9qv\x0e'
one_time_key = b""
one_time_iv = b""

class IncorrectPadding(Exception) :
	pass

class user_profile :
	def __init__(self) :
		self.key = gen_random_key()

	@staticmethod
	def parse(byte_string) :

		string = byte_string.decode("latin-1")

		result = dict(pair.split('=') for pair in string.split('&'))
		
		return result

	@staticmethod
	def profile_for(email) :
		if b"&" in email or b"=" in email :
			raise ValueError("Invalid email address")
	
		return b"email=" + email + b'&uid=10&role=user'

	def get_encrypted_profile(self, email):
		profile = self.profile_for(email)
	
		return aes_ecb_encryption(profile, self.key)

	def decrypt_and_parse_profile(self, ctxt):
		profile = aes_ecb_decryption(ctxt, self.key)
		
		return self.parse(profile)

def pkcs7_padding(text_to_pad) :

	if len(text_to_pad) % 16 ==  0 :
		return text_to_pad + bytes([16] * 16)

	padding = 0

	while (len(text_to_pad) + padding) % 16 != 0 :
		padding += 1

	return text_to_pad + bytes([padding] * padding)

def pkcs7_unpad(text_to_unpad) :

	return text_to_unpad[:-text_to_unpad[-1]]

def is_pkcs7_padding_correct(padded_text) :

	if len(padded_text) % 16 != 0 :
		raise IncorrectPadding("Length of {} is {}, must be a multiple of 16 !\
			".format(padded_text, len(padded_text)))

	padding_char = padded_text[-1]
	padding_sequence = padded_text[-padding_char:]

	if all(c == padding_char for c in padding_sequence) :
		return True
	else :
		raise IncorrectPadding("Incorrect padding !") 



"""	padding_chars = []

	for i in range(1, 17) :
		padding_chars.append(bytes([i]))

	if not bytes([padded_text[-1]]) in padding_chars :
		return True
	else :
		count = 0
		while bytes([padded_text[-count-1]]) in padding_chars :
			count += 1
		
		if not all(c == count for c in padded_text[-count :]) :
			raise IncorrectPadding("Incorrect padding !")
		
	return True"""

def gen_random_key() :

	random_key = [random.randint(0,255) for i in range(0 ,16)]

	return bytes(random_key)

def encryption_oracle(msg) :

	key = gen_random_key()
	iv = gen_random_key()

	bytes_added_start = bytes(random.randint(5, 10))
	bytes_added_end = bytes(random.randint(5, 10))

	msg = bytes_added_start + msg + bytes_added_end
	msg = pkcs7_padding(msg)

	encryption_mode = random.randint(1, 2)

	if encryption_mode == 1 :
		return aes_ecb_encryption(msg, key)
	else :
		return aes_cbc_encryption(msg, key, iv)

def is_ecb_or_cbc(ciphertext) :

	return True if aes_ecb_oracle(ciphertext) else False

##################################################
# AES ECB
##################################################

def aes_ecb_decryption(cipher, key) :
	
	decipher = AES.new(key, AES.MODE_ECB).decrypt(cipher)

	return decipher

def aes_ecb_encryption(msg, key) :

	cipher = AES.new(key, AES.MODE_ECB)

	return cipher.encrypt(msg)

def aes_ecb_oracle(cipher) :

	identical_cipher_count = 0
	nb_strings_repeated = 0
		
	for i in range(0, len(cipher), 4) :
		identical_cipher_count = cipher.count(cipher[i : i + 4])
		if identical_cipher_count >= 2 :
			nb_strings_repeated += 1

	if nb_strings_repeated >= 4 :
		return True
	else :
		return False

"""
	Easy version for aes_ecb_baat_attack
"""
def aes_ecb_add_secret_b64(user_input) :

	global super_key
	
	sample = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
			aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
			dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\
			YnkK"

	sample = base64.b64decode(sample)
	user_input = pkcs7_padding(user_input + sample)

	return aes_ecb_encryption(user_input, super_key)

"""
	Hard version for aes_ecb_baat_attack_hard
"""
def aes_ecb_add_secret_b64_hard(user_input) :

	global super_key

	sample = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
			aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
			dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\
			YnkK"

	prepend = bytes([random.randint(10, 20)] * random.randint(1, 5))

	sample = base64.b64decode(sample)
	user_input = pkcs7_padding(prepend + user_input + sample)

	return aes_ecb_encryption(user_input, super_key) 

def aes_ecb_baat_attack() :

	my_string = b'A' * 32
	my_string_encrypted = aes_ecb_add_secret_b64(my_string)
	total_length = len(my_string_encrypted) - 32 # For further use when we need to know when to stop brute-forcing

	# Figuring out the length of the cipher block
	result = aes_ecb_add_secret_b64(my_string[:1])
	block_length = len(result)

	for i in range(2, len(my_string)) :
		result = aes_ecb_add_secret_b64(my_string[:i])
		cur_len = len(result)
		if cur_len > block_length :
			block_length = cur_len - block_length
			print("Cipher block size : {}".format(block_length))
			break

	# Detecting if we're dealing with ECB or not
	if aes_ecb_oracle(my_string) :
		print("Function is using AES ECB mode.")

	# Creating a dictionary of all possible 'AAAAA...X' to compare the results
	# with the actual back-end encryption

	# So with one byte short, the first byte to go up to 16 should be
	# the first byte of the secret string, we keep that in memory for later 
	one_byte_short = bytes([ord('A')] * (block_length - 1))
	secret_string_leaked = aes_ecb_add_secret_b64(one_byte_short)[:16]
	
	# Now we're gonna create all 16 bytes possible strings in order to
	# match them against the true encrypted string
	last_byte_dictionary = {}
	discovered_byte = b''
	count = 1
	nbBlocks = 1

	while total_length != 0 :

		for i in range(1, 256) :
			brute_string = bytes([ord('A')] * (block_length - count)) + discovered_byte + bytes([i])
			last_byte_dictionary[brute_string] = aes_ecb_add_secret_b64(brute_string)[:16 * nbBlocks]

		dict_keys = list(last_byte_dictionary.keys())
		dict_values = list(last_byte_dictionary.values())

		if secret_string_leaked in dict_values :
			# Need to find the key corresponding to the value !
			discovered_byte += dict_keys[dict_values.index(secret_string_leaked)][-1:]

			count += 1
			last_byte_dictionary = {}

			if len(discovered_byte) % 16 == 0 :
				nbBlocks += 1
				count = 1

			secret_string_leaked = aes_ecb_add_secret_b64(bytes([ord('A')] * (block_length - count)))[:16 * nbBlocks]

		total_length -= 1

	return b"Retrieved :\n" + discovered_byte

def aes_ecb_baat_attack_hard() :

	# NE SEMBLE PAS FONCTIONNER POUR LES CHAINES DE CARACTERE
	# INFERIEURES A UNE LONGUEUR DE 32 :(

	"""
	b'Q\xc5:"8\xedp\xa1$\xf5 8I\x93\xb4\x8f'
	b'fY\xf8O6\xe5\x8d\xbehhLi\x97\xe7\\\xef'
	b'fY\xf8O6\xe5\x8d\xbehhLi\x97\xe7\\\xef'
	b'fY\xf8O6\xe5\x8d\xbehhLi\x97\xe7\\\xef'
	b"\x92\x1f~g\x1a\x1c\xf7\x10IO|'Ia\xfd\xc5"

	Voilà ce que j'obtiens sur un test avec 62 A. Les lignes 2 à 4 correspondent à
	AAA.... Le nombre d'octets ajouté au début étant aléatoire, je ne sais pas
	combien de A "débordent" sur le bloc suivant.
	Néanmoins en appelant la fonction plusieurs fois, je finis par obtenir ceci :
	b'\x1d\xe2m\x16N\xe4\xf1\xc5\xc2\x91XlT,\xc8\x98'
	b'fY\xf8O6\xe5\x8d\xbehhLi\x97\xe7\\\xef'
	b'fY\xf8O6\xe5\x8d\xbehhLi\x97\xe7\\\xef'
	b'\xb9\x8c\x92b\xf5\tw\xd51;l\xc2\xe9\x7f\xd0\xdf'

	Comme j'envoie 62 A, le fait que la ligne 4 ait changé signifie qu'elle n'est
	plus composée uniquement de A, or comme chaque bloc fait 16 caractères, ça veut 
	forcément dire que la chaîne 
	b'\x1d\xe2m\x16N\xe4\xf1\xc5\xc2\x91XlT,\xc8\x98'
	correspond à XAAAA... et que la chaîne 
	b'\xb9\x8c\x92b\xf5\tw\xd51;l\xc2\xe9\x7f\xd0\xdf'
	correponds à AAAA...Y

	J'imagine que je n'ai plus qu'à appeler la fonction en boucle, jusqu'à ce que
	la première ligne matche celle plus haut, et ensuite je fais les caractères
	un par un comme dans la version facile.
	"""

	input_s = b'A' * 30
	input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s)

	"""
	Là on va essayer de déterminer statistiquement quelles sont les chaînes de contrôle pour
	la suite du programme. Ce qu'on veut savoir c'est à quoi ressemble, une fois chiffré,
	une chaîne composée de 16 A, et à quoi ressemble, une fois chiffré, une chaîne composée
	d'un caractère aléatoire suivie de 15 A.
	On va donc faire plusieurs appels à la fonction de chiffrement et, logiquement,
	la chaîne avec un seul caractère aléatoire au début sera celle qui apparaît le moins, et
	par conséquence la chaîne avec 16 A celle qui apparaît le plus.
	"""

	string_of_A_encrypted = b""
	beginning = b""
	appearances = {}
	appearances[input_s_encrypted[16:32]] = 1

	for i in range(0, 50) :
		input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s)
		if input_s_encrypted[16:32] in appearances.keys() :
			appearances[input_s_encrypted[16:32]] += 1
		else :
			appearances[input_s_encrypted[16:32]] = 1

	appearances_keys = list(appearances.keys())
	if appearances[appearances_keys[0]] > appearances[appearances_keys[1]] :
		min_index = 1
		string_of_A_encrypted = appearances_keys[0]
	else :
		min_index = 0
		string_of_A_encrypted = appearances_keys[1]

	for i in range(0, 20) :
		input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s)
		if input_s_encrypted[16:32] == appearances_keys[min_index] :
			beginning = input_s_encrypted[:16]
			break

	while input_s_encrypted[16:32] == string_of_A_encrypted :# b"fY\xf8O6\xe5\x8d\xbehhLi\x97\xe7\\\xef" :
		input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s)
		
	length_secret = len(input_s_encrypted) - 31 # Lenght of AAA...A + 1 random byte

	i = 0
	length_bfs = length_secret
	
	while (length_secret + i) % 16 != 0 :
		length_bfs += 1
		i += 1
	
	# On recompile input_s pour qu'elle soit de la bonne taille afin de faciliter les comparaisons ultérieures
	input_s = b'A' * (length_bfs - 2)
	input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s)

	while input_s_encrypted[length_bfs - 16 : length_bfs] == string_of_A_encrypted : # b'fY\xf8O6\xe5\x8d\xbehhLi\x97\xe7\\\xef' :
		input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s)

	bfs = b'A' * (length_bfs - 2)
	bfs_encrypted = b""

	dict_encrypted_string = {}
	discovered_byte = b""

	nbBlocks = 1
	
	while length_secret != 0 :

		for i in range(0, 256) :
			
			s_to_encrypt = bfs[:len(bfs) - len(discovered_byte)] + discovered_byte + bytes([i])
			bfs_encrypted = aes_ecb_add_secret_b64_hard(s_to_encrypt)

			while bfs_encrypted[:16] != beginning : # b"\x1d\xe2m\x16N\xe4\xf1\xc5\xc2\x91XlT,\xc8\x98" :
				bfs_encrypted = aes_ecb_add_secret_b64_hard(s_to_encrypt)
			
			dict_encrypted_string[i] = bfs_encrypted[length_bfs - 16 * nbBlocks : length_bfs]

		dict_keys = list(dict_encrypted_string.keys())
		dict_values = list(dict_encrypted_string.values())
		
		matching_s = input_s_encrypted[length_bfs - 16 * nbBlocks : length_bfs]

		if matching_s in dict_values :
			discovered_byte += bytes([dict_keys[dict_values.index(matching_s)]])
			# On recompile à nouveau input_s avec un A en moins pour avoir un
			# caractère en plus de la chaîne qu'on chercher à décoder
			# AAAAA....AAA
			# AAAA.....AXY <-
			input_s = b'A' * (length_bfs - 2 - len(discovered_byte))
			input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s) 
			
			while input_s_encrypted[:16] != beginning :# b"\x1d\xe2m\x16N\xe4\xf1\xc5\xc2\x91XlT,\xc8\x98" :
				input_s_encrypted = aes_ecb_add_secret_b64_hard(input_s)
			
		if len(discovered_byte) % 16 == 0 :
			print("Found so far :")
			print(discovered_byte.decode())
			nbBlocks += 1
		
		length_secret -= 1
		bfs_encrypted = b""
		dict_encrypted_string = {}
		
	return(discovered_byte)

def ecb_cut_and_paste_attack() :

	# In order to set the role to admin, we need first to submit an
	# email adress that will ensure we get "user" as the beginning of 
	# a new block (block number 3)
	
	email = b"wird@mail.com"

	"""
	s_test = b"email=" + email + b"&uid=10&role=user"
	print(b" | ".join(s_test[i:i+16] for i in range(0, len(s_test), 16)))
	"""

	up = user_profile()
	enc_profile = up.get_encrypted_profile(email)
	get_beginning_of_string = enc_profile[0:32]

	# This mail address will give us a block starting with the word "admin"
	# (block number 2) and ending by the necessary padding

	email_admin = b"abcdefghijadmin" + b'\x0b' * 11

	enc_admin_profile = up.get_encrypted_profile(email_admin)
	get_admin_part = enc_admin_profile[16:32]

	dec_profile = up.decrypt_and_parse_profile(get_beginning_of_string + get_admin_part)

	print(dec_profile)


##################################################
# AES CBC
##################################################

"""def aes_cbc_decryption(cipher, key, iv) :

	deciphered_blocks = []

	for i in range(1, len(cipher) // 16 ) :

		slice1 = slice(len(cipher) - i * 16, len(cipher) - 16 * (i - 1))
		slice2 = slice(len(cipher) - 16 * (i + 1), len(cipher) - i * 16)

		last_block = aes_ecb_decryption(cipher[slice1], key)
		deciphered_blocks.append(bxor(last_block, cipher[slice2]))

	first_block = aes_ecb_decryption(cipher[0 : 16], key)
	deciphered_blocks.append(bxor(first_block, iv))

	result = bytes()
	for i in range(len(deciphered_blocks) - 1, -1, -1) :
		result += deciphered_blocks[i]

	return result

def aes_cbc_encryption(plaintext, key, iv) :

	ciphered_text = bytes()

	assert(len(plaintext) % 16 == 0)

	first_block = bxor(plaintext[0 : 16], iv)
	first_block = aes_ecb_encryption(first_block, key)
	previous_block = first_block
	ciphered_text += first_block

	for i in range(1, len(plaintext) // 16) :
		current_block = bxor(previous_block, plaintext[i * 16 : (i + 1) * 16])
		current_block = aes_ecb_encryption(current_block, key)
		previous_block =  current_block
		ciphered_text += current_block

	return ciphered_text"""

def aes_cbc_encryption(plaintext, key) :

	if len(plaintext) % 16 != 0 :
		plaintext = pkcs7_padding(plaintext)

	iv = gen_random_key()

	first_block = bxor(plaintext[0 : 16], iv)
	first_block = aes_ecb_encryption(first_block, key)
	previous_block = first_block
	ciphertext = first_block

	for i in range(1, len(plaintext) // 16) :
		current_block = bxor(previous_block, plaintext[i * 16 : (i + 1) * 16])
		current_block = aes_ecb_encryption(current_block, key)
		previous_block =  current_block
		ciphertext += current_block	

	return iv + ciphertext

def aes_cbc_decryption(cipher, key) :

	deciphered_blocks = []

	for i in range(1, len(cipher) // 16 - 1) :

		slice1 = slice(len(cipher) - i * 16, len(cipher) - 16 * (i - 1))
		slice2 = slice(len(cipher) - 16 * (i + 1), len(cipher) - i * 16)

		last_block = aes_ecb_decryption(cipher[slice1], key)
		deciphered_blocks.append(bxor(last_block, cipher[slice2]))

	first_block = aes_ecb_decryption(cipher[16 : 32], key)
	deciphered_blocks.append(bxor(first_block, cipher[0 : 16]))

	plaintext = bytes()
	for i in range(len(deciphered_blocks) - 1, -1, -1) :
		plaintext += deciphered_blocks[i]

	return plaintext

def aes_cbc_encrypt_userdata(input_s) :

	global super_key, super_iv

	input_s = input_s.replace('=', '?').replace(';', '?')

	prepended = "comment1=cooking%20MCs;userdata=".encode()
	appended = ";comment2=%20like%20a%20pound%20of%20bacon".encode()

	final_s = prepended + input_s.encode() + appended

	final_s = pkcs7_padding(final_s) 

	try :
		cipher = aes_cbc_encryption(final_s, super_key, super_iv)
		return cipher
	except AssertionError as e :
		print("The length of the message should be a multiple of 16 ! Error :\n{}".format(e))

def aes_cbc_lookforadmin(ciphertext) :

	global super_key, super_iv

	plaintext = aes_cbc_decryption(ciphertext, super_key, super_iv).decode("latin-1")
	print(plaintext)
	plaintext = plaintext.split(';')

	for elem in plaintext :
		pair = elem.split('=')
		if (pair[0] == "admin") & (pair[1] == "true") :
			return True

	return False



##################################################




