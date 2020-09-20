#!/usr/bin/env python3
"""
Get all blockchain addresses
"""

import sys
import btc.heap as heap
from btc.authproxy import AuthServiceProxy as Proxy
from btc.utils import load_conf, pk2addr, Timer, eprint

Dup_Blocks = {91722, 91812}  # duplicate 91880, 91842
Interim_Size = 1000


def walk(qty: int = 0):
    rpc_connection = Proxy(load_conf(), timeout=300)  # for heavy load
    bk_hash = rpc_connection.getblockhash(0)
    if qty == 0:
        qty = rpc_connection.getblockcount()
    heap.timer = Timer()
    heap.timer.start()
    # 1. go
    for bk_no in range(0, qty):
        bk = rpc_connection.getblock(bk_hash, 2)
        if bk_no in Dup_Blocks:
            continue
        tx_no = 0
        for tx in bk['tx']:
            for vout in tx['vout']:
                vout_no = vout['n']
                spk = vout['scriptPubKey']
                spk_type = spk['type']
                if spk_type == 'pubkey':
                    addr_l = [pk2addr(spk['asm'].split(' ')[0])]
                else:
                    addr_l = spk.get('addresses', None)

                pfx = "{}\t{}\t{}\t{}".format(bk_no, tx_no, vout_no, spk_type)
                if addr_l:
                    print("{}\t{}".format(pfx, ','.join(addr_l)))
                else:
                    print(pfx)
            tx_no += 1
        bk_hash = bk['nextblockhash']
        if not ((bk_no+1) % Interim_Size):
            eprint("{}\t{}".format(int((bk_no+1)/1000), heap.timer.now()))
    eprint("{}:\t{}".format(int((bk_no + 1)), heap.timer.now()))


if __name__ == '__main__':
    end = 0
    if len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            end = int(sys.argv[1])
        else:
            print("Usage: {} [qty[=all]".format(sys.argv[0]))
            exit()
    walk(end)
