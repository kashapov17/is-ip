#!/usr/bin/python

import sys
import argparse
import string
import sympy as sp
from enum import Enum

appname = "hillpher"
appver = "0.1"

alph = (string.digits + string.ascii_letters + string.punctuation + " ").replace("$", "").replace("&", "")
#alph = string.digits+string.ascii_letters+",.() "
keyPower = 32 #max key lengh = 2^32 = about 4 billion

class operation(Enum):
    encode = 0
    decode = 1

def main(result):
    print("\'{}\'".format(result))
    return 0

def encode(plaintext, key):
    keyPower = int(len(key)**0.5)
    plaintext = textCompletion(plaintext, keyPower)

    ciphertext = ""
    for i in range(int(len(plaintext) / keyPower)):
        ciphertext += createStrFromMatrix(
            (createMatrixFromStr(plaintext[keyPower*i:keyPower*(i+1)], 1) 
             * createMatrixFromStr(key, keyPower))
            % len(alph)
            )

    return ciphertext

def decode(ciphertext, key):
    keyPower = int(len(key)**0.5)
    
    plaintext = ""
    for i in range(int(len(ciphertext) / keyPower)):
        plaintext += createStrFromMatrix(
            (createMatrixFromStr(ciphertext[keyPower*i:keyPower*(i+1)], 1) 
             * invMatrixMod(createMatrixFromStr(key, keyPower), len(alph)))
            % len(alph)
            )
    
    return(plaintext)

def keyCompletion(key):
    for i in range(1, keyPower):
        keyLenght = len(key)
        if keyLenght <= i**2:
            offset = alph.find('a')
            for j in range(offset, i**2 - keyLenght + offset):
                key += alph[j]
            break
    return key

def textCompletion(text, keyPower):
    while(len(text) % keyPower):
        text += " "
    return text

def isAlphConsistOf(string):
    if string != None:
        for l in string:
            if alph.find(l) == -1:
                print("Error: symbol \'{}\' not contained in the alphabet".format(l))
                print("Allowable set of symbols: {}".format(tuple(alph)))
                sys.exit()

def createMatrixFromStr(string, order):
    m = list(string)
    for i,l in enumerate(m):
        m[i] = int(alph.find(l))
    m = sp.Matrix(m)
    if order != 1:
        m = m.reshape(order, order)
    else:
        m = m.T
    return m

def createStrFromMatrix(m):
    string = ""
    for x in m:
        string += alph[x]
    return string

def gcdExtended(a, b):  
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcdExtended(b, a % b)
        return d, y, x - y * (a // b)


def multInvMod(num, mod):
    gcd,x,y = gcdExtended(num, mod)
    if x > 0:
        return x
    elif x < 0:
        if num > 0:
            return -x
        elif num < 0:
            return mod+x

def invMatrixMod(m, mod):
    det = int(sp.det(m))
    detInv = multInvMod(det, mod)
    return (m.adjugate() % mod) * detInv % mod

def checkInput(key, plaintext, ciphertext):
    isAlphConsistOf(plaintext)
    isAlphConsistOf(ciphertext)
    isAlphConsistOf(key)
    
    keyMatrix = createMatrixFromStr(args.key, int(len(args.key)**0.5))
    det = sp.det(keyMatrix)
    gcd,x,y = gcdExtended(sp.det(keyMatrix), len(alph))
    if det == 0:
        print("Error: bad key, choose another one [zero-determinant]")
        sys.exit()
    elif x == 0:
        print("Error: bad key, choose another one [inverse mult doesn't exist]")
        sys.exit()
    
if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description="Hill\'s encryptor and decryptor.")
   
    mutexgr = parser.add_mutually_exclusive_group(required=True)
    mutexgr.add_argument(
            "-t", "--text", 
            help="specified the plaintext which will encrypted", 
            dest="plaintext", 
            type=str
            )
    mutexgr.add_argument(
            "-c", "--cipher", 
            help="specified the ciphertext which will decrypted", 
            dest="ciphertext", 
            type=str
            )
    parser.add_argument(
            "-k", "--key", 
            help="cryptor key", 
            dest="key", 
            required=True
            )
    parser.add_argument(
            "-v", "--version", 
            help="output version information and exit", 
            action="version", 
            version="{} {}".format(appname, appver)
            )

    args = parser.parse_args()
    op = operation(args.plaintext == None) 
    args.key = keyCompletion(args.key)
    checkInput(args.key, args.plaintext, args.ciphertext)

    if op == operation.decode: 
        main(decode(args.ciphertext, args.key))
    else:
        main(encode(args.plaintext, args.key))    
