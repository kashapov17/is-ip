#!/usr/bin/python

import sys
import argparse
import string
import numpy

appname = "hillpher"
appver = "0.1" 

alph = string.digits + string.ascii_letters + ",.() "

def main(result):
    print(result)
    return 0

def encode(plaintext, key):
    print("Text encoding...")

    return encodedtext 

def decode(ciphertext, key):
    print("Chipher decoding...")
    return decodedtext

def isAlphConsistOf(string):
    if string != None:
        for l in string:
            if alph.find(l) == -1:
                print("Error: symbol \'{}\' not contained in the alphabet".format(l))
                print("Allowable set of symbols: {}".format(list(alph)))
                sys.exit()

if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description='Hill encryptor and decryptor.')
   
    mutexgr = parser.add_mutually_exclusive_group(required=True)
    mutexgr.add_argument("-t", "--text", 
           help="specified the plaintext which will encrypted", dest="plaintext", type=str, default=sys.stdin)
    mutexgr.add_argument("-c", "--cipher", 
           help="specified the ciphertext which will decrypted", dest="ciphertext", type=str, default=sys.stdin)
   
    parser.add_argument("-k", "--key", 
            help="cryptor key", dest="key", required=True)
    parser.add_argument("-v", "--version", 
            help="output version information and exit", action='version', 
            version='{} {}'.format(appname, appver))

    args = parser.parse_args()
    decode_needed = (args.plaintext == None)
    print((vars(args)))
    print(decode_needed)

    isAlphConsistOf(args.plaintext)
    isAlphConsistOf(args.ciphertext)
    isAlphConsistOf(args.key)
    
    if decode_needed:
        main(decode(args.ciphertext, args.key))
    else:
        main(encode(args.plaintext, args.key))
