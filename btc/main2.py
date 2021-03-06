"""
8. All together.
- 0 - just walk (+bk_size, +txs)
- 1 - +vins,+vouts
- 2 - +store (file) txs (tx.id:no), addrs; gen data
- 3 - +txout (tx.no:vout.n)
"""

import argparse
import datetime

from btc.authproxy import AuthServiceProxy as Proxy
# from slickrpc import Proxy

import btc.heap as heap
from btc.utils import load_conf, eprint, Timer


def walk(kbeg: int, kty: int):
    """
    Main loop
    @param kbeg: 1st Kblock
    @param kty: Kblocks to process
    """
    if heap.Opts.mode == 0:
        import btc.m0 as mode
    elif heap.Opts.mode == 1:
        import btc.m1 as mode
    else:
        import btc.m2 as mode
    # 0. prepare
    rpc_connection = Proxy(load_conf(), timeout=300)  # for heavy load
    if mode.prepare(kbeg):
        return
    if kbeg is None:
        kbeg = 0
    heap.bk_no = kbeg * heap.Bulk_Size
    bk_to = heap.bk_no + (kty * heap.Bulk_Size)
    bk_hash = rpc_connection.getblockhash(heap.bk_no)
    heap.timer = Timer()
    # 1. go
    heap.timer.start()
    eprint(mode.prn_head())
    while heap.bk_no < bk_to:
        block = rpc_connection.getblock(bk_hash, 1 if heap.Opts.mode == 0 else 2)  # 0=raw hex, [1]=short, 2=full
        mode.work_bk(block)
        bk_hash = block['nextblockhash']
        heap.bk_no += 1
        if not (heap.bk_no % heap.Interim_Size):
            eprint(mode.prn_interim())
    eprint(mode.prn_tail())


def init_cli():
    """ Handle CLI """
    parser = argparse.ArgumentParser(description='Process blockchain.')
    parser.add_argument('-m', '--mode', metavar='n', type=int, nargs='?', default=0,
                        help='Mode: 0 - simple walk, 1 - deep walk, 2 - full process (default=0)')
    parser.add_argument('-f', '--from', dest='beg', metavar='n', type=int, nargs='?', default=None,
                        help='kBk start from (default=0)')
    parser.add_argument('-q', '--qty', metavar='n', type=int, nargs='?', default=1, help='kBk to process (default=1)')
    # parser.add_argument('-k', '--keep', action='store_true', help='Keep existing Tx/Addr (default=false)')
    parser.add_argument('-l', '--log', action='store_true', help='Logfile (default=false)')
    parser.add_argument('-o', '--out', action='store_true', help='DB output (default=false)')
    parser.add_argument('-c', '--cache', type=str, metavar='dir', nargs='?', default=".", help='Cache dir (default=.)')
    return parser


def main():
    """
    CLI commands/options handler.
    """
    parser = init_cli()
    args = parser.parse_args()
    if args.mode is None:
        parser.print_help()
    elif args.mode > 2:
        print("Wrong mode: %d" % args.mode)
    else:
        if args.log:
            heap.Opts.log = True
            heap.logfile = open("%s.log" % datetime.datetime.now().strftime('%y%m%d%H%M%S'), 'wt')
        heap.Opts.mode = args.mode
        # heap.Opts.keep = args.keep
        heap.Opts.out = args.out
        heap.Opts.kvdir = args.cache
        walk(args.beg, args.qty)
