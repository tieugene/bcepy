#!/bin/sh
# Clean whole of db
psql -q -c "TRUNCATE TABLE data, addresses, transactions, blocks;" btcdb btcuser
sudo du -sm /mnt/shares/pgsql