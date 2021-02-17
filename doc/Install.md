# Install

## Requirements

- running bitcoind
- python3
- python3-kyotocabinet or python3-tkrzw (optional)

Bundled contribs:

- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc/blob/master/bitcoinrpc/authproxy.py) as [btc/authproxy.py](btc/authproxy.py)
- [python-base58](https://github.com/keis/base58/blob/master/base58/__init__.py) as [btc/base58.py](btc/base58.py)

## Installation

- `git clone` or `rpm -i`.
- setup bitcoind and/or connection to them according to [documentation](doc/bitcoind.md)
- free space for:
  - blockchain (~350GB+ on 2021-01-01)
  - bcepy output data (~&frac14; of blockchain size (if gziped))
  - key-value storage (~&frac14; of blockchain size (tx.* + addr.*))
