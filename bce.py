#!/bin/env python3
"""
Exports bitcoind data to sql/plaintext
3rd parties:
- python3-bitcoinrpc
- python3-kyotocabinet
- python3-base58
"""

from btc.main import main

if __name__ == "__main__":
    main()
