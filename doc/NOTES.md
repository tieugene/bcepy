# Misc notes
## 200520:
* m2 - pypy3 is wore
## 1. Resources
* [Learn me a bitcoin](https://learnmeabitcoin.com/)
* [bitcoin-core](http://github.com/bitcoin/bitcoin/)
* [libbitcoin](https://github.com/libbitcoin) ([RH specs](https://github.com/AliceWonderMiscreations/libbitcoin-RPM), man fedpkg chain-build)
* [Blockchain API](http://www.blockchain.com/api/blockchain_api)
* [blk* structure](https://en.bitcoin.it/wiki/Bitcoin_Core_0.11_(ch_2):_Data_Storage)
* Python:
  * [python3-bitcoinlib](https://github.com/petertodd/python-bitcoinlib) ([docs](file:///usr/share/doc/python3-bitcoinlib/html/index.html))
  * [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc)
* direct parsers:
  * [fast-dat-parser](https://github.com/bitcoinjs/fast-dat-parser) - C++
  * [bitcoin-blockchain-parser](https://github.com/alecalve/python-bitcoin-blockchain-parser) - Py
  * [bitcoin-blk-file-reader](https://github.com/mrqc/bitcoin-blk-file-reader) - Py
  * [bit](https://github.com/ofek/bit/) - Py
  * [PyBC](https://github.com/garethjns/PyBC) - Py
  * [blockchain-parser](https://github.com/ragestack/blockchain-parser) - handmade of [habr user](http://habr.com/ru/post/482978/)

## 2. Order
1. Берем [первый попавшийся](https://rutracker.org/forum/viewtopic.php?t=5520053) blockchain
1. натравливаем bitcoind
1. ждем-с
1. вынимаем данные в SQL
1. загружаем SQL в базу

## 3. ToDo
* autovaluum off
* split UPDATEs by X lines: ```sed '0~X i COMMIT;\nBEGIN;'```
* PK:
  * bk: int (32)
  * tx: int64 = bk << 32 + tx_no
  * data: txno & voutno
  * address: last 8 bytes of deBase58(address); check it!
* Uniq:
  * transaction.hash
  * data.txout_id.txout_n.txin.id
  * address.a_list
* Index:
  * ...
* address: json: ["xxx"] => "xxx"
* ~~bitcoin += lib (like libbitcoinconsensus)~~
* find ~~key-value~~ key-recno (key=32B/24B)
* convert address (34c) to bytes (25|20)
* convert pubkey to address ([RTFM](http://gobittest.appspot.com/Address)):

```python
def pk2addr(pk: str[130]) -> str:
  # use px.hex() to control
  import haslib
  p1 = bytes.fromhex(pk)
  p2 = hashlib.sha256(p1).digest()
  p3 = hashlib.new('ripemd160', p2).digest()
  p4 = b'\x00' + p3
  p5 = hashlib.sha256(p4).digest()
  p6 = hashlib.sha256(p5).digest()
  p7 = p6[:4]
  p8 = p4+p7		# concat
  p9 = base58.b58encode(p8)
  return(p9)
```
or:

```python
def short (pk: bytes):
  """ Function doc """
  p4 = b'\x00' + hashlib.new('ripemd160', hashlib.sha256(pk).digest()).digest()
  return(base58.b58encode(p4+hashlib.sha256(hashlib.sha256(p4).digest()).digest()[:4]))
```

### Idea

* use buitin LevelDB files
* bitoind += getblockshort:ineed.json
* bitcoin-core = bitcoin-libs + util/qt/d
* connect via [socket](https://github.com/bitcoin/bitcoin/pull/9919) - err
* простейший фильтр json для getblock
* -blocknotify=cmd - exec cmd on adding new block
* ~~pypy3~~ (no advices)

```
ALTER TABLE transactions DROP CONSTRAINT transactions_pkey;
ALTER TABLE transactions ADD CONSTRAINT transactions_pkey PRIMARY KEY (t_id);
```

## misc
* с адресами [не всё так просто](https://en.bitcoin.it/wiki/Address)
* в данный момент достаточно номер кошелька, баланс, день, для аналитики этого хватит
* Address: 26..35 (really 42) chars
* distributing:
	- bitcoind
	- [key-value server (redis)]
	- PGSQL server (1 x core)
	- my script (1 x core)
* 1 блок = 1 coinbase tx; coinbase tx: 1 x vin, 1 x voit
	
## 3. Словаме
* в каждом блоке - x транзакций
* одна из них  (и только  одна) - coinbase; в ней только 1 x vin, 1 x vout
* нас от блока интересует только время (?)
* в каждой транзакции: txid, входы (vint) и выходы(vout)
* vin:
  * если coinbase есть, то это генерация => ...
  * если нет, то нужны:
  	* txid - транзакции vout (откуда?)
  	* vout - N в vout (?)
* voit:
  - pubkey => ?
  - pubkeyhash => address
  - multisig => addresses[]

## 4. QA

* Q: куда деваются vout без addresses?
* A: see pubkey
* A: и куда с multiaddresses?
* A: ? штоле coinbase уходят на адрес через скрипт?

## 5. BCXExplorer recomendations:
- use block['nextblockhash'] for traverse
- use block['height'] as block.b_id
- addresses.a_list:str = ' '.join(addresses[])
- add indeces (e.g. *n)
- add UNIQUE t_out_id + t_out_n
- transactions.t_in_n нинужен
- constraints:
  - tx=>bk: on delete
  - don't update t_in_id WHERE t_in_id is NOT NULL
- use dict() hash:id, address:id


## 6. bitcoin.conf
- server=1
- rpcuser=...
- rpcpassword=...
- blocksonly=1
- ?noconnect=1
- listen=0
- listenonion=0
- disablewallet=1
- datacarrier=0
- whitelistrelay=0
- ?maxconnections=0
- # 'Using at most 125 automatic connections'

## 7. vout
* Pay to public key hash (P2PKH):
  - type: pubkeyhash
  - addresses: [1]
* Multisig:
  - type: pubkeyhash
  - addresses: [+]
* Pay to script hash (P2SH):
  - type: scripthash
  - addresses: [+]
* Pubkey:
  - type: pubkey
  - hex (67 bytes):
    - 1 - datalen (x41 = 65)
    - 65 - pubkey
    - 1 - opcode (xAC = OP_CHECKSIG)
  - asm (65 bytes): [Public ECDSA Key](http://gobittest.appspot.com/Address)
  - addresses: absent
* Null
  - type: nulldata
  - value: 0
  - addresses: absent

## 8. Example
tx №1: -> 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa -> 25 bytes:
1 - ver
20 - pubkeyhash (RIPEMD15(SHA256(pubkey)))
4 - crc
vout.asm = %130x = 65 bytes = 1xSHA256

## 9. Stat:
### blk*.dat:

* 0000? - 76", 10 files, 1.25GB, 180048 bk, ... tx
* 000?? - 100 files, 12.5GB, ... bk, ... tx
* 00??? - 1000 files, 125GB, ... bk, ... tx
* 0[0-1]??? - 2000 files, 249GB, ... bk, ... tx
* .02049 - 2050 files, 255GB, ... bk, ... tx

## x. misc
* [array perfomance](https://stackoverflow.com/questions/537086/reserve-memory-for-list-in-python)
* [array perfomance 2](https://stackoverflow.com/questions/311775/python-create-a-list-with-initial-capacity/24173567)

## 200505
Speed up btc.py:
- get all blocks and tx (getblock w/o 2) => bk+tx ok
- get all tx

getmempoolinfo
getrawmempool ( verbose )
gettxout "txid" n ( include_mempool )
gettxoutproof ["txid",...] ( "blockhash" )
gettxoutsetinfo

1st block: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
1st tx: 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b

- get all actual blocks: [bulk] getblockhash 0..629xxx