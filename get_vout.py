#!/usr/bin/env python3
"""
Get blockchain vout
External check: https://blockchain.info/rawtx/$tx_hash
"""

import json
import sys

import requests

from btc.authproxy import AuthServiceProxy as Proxy
from btc.utils import load_conf


def walk(bk_no: int, tx_no: int, vout_no: int):
    rpc_connection = Proxy(load_conf(), timeout=300)
    bk_hash = rpc_connection.getblockhash(bk_no)
    bk = rpc_connection.getblock(bk_hash, 2)
    if bk:
        txs = bk['tx']
        if len(txs) > tx_no:
            tx = txs[tx_no]
            txid = tx['txid']
            vouts = tx['vout']
            if vout_no < len(vouts):
                vout = vouts[vout_no]
                print("My:")
                print("\tS:\t{}".format(vout['hex']))
                print("\tT:\t{}".format(vout['type']))
                if 'addresses' in vout:
                    print("\tA:\t{}".format(json.dumps(vout['hex'])))
                # ext: ['out']['script, type, addr
                r = requests.get('https://blockchain.info/rawtx/')
                print(r.status_code)
                print(r.json())

def main():
    argv = sys.argv
    argc = len(argv)
    if argc != 4 \
            or not argv[1].isdigit() \
            or not argv[2].isdigit() \
            or not argv[3].isdigit():
        print("Get tx/vout.\nUsage: {} <bk #> <tx #> [<vout #>]".format(argv[0]))
    else:
        walk(int(argv[1]), int(argv[2]), int(argv[3]))


if __name__ == '__main__':
    main()
