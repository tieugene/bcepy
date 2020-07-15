#!/bin/sh
./bce.py -m 2 -q 100 -c /mnt/sdb2/kv -l -o | pigz -c > 100.txt.gz
