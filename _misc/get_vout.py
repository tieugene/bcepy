#!/usr/bin/env python3
"""
Get blockchain vout
External check: https://blockchain.info/rawtx/$tx_hash
"""

import json
import sys

from urllib import request

from bcepy.authproxy import AuthServiceProxy as Proxy
from bcepy.utils import load_conf


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
                script = vouts[vout_no]['scriptPubKey']
                # print(json.dumps(script, indent=1))
                print("S: {}".format(script['hex']))
                print("T: {}".format(script['type']))
                addrs = script.get('addresses', None)
                if addrs:
                    print("A: {}".format(','.join(addrs)))
            # ext: ['out']['script, type, addr
            # extra source
            print("E: ", end='')
            with request.urlopen('https://blockchain.info/rawtx/' + txid) as f:
                s = f.read().decode('utf-8')
                tx = json.loads(s)
                vout = tx['out'][vout_no]
                # print(json.dumps(vout, indent=1))
                # print("\tS:\t{}".format(vout['script']))
                # print("\tT:\t{}".format(vout['type']))
                print(vout.get('addr', '---'), end='')
            print()


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
