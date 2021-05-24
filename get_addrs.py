#!/usr/bin/env python3
"""
Get blockchain addresses from bitcoind.
"""

import argparse
import datetime
import bcepy.heap as heap
from bcepy.authproxy import AuthServiceProxy as Proxy
from bcepy.utils import load_conf, pk2addr, Timer, eprint

Dup_Blocks = {91722, 91842}  # duplicate 91880, 91812
Interim_Size = 1000


def walk(beg: int, qty: int):
    rpc_connection = Proxy(load_conf(), timeout=300)  # for heavy load
    if qty == 0:
        end = rpc_connection.getblockcount()
    else:
        end = beg + qty
    bk_hash = rpc_connection.getblockhash(beg)
    heap.timer = Timer()
    heap.timer.start()
    bk_no = 0
    # 1. go
    for bk_no in range(beg, end):
        bk = rpc_connection.getblock(bk_hash, 2)
        bk_hash = bk['nextblockhash']
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
        if not ((bk_no+1) % Interim_Size):
            eprint("{}\t{}".format(int((bk_no+1)/1000), heap.timer.now()))
    eprint("{}:\t{}".format(int((bk_no + 1)), heap.timer.now()))


def init_cli():
    """ Handle CLI """
    parser = argparse.ArgumentParser(description='Export addresses.')
    parser.add_argument('-f', '--from', dest='beg', metavar='n', type=int, nargs='?', default=0,
                        help='Bk start from (default=0)')
    parser.add_argument('-n', '--num', metavar='n', type=int, nargs='?', default=0,
                        help='Bk to process (default=all)')
    parser.add_argument('-l', '--log', action='store_true',
                        help='Logfile (default=false)')
    return parser


def main():
    parser = init_cli()
    args = parser.parse_args()
    if args.log:
        heap.Opts.log = True
        heap.logfile = open("%s.log" % datetime.datetime.now().strftime('%y%m%d%H%M%S'), 'wt')
    walk(args.beg, args.num)


if __name__ == '__main__':
    main()
