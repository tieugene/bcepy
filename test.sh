#!/bin/sh
./bce.py -m 2 -q 250 -l -o | pigz -c > 250.txt.gz
