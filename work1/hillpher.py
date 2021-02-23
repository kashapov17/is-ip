#!/usr/bin/python

import sys
import argparse
import string
import numpy as np
from enum import Enum

appname = "hillpher"
appver = "0.1"

alph = string.digits+string.ascii_letters+",.() "
keyPower = 32

class operation(Enum):
    encode = 0
    decode = 1

def main(inputtext, result, op):
    if op == operation.encode:
        print("The \"{}\" has been encrypted as \"{}\"".format(inputtext,result))
    elif op == operation.decode:
        print("The \"{}\" has been decrypted as \"{}\"".format(inputtext,result))
    return 0

def keyCompletion(key):
    for i in range(1, keyPower):
        keyLenght = len(key)
        if keyLenght <= i**2:
            offset = alph.find('a')
            for j in range(offset, i**2 - keyLenght + offset):
                key += alph[j]
            break
    return key

def createMatrixFromStr(string, order):
    m = list(string)
    for i,l in enumerate(m):
        m[i] = int(alph.find(l))
    m = np.array(m, dtype=int)
    if order != 1:
        m = m.reshape(order, order)
    return m

def createStrFromMatrix(m):
    string = ""
    for x in m:
        string+=alph[x]
    return string

def encode(plaintext, key):
    keyPower = int(len(key)**0.5)
    while(len(plaintext) % keyPower):
        plaintext += " "
    
    keyMatrix = createMatrixFromStr(key, keyPower)
   
    ciphertext = ""
    for i in range(int(len(plaintext) / keyPower)):
        ciphertext += createStrFromMatrix(
                np.dot(createMatrixFromStr(
                    plaintext[i*2:i*2+keyPower], 1), keyMatrix) % len(alph)
                ) 
    
    return ciphertext

def decode(ciphertext, key):
    print()

def isAlphConsistOf(string):
    if string != None:
        for l in string:
            if alph.find(l) == -1:
                print("Error: symbol \'{}\' not contained in the alphabet".format(l))
                print("Allowable set of symbols: {}".format(list(alph)))
                sys.exit()

if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description='Hill\'s encryptor and decryptor.')
   
    mutexgr = parser.add_mutually_exclusive_group(required=True)
    mutexgr.add_argument(
            "-t", "--text", 
            help="specified the plaintext witch will encrypted", 
            dest="plaintext", 
            type=str
            )
    mutexgr.add_argument(
            "-c", "--cipher", 
            help="specified the ciphertext witch will decrypted", 
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
            action='version', 
            version='{} {}'.format(appname, appver)
            )

    args = parser.parse_args()
    op = operation(args.plaintext == None) 

    isAlphConsistOf(args.plaintext)
    isAlphConsistOf(args.ciphertext)
    isAlphConsistOf(args.key)
   
    args.key = keyCompletion(args.key)

    if op == decode: 
        main(args.ciphertext, decode(args.ciphertext, args.key), op)
    else:
        main(args.plaintext, encode(args.plaintext, args.key), op)
