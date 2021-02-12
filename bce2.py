#!/usr/bin/env python3
"""
Exports bitcoind data to sql-ready plaintext
3rd parties:
- python3-configobj
- python3-kyotocabinet
- python3-base58
- [python3-ujson]
Bundled:
- python3-bitcoinrpc
"""

from bcepy.main2 import main

if __name__ == "__main__":
    main()
