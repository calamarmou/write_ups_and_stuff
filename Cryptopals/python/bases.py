#!/usr/bin/python3

###############
# asciitob2
#
# b2tob10
# b2tohex
# b2tob64
# b2toascii
#
# b10tob2
#
# hextob2
###############

hexChars = "0123456789abcdef"
base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

#########
# ASCII #
#########

def asciitob2(s) :

    res = ""

    for c in s :
        res += b10tob2(ord(c))

    return res

##########
# Base 2 #
##########

def b2tob10(s, nbBytes = 0) :

    res = 0
    l = len(s)

    for n in s :
        res += 2 ** (l - 1) * int(n)
        l -= 1

    return res

####################

def b2tohex(s) :

    chunk_size = 4
    res = ""

    bitBlocks = [ s[i : i + chunk_size] for i in range(0, len(s), chunk_size) ]

    for _4bits in bitBlocks :
        hexChar = hexChars[b2tob10(_4bits)]
        res += hexChar

    return res

####################

def b2tob64(s) :

    complement = ""
    res = ""

    # On sépare une première fois la chaîne en blocs de 24 bits
    chunk_size = 24
    byteBlocks = [ s[i : i + chunk_size] for i in range(0, len(s), chunk_size) ] 

    # On vérifie s'il faut complémenter avec =
    if len(byteBlocks[-1]) == 8 :
        byteBlocks[-1] += '0000'
        complement = '=='
    elif len(byteBlocks[-1]) == 16 :
        byteBlocks[-1] += '00'
        complement = "="

    # Puis on sépare chaque bloc de 24 bits en 4 blocs de 6 bits
    chunk_size = 6
    
    for _24bits in byteBlocks :
        _6bitgroups = [ _24bits[i : i + chunk_size] for i in range(0, len(_24bits), chunk_size) ]
        for _6bits in _6bitgroups :
            res += base64Chars[b2tob10(_6bits)]
    
    return res + complement

####################

def b2toascii(s) :

    res = ""
    chunk_size = 8

    bitBlocks = [ s[i : i + chunk_size] for i in range(0, len(s), chunk_size) ]
    
    for elem in bitBlocks :
        res += chr(b2tob10(elem[1:])) # Parce qu'on est sur 7 bits en ASCII

    return res


###########
# Base 10 #
###########

def b10tob2(n, nbBits = 8) :

    res = ""

    if n == 0 :
        return nbBits * '0'

    while n != 0:

        res += str(n % 2)
        n = n // 2

    if nbBits != 0 :

        while len(res) % nbBits != 0 :
            res += '0'

    return res[::-1]

###############
# Hexadécimal #
###############

def hextob2(s, nbBits = 4) :

    byteString = ""

    # On s'assure qu'on a des groupes de 2 caractères, sinon
    # on triche en rajoutant un 0 en avant-dernière position
    if len(s) % 2 != 0 :
        s = s[0:len(s) - 1] + '0' + s[-1]

    for c in s :
        code_char = hexChars.find(c.lower())
        if code_char == -1 :
            print("Erreur, caractère non hexadécimal !")
            print(s)
            print(c)
            exit()
        byteString += b10tob2(code_char, nbBits)

    return byteString

if __name__ == "__main__" :

    print(asciitob2("coucou"))
    print(b2toascii("01110000011001010111010001100101011100100010000001110000011000010111001000100000011101000110010101110010011100100110010100100000011011000110111101101100"))
