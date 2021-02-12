# bcepy - BitCoin Export (Python)

Exports BTC blockchain into SQL DB loadable data.

## 1. Requires

- running bitcoind
- python3
- python3-kyotocabinet or python3-redis
- python3-ujson (optionaly)
- free space for:
  - blockchain (~350GB+ on 2021-02-12)
  - interim bce2.py data (~&frac14; blockchain)
  - key-value storage (~&frac14; blockchain)

Conrib:

- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc/blob/master/bitcoinrpc/authproxy.py) as [btc/authproxy.py](btc/authproxy.py)
- [python-base58](https://github.com/keis/base58/blob/master/base58/__init__.py) as [btc/base58.py]

## 2. Who's who

- bce1.py: walks through bitcoind and count txs, vouts, vins
- bce2.py: bce1 + export to SQL
- bce3?.py: 2-part version of bce2:
  - bce31.py: get data from bitcoin into interim json files
  - bce32.py: export bce31.py results into interim txt files

## 3. Explanation

Storing blocks/transactions/addresses in SQL DB with their hashes as primary keys makes DBs extreme huge.
The solution is to use block/tx/address order numbers.
This application:
- get blocks from bitcoind
- enumerates objects (bk/tx/address) using key-value storage
- and exports results in compact text representation, ready to load into SQLn DB.

## 4. Usage

### bce1.py

Counts blocks size, transactions, vouts and vins querying bitcoind like `bitcoin-cli getblock <hash>`.<br/>
Without `-v` option short version ('verbosity=1') of bitcoind response used.
`-v` option uses 'verbosity=2' queries.<br/>
This utility is for tests and harware perfomance ratings.<br/>
Bitcoind connection are loading from bitcoin.conf as it is required for bitcoin-cli.

### bce2.py

The same as bce1.py (`-m 0|1` option) but generates interim flat text for further conversion(`-m 2` option).<br/>
Options:
 - -m 0 - 

## 5. Installation

## Input
- block location file ({fileno:uint32, offset:uint32) for each block}
- blockchain directory (with blkXXXXX.dat files)

## Output

Plaintext with records:

- `b	id		'datetime'	'hash'`
- `t	id		b.id		hash`
- `i	<t.id	vout		t.id`
- `o	t.id	vout		$		[a.id]`
- `a	id		"addr"		qty`
