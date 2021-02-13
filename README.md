# bcepy - *B*it*c*oin *e*xport (*py*thon version)

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
- python3-kyotocabinet or python3-tkrzw (optional)

Bundled contribs:

- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc/blob/master/bitcoinrpc/authproxy.py) as [btc/authproxy.py](btc/authproxy.py)
- [python-base58](https://github.com/keis/base58/blob/master/base58/__init__.py) as [btc/base58.py](btc/base58.py)

## 3. Installation

- `git clone` or `rpm -i`.
- setup bitcoind and/or connection to them according to [documentation](doc/bitcoind.md)
- free space for:
  - blockchain (~350GB+ on 2021-01-01)
  - bcepy output data (~&frac14; of blockchain size (if gziped))
  - key-value storage (~&frac14; of blockchain size (tx.* + addr.*))

## 4. Usage

Bitcoind connection are loading from bitcoin.conf as it is required for bitcoin-cli.<br/>
Options (use `-h` for help):
- `-f` *int*: from kiloblock (default 0)
- `-q` *int*: kiloblocks to process (default 1 kbk == 1000 blocks)
- `-l`: write log file (yymmddhhMMss.log)
- `-m` *mode*:
  - `0`: counts blocks (bk), their size and transactions (tx) querying bitcoind like `bitcoin-cli getblock <hash> 1`.
  - `1`: == `0` + vouts and vins.
  - `2`: == `1` + addresses. Uses key-value storage (default in-memory; see `-c`). Quiet without `-o` option (just fills out key-values)
- `-o`: generates text output (`-m 2` only, stdout)
- `-c` *dir*: set file-based key-value storage. Using `kc:` (kyotocabinet) or `tk:` path prefix set exact key-value backend. Ommiting prefix cause trying kyotocabinet then tkrzw then exception if both are absent.

## 5. Results

Plaintext records (tab separated lines):

- `b	id		'datetime'	'hash'` - block
- `t	id		b.id		hash` - transaction
- `i	<t.id	vout		t.id` - vin
- `o	t.id	vout		$		[a.id]` - vout
- `a	id		"addr"		qty` - address
