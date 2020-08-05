# Bitcoind

- distro: Fedora 32
- blockchain path: $BCPATH
- bitcoind rpc user: $RPCUSER
- bitcoind rpc password: $RPCPASS

## 1. install packages

```bash
sudo dnf localinstall bitcoin-server bitcoin-utils
```

## 2. configure server

- /etc/sysconfig/bitcoin:

```diff
+OPTIONS="-txindex=1"
-DATA_DIR="/var/lib/bitcoin"
+DATA_DIR="/mnt/sdb2/bitcoin"
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

- run server:

```bash
sudo systemctl enable --now bitcoin
```

## 3. configure client

~/.bitcoin/bitcoin.conf

```
rpcuser=$RPCUSER
rpcpassword=$RPCUSER
```

- check client:

```bash
bitcoin-cli help
```

## Misc
- [Lost BTCs](https://blog.okcoin.com/2020/05/12/btc-developer-asks-where-are-the-coins/):
  - bitcoind options += "-txindex"
  - bitcoind -reindex
