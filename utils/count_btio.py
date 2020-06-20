#!/bin/env python3
"""
Counts all blocks and transactions
3rd parties:
- python3-bitcoinrpc
"""

import sys
import argparse
import datetime
import time

from authproxy import AuthServiceProxy

Dup_Blocks = {91722, 91812}  # duplicate 91880, 91842
Bulk_Size = 1000
Interim_Size = 1000
logfile = None
tpl = (
    (
        "Bk\tSize\tTx\tTime",
        "===\t=======\t=======\t=====",
        "%03d\t%d\t%d\t%d"
    ),
    (
        "Bk\tSize\tTx\tIn\tOut\tTime",
        "===\t=======\t=======\t=======\t=======\t=====",
        "%03d\t%d\t%d\t%d\t%d\t%d"
    )
)

def eprint(s: str):
    global logfile
    print(s, file=sys.stderr)
    if logfile:
        print(s, file=logfile)
        logfile.flush()


def walk(kbeg: int, kty: int, v: bool):
    """
    Main loop
    @param kbeg: 1st Kblock
    @param kty: Kblocks to process
    """
    # 0. prepare
    bk_no = kbeg
    bk_to = bk_no + (kty * Bulk_Size)
    size = 0
    txs = 0
    ins = 0
    outs = 0
    rpc_connection = AuthServiceProxy("http://login:password@127.0.0.1:8332", timeout=300)  # for heavy load
    bk_hash = rpc_connection.getblockhash(bk_no)
    eprint("%s\n%s" % (tpl[v][0], tpl[v][1]))
    # 1. go
    t0 = time.time()
    while bk_no < bk_to:
        bk = rpc_connection.getblock(bk_hash, 1 + v)
        # if int(bk['height']) not in Dup_Blocks:
        size += bk['size']
        txs += bk['nTx']
        if v:
            for tx in bk['tx']:
                ins += len(tx['vin'])
                outs += len(tx['vout'])
        bk_no += 1
        if not (bk_no % Interim_Size):
            if not v:
                res = (bk_no // Bulk_Size, size, txs, int(time.time() - t0))
            else:
                res = (bk_no // Bulk_Size, size, txs, ins, outs, int(time.time() - t0))
            eprint(tpl[v][2] % res)
        bk_hash = bk['nextblockhash']
    # 2. Summary
    eprint(tpl[v][1])
    if not v:
        res = (bk_no // Bulk_Size, size, txs, int(time.time() - t0))
    else:
        res = (bk_no // Bulk_Size, size, txs, ins, outs, int(time.time() - t0))
    eprint(tpl[v][2] % res)


def init_cli():
    """ Handle CLI """
    parser = argparse.ArgumentParser(description='Process blockchain.')
    parser.add_argument('-f', '--from', dest='beg', metavar='n', type=int, nargs='?', default=0,
                        help='kBk start from (default=0)')
    parser.add_argument('-q', '--qty', metavar='n', type=int, nargs='?', default=1, help='kBk to process (default=1)')
    parser.add_argument('-l', '--log', action='store_true', help='Logfile (default=false)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose (w/ vins and vouts, default=false)')
    return parser


def main():
    """
    CLI commands/options handler.
    """
    global logfile
    parser = init_cli()
    args = parser.parse_args()
    if args.log:
        logfile = open("%s.log" % datetime.datetime.now().strftime('%y%m%d%H%M%S'), 'wt')
    walk(args.beg, args.qty, args.verbose)


if __name__ == "__main__":
    main()
