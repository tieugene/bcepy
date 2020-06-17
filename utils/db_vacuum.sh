#!/bin/sh
# Vacuum whole of db
psql -q -c "VACUUM FULL data, addresses, transactions, blocks;" btcdb btcuser
sudo du -sm /mnt/shares/pgsql