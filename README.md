# bcepy - BitCoin Export (Python)

Exports BTC blockchain into SQL DB loadable data.

## 1. Requires

- bitcoind
- python3
- python3-configobj
- python3-base58
- python3-kyotocabinet or python3-redis
- python3-ujson (optionaly)

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
- enumerates them using key-value storage
- and exports results in compact text representation, ready to load into SQLn DB.

## 4. Usage

### bce1.py

Counts blocks size, transactions, vouts and vins querying bitcoind like `bitcoin-cli getblock <hash>` (steps 1..2).
Without `-v` option short version ('verbosity=1') of bitcoind response used.
`-v` option uses 'verbosity=2' queries.
This utility is for tests and harware perfomance ratings.
Bitcoind connection a...s are loading from bitcoin.conf as it is required for bitcoin-cli.

### bce2.py

The same as bce1.py (`-m 0|1` option) but generates interim flat text for further conversion(`-m 2` option; steps 1..3).
Next and last step - prepare this interim text and load into PostgreSQL using utils/db_ctl.sh (steps 4..6).
db\_ctl.sh uses .db\_ctl.cfg in the same directory for connecting to SQL DB (see [db\_ctl.cfg sample](doc/db_ctl.cfg.sample)).

## 5. Installation

- [bitcoind](doc/bitcoind.md)
- free space for (2020-09-01):
  - blockchain (~350GB+)
  - interim bce2.py data (~&frac14; blockchain)
  - key-value storage (~&frac14; blockchain)
- this package

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
