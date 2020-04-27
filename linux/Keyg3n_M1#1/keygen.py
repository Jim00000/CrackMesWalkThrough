#!/usr/bin/python3
"""keygen.py

This script keygens for keygen.bin program (Keyg3n_M1#1)
Command example : python3 keygen.py [-v]
Author : Jim00000
"""

import argparse
import logging
import random


def randomlyPickPrintableChar(lowerbound: int = 33, upperbound: int = 126):
    pchar = random.randint(lowerbound, upperbound)
    return pchar


def keygen(args) -> [str, bool]:
    """
    The rule of keygen.bin program (Keyg3n_M1#1) is as following :

    1. key length (keylen) rule : 8 <= keylen <= 10
    2. The sum of each bytes that key >= 999

    """
    logging.info(
        "Welcome to use key generator for keygen.bin program (Keyg3n_M1#1)")

    keylen = random.randint(8, 10)
    logging.info("Key length = %d", keylen)
    key = bytearray()
    bytesum = 0
    minsize = 1000

    for step in range(keylen):
        logging.debug("Step %d", step)
        average = (minsize - bytesum) / (keylen - step)
        logging.debug("Average : %f", average)
        if step == keylen - 1:
            if bytesum < minsize:
                pchar = randomlyPickPrintableChar(int(minsize - bytesum))
            else:
                pchar = randomlyPickPrintableChar()
        else:
            pchar = randomlyPickPrintableChar()
            while (minsize - bytesum - pchar) / (keylen - step - 1) >= 126.0:
                pchar = randomlyPickPrintableChar(int(average))
                average = int(average) + 1 if int(average) <= 126 else 126
        bytesum += pchar
        key.append(pchar)
    # shuffle the key
    random.shuffle(key)
    keystring = key.decode("ascii")
    logging.info("key : %s", keystring)
    return keystring, True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="give more detailed information", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        format='[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.NOTSET if args.verbose else logging.ERROR)
    success = False
    while not success:
        [key, success] = keygen(args)
    # output to stdout
    print(key)
