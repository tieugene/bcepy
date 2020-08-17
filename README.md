# bcepy - BitCoin Export (Python)

Exports BTC blockchain into PostgreSQL.

## Requires

- bitcoind
- postgresql-server
- python3
- python3-configobj
- python3-base58
- python3-kyotocabinet or python3-redis
- python3-ujson (optionaly)

## Who's who

- bce1.py: walks through bitcoind and count txs, vouts, vins
- bce2.py: bce1 + export to SQL
- bce3?.py: 2-part version of bce2:
  - bce31.py: get data from bitcoin into interim json files
  - bce32.py: export bce31.py results into interim txt files
- utils/:
  - db_ctl.sh: converts bce*.py results into SQL loadable data
  - join\_io.py: used by db_ctl.sh to merge transaction vouts and vins

## Explanation

Storing blocks/transactions/addresses hashes in data table dircectly makes it extreme huge.
The solution is to use block/tx/address order numbers (#).
Target PostgreSQL DB consists from tables (see [db structure](doc/db.svg)):

1. blocks (#, datetime)
2. transactions (#, hash)
3. data (transaction vouts and vins)
4. addresses (#, hash)

Process of bitcoind=>PostgreSQL conversion goes through next steps:

1. Get data from bitcoind as json responses.
2. Load into inmemory structures
3. Calculate block/tx/address #s using external key-value storage
4. Merge vouts and vins
5. Export data into flat text ready to load into SQL DB
6. Load those data into PostreSQL using `COPY` statements

## Usage

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

## Installation

- [bitcoind](doc/bitcoind.md)
- [PostgreSQL](doc/postgresql.md)
- [Redis](doc/redis.md) (optional)
- free space for (2020-09-01):
  - blockchain (~350GB+)
  - PostgreSQL database (~&frac12; blockchain)
  - interim bce2.py data (~&frac14; blockchain)
  - key-value storage (~&frac14; blockchain)
  - temporary `sort` files (&infin;)
- this package
