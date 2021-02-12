#!/usr/bin/env python3
"""
Exports bitcoind data to sql-ready plaintext
3rd parties:
- python3-kyotocabinet
- [python3-ujson]
Bundled:
- python3-bitcoinrpc
- python3-base58
"""

from bcepy import main

if __name__ == "__main__":
    main()
