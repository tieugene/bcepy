# Bitcoind

Setting up bitcoind server and client.

- distro: Fedora 33
- blockchain path: $BCPATH
- bitcoind rpc user: $RPCUSER
- bitcoind rpc password: $RPCPASS
- bitcoind host IP: $BTCDIP

## 1. Server

### 1.1. Install packages:

```bash
sudo dnf install bitcoin-server
```

### 1.2. Configure:

- /etc/sysconfig/bitcoin:

```diff
-DATA_DIR="/var/lib/bitcoin"
+DATA_DIR="/mnt/my_big_and_fastest_drive/bitcoin"
+# next line is optional
+OPTIONS="-txindex=1"
```

- /etc/bitcoin/bitcoin.conf:

```
datadir=$BCPATH
rpcuser=$RPCUSER
rpcpassword=$RPCPASS
server=1
disablewallet=1
listen=0
listenonion=0
blocksonly=1
rpcservertimeout=1200
datacarrier=0
whitelistrelay=0
# rpcbind=0.0.0.0           # optional
# rpcallowip=127.0.0.1      # optional
# rpcallowip=192.168.0.0.24 # optional
```

- mk space:

```bash
sudo mkdir -p $BCPATH
sudo chown -R bitcoin:bitcoin $BCPATH
```

### 1.3. Run:

```bash
sudo systemctl enable --now bitcoin
```

### 1.4. Check

```bash
sudo tail -f /var/log/bitcoin/debug.log
```

## 2. Client

### 2.1. Install packages

```bash
sudo dnf install bitcoin-utils
```

### 2.2. Configure:

~/.bitcoin/bitcoin.conf:
(_)

```
rpcuser=$RPCUSER
rpcpassword=$RPCUSER
# next line optional
rpcconnect=$BTCDIP
```

### 2.3. Check:

```bash
bitcoin-cli help
bitcoin-cli getblockcount
bitcoin-cli getblock `bitcoin-cli getblockhash 0`
```

## Misc
- [Lost BTCs](https://blog.okcoin.com/2020/05/12/btc-developer-asks-where-are-the-coins/):
  - bitcoind options += "-txindex"
  - bitcoind -reindex
