# bcepy - *B*it*C*oin *E*xport (*PY*thon version)

Exports BTC blockchain into SQL DB loadable data.

## 1. Explanation

Storing blocks/transactions/addresses in SQL DB with their hashes as primary keys makes DBs extreme huge.
The solution is to use their order numbers.<br/>
This application:
- get blocks from bitcoind
- enumerates objects (bk/tx/address) using key-value storage
- and exports results in compact text representation, ready to load into SQLn DB.

## 2. Requirements

- running bitcoind
- python3
- python3-kyotocabinet or python3-redis
- python3-ujson (optionaly)
- free space for:
  - blockchain (~350GB+ on 2021-02-12)
  - interim bcepy.py data (~&frac14; blockchain)
  - key-value storage (~&frac14; blockchain; tx.kch + addr.kch)

Bundled contribs:

- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc/blob/master/bitcoinrpc/authproxy.py) as [btc/authproxy.py](btc/authproxy.py)
- [python-base58](https://github.com/keis/base58/blob/master/base58/__init__.py) as [btc/base58.py]

## 3. Installation


## 4. Usage

Counts blocks size, transactions, vouts and vins querying bitcoind like `bitcoin-cli getblock <hash>`.<br/>
Without `-v` option short version ('verbosity=1') of bitcoind response used.
`-v` option uses 'verbosity=2' queries.<br/>
This utility is for tests and harware perfomance ratings.<br/>
Bitcoind connection are loading from bitcoin.conf as it is required for bitcoin-cli.

'-c' - you can set simply folder or set k-v type: 'kc:/my/path' for kyotocabinet or 'tk:/my/path' for tkrzw.

### bce2.py

The same as bce1.py (`-m 0|1` option) but generates interim flat text for further conversion(`-m 2` option).<br/>
Options:
 - -m 0 - 

## 5. Results

Plaintext with records:

- `b	id		'datetime'	'hash'`
- `t	id		b.id		hash`
- `i	<t.id	vout		t.id`
- `o	t.id	vout		$		[a.id]`
- `a	id		"addr"		qty`
