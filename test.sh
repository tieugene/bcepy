#!/bin/sh
./bce.py -m 2 -q 10 -l -o | pigz -c > 10.txt.gz
