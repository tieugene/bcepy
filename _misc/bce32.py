#!/usr/bin/env python3
"""
- bce3?.py: 2-part version of bce2:
  - bce31.py: get data from bitcoin into interim json files
  - bce32.py: export bce31.py results into interim txt files

Process bitcoind gziped jsons into SQL-ready data.
3rd parties:
- python3-kyotocabinet
- [python3-ujson]
"""
from bcepy.main32 import main

if __name__ == "__main__":
    main()
