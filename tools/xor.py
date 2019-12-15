#!/usr/bin/env python3
# coding: utf-8

keys = [
b'\x61\x78\x64\x61\x6f\x65\x72\x61\x64\x73\x73\x61\x64\x73\x71\x78\x00',
#b'\x19\x64\x12\x09\x1c\x61\x0e\x1d\x16\x00\x0b\x16\x01\x00\x00\x00\x02',
]

import os
import sys

def main():
	with open(sys.argv[1], 'rb') as f:
		while True:
			for key in keys:
				dbuf = f.read(0x400)
				if len(dbuf) == 0:
					return
				
				kbuf = key[:]
				while len(kbuf) < len(dbuf):
					kbuf += key
				
				sys.stdout.buffer.write(
					bytes(a ^ b for a, b in zip(dbuf, kbuf)))

main()
