#!/usr/bin/env python3
"""
Process bitcoind gziped jsons into SQL-ready data.
3rd parties:
- python3-kyotocabinet
- python3-base58
- [python3-ujson]
"""
from bcepy.main32 import main

if __name__ == "__main__":
    main()
