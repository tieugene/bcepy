#!/bin/env python3
# converts string pubkey into address
# ~8k pubkeys/s @ P4-3.0

import sys, hashlib, base58

def short (pk: bytes):
	""" Function doc """
	p4 = b'\x00' + hashlib.new('ripemd160', hashlib.sha256(pk).digest()).digest()
	return(base58.b58encode(p4+hashlib.sha256(hashlib.sha256(p4).digest()).digest()[:4]))

def main (pk: bytes) -> bytes:
	"""
	Function doc.
	RTFM: http://gobittest.appspot.com/Address
	use px.hex() to control
	"""
	p2 = hashlib.sha256(pk).digest()
	p3 = hashlib.new('ripemd160', p2).digest()
	p4 = b'\x00' + p3	# 0 == Main Network
	p5 = hashlib.sha256(p4).digest()
	p6 = hashlib.sha256(p5).digest()
	p7 = p6[:4]
	p8 = p4+p7
	p9 = base58.b58encode(p8)
	return(p9)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: %s <hex>" % sys.argv[0])
	else:
		b = bytes.fromhex(sys.argv[1])
		#s = main(b)
		print(short(b))
