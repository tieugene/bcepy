#!/bin/env python3
"""
Export bitcoind data to gziped jsons.
3rd parties: None

Usage:
- [-f, -q, -l]: count txs using short bitcoind reply
- -v: count tx, vins, vouts using long bitcoind replies
- -v -o: + save prepared long replies

time (kbk, macbook, wifi):
1   4
100 718 (60=>396MB)
"""

from btc.main31 import main

if __name__ == "__main__":
    main()
