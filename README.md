# bcepy
Blockchain export (python version)

## Who's who
- bce1.py: shortest version, just walks through bitcoind
- bce2.py: includes bce1 + export to SQL
- bce3.py: splits bitcoind import and processing it

## Prereq
- python3
- python3-base58
- python3-bitcoinrpc
- python3-kyotocabinet | python3-redis

## Usage
1. Run bce (631 Kblocks):
  ```
  python3 bce.py -m 2 -q 631 -l -o | pigz > all.txt.gz
  ```
2. split into parts:

	```
	#!/bin/sh
	SRCFILE = all.txt.gz
	TMPDIR = /mnt/sdb2/tmp
	# 1. blocks (1'):
	unpigz -c $SRCFILE | grep ^b | gawk -F "\t" -v OFS="\t" '{print $2,$3}' | pigz -c > b.txt.gz
	# 2. tx (7/11'):
	unpigz -c $SRCFILE | grep ^t | gawk -F "\t" -v OFS="\t" '{print $2,$3,$4}' | pigz -c > t.txt.gz
	# 3. address (4/6'):
	unpigz -c $SRCFILE | grep ^a | gawk -F "\t" -v OFS="\t" '{print $2,$3,$4}' | pigz -c > a.txt.gz
	# 4. data
	# 4.1. filter vouts (out_tx, out_n, satoshi, addr) (8/13')
	unpigz -c $SRCFILE | grep ^o | gawk -F "\t" -v OFS="\t" '{print $2,$3,$4,$5}' | pigz -c > o.txt.gz
	# 4.2. filter vins (out_tx, out_n, in_tx) (2/8')
	unpigz -c $SRCFILE | grep ^i | gawk -F "\t" -v OFS="\t" '{print $2,$3,$4}' | pigz -c > i.txt.gz
	# 4.3. sort vins by vouts (11/12')
	unpigz -c i.txt.gz | sort -n -k1 -k2 -T $TMPDIR | pigz -c > is.txt.gz
	# 4.4. join vouts | vins (7/13')
	python3 join_io.py o.txt.gz is.txt.gz | pigz -c > d.txt.gz
	```
3. Load into DB:

	```
	#!/bin/sh
	DBNAME=btcdb
	DBUSER=btcuser
	# 1. Prepare: switch indexes off; drop all records; vacuum all
	psql -q -f idx_off.sql $DBNAME $DBUSER
	psql -q -c "TRUNCATE TABLE data, addresses, transactions, blocks;" $DBNAME $DBUSER
	psql -q -c "VACUUM FULL data, addresses, transactions, blocks;" $DBNAME $DBUSER
	# 2. Load data: bk, tx, addresses, data
	unpigz -c b.txt.gz | psql -q -c "COPY blocks (b_id, b_time) FROM STDIN;" $DBNAME $DBUSER
	unpigz -c t.txt.gz | psql -q -c "COPY transactions (t_id, b_id, hash) FROM STDIN;" $DBNAME $DBUSER
	unpigz -c a.txt.gz | psql -q -c "COPY addresses (a_id, a_list, n) FROM STDIN;" $DBNAME $DBUSER
	unpigz -c d.txt.gz | psql -q -c "COPY data (t_out_id, t_out_n, satoshi, a_id, t_in_id) FROM STDIN;" $DBNAME $DBUSER # 3'30"
	# 3. Post: switch indexes on; vacuum all
	psql -q -f idx_on.sql $DBNAME $DBUSER
	```

x. Chk result:
psql -q -c "SELECT SUM(satoshi) AS itogo FROM data WHERE t_in_id IS NULL;" $DBNAME $DBUSER

## RTFM

- [Lost BTCs](https://blog.okcoin.com/2020/05/12/btc-developer-asks-where-are-the-coins/):
  - bitcoind options += "-txindex"
  - bitcoind -reindex
