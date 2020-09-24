#!/usr/bin/env python3
"""
Get blockchain item: tx [and vout]
"""

import json
import sys

from btc.authproxy import AuthServiceProxy as Proxy
from btc.utils import load_conf


def walk(bk_no: int, tx_no: int, vout_no: int = None):
    rpc_connection = Proxy(load_conf(), timeout=300)
    bk_hash = rpc_connection.getblockhash(bk_no)
    bk = rpc_connection.getblock(bk_hash, 2)
    if bk:
        txs = bk['tx']
        if len(txs) > tx_no:
            tx = txs[tx_no]
            if (vout_no is None):
                print(json.dumps(tx, indent=1))
            else:
                vouts = tx['vout']
                if vout_no < len(vouts):
                    print(json.dumps(vouts[vout_no], indent=1))

def main():
    argv = sys.argv
    argc = len(argv)
    if argc < 3 \
            or argc > 4 \
            or not argv[1].isdigit() \
            or not argv[2].isdigit() \
            or (argc == 4 and not argv[3].isdigit()):
        print("Get tx/vout.\nUsage: {} <bk #> <tx #> [<vout #>]".format(argv[0]))
    else:
        walk(int(argv[1]), int(argv[2]), int(argv[3]) if argc == 4 else None)


if __name__ == '__main__':
    main()
