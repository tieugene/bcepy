#!/bin/env python3
"""
Get all blockchain addresses
"""

from btc.authproxy import AuthServiceProxy as Proxy
from btc.utils import load_conf, eprint, Timer

Dup_Blocks = {91722, 91812}  # duplicate 91880, 91842


def walk():
    rpc_connection = Proxy(load_conf(), timeout=300)  # for heavy load
    bk_hash = rpc_connection.getblockhash(0)
    bk_count = rpc_connection.getblockcount()
    # 1. go
    for bk_no in range(0, 5):
        bk = rpc_connection.getblock(bk_hash, 2)
        if bk_no in Dup_Blocks:
            continue
        tx_no = 0
        for tx in bk['tx']:
            for vout in tx['vout']:
                vout_no = vout['n']
                addrs = vout.get('addresses', None)
                pfx = "{}\t{}\t{}\t{}".format(bk_no, tx_no, vout_no, vout['scriptPubKey']['type'])
                if addrs:
                    print("{}\t{}".format(pfx, ','.join(addrs)))
                else:
                    print(pfx)
            tx_no += 1
        bk_hash = block['nextblockhash']


if __name__ == '__main__':
    walk()
