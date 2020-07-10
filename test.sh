#!/bin/sh
./bce.py -m 2 -q 100 -l -o | pigz -c > 100.txt.gz
