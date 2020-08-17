# Redis

## Install

```bash
sudo dnf install redis
```

## Configure

- /etc/redis.conf:

```diff
-# unixsocket /tmp/redis.sock
-# unixsocketperm 0700
+unixsocket /tmp/redis.sock
+unixsocketperm 0755
-databases 16
+databases 2
-dir /var/lib/redis
+dir /mnt/sdb2/btc/redis
```

- data dir:

```bash
sudo mkdir -p /mnt/sdb2/btc/redis
sudo chown -R redis:redis /mnt/sdb2/btc/redis
sudo chmod 0777 /mnt/sdb2/btc/redis
```


## Go

```bash
sudo systemctl enable --now redis
```
