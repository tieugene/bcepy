#!/usr/bin/env python3
"""
- bce3?.py: 2-part version of bce2:
  - bce31.py: get data from bitcoin into interim json files
  - bce32.py: export bce31.py results into interim txt files

Export bitcoind data to gziped jsons.

Usage:
- [-f, -q, -l]: count txs using short bitcoind reply
- -v: count tx, vins, vouts using long bitcoind replies
- -v -o: + save prepared long replies

time (kbk, macbook, wifi):
1   4
100 718 (60=>396MB)
"""

from bcepy.main31 import main

if __name__ == "__main__":
    main()
