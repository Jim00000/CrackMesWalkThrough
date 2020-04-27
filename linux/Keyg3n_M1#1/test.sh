#!/bin/sh
for _ in $(seq 1 100)
do
    python3 keygen.py | ./keygen.bin
done