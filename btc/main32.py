"""
"""

import argparse
import datetime
import json
import os
import pathlib
import gzip

import btc.heap as heap
from btc.utils import load_conf, eprint, Timer


def load_bk(no: int) -> dict:
    fname = "%06d.json.gz" % no
    fpath = os.path.join(heap.Opts.jsdir, fname[:3], fname)
    with gzip.open(fpath, "rt") as f:
        bk = json.load(f)
    return bk


def walk(kbeg: int, kty: int):
    """
    Main loop
    @param kbeg: 1st Kblock
    @param kty: Kblocks to process
    """
    import btc.m2 as mode
    # 0. prepare
    if mode.prepare(kbeg):
        return
    if kbeg is None:
        kbeg = 0
    heap.bk_no = kbeg * heap.Bulk_Size
    bk_to = heap.bk_no + (kty * heap.Bulk_Size)
    heap.timer = Timer()
    # 1. go
    heap.timer.start()
    eprint(mode.prn_head())
    while heap.bk_no < bk_to:
        block = load_bk(heap.bk_no)
        if not block:
            break
        mode.work_bk(block)
        heap.bk_no += 1
        if not (heap.bk_no % heap.Interim_Size):
            eprint(mode.prn_interim())
    eprint(mode.prn_tail())


def init_cli():
    """
    Handle CLI
    TODO: mandatory args (-i)
    """
    parser = argparse.ArgumentParser(description='Process blockchain.')
    parser.add_argument('-i', '--indir', metavar='dir', type=str, nargs=1,
                        help='Directory with gziped jsons.')
    parser.add_argument('-f', '--from', dest='beg', metavar='n', type=int, nargs='?', default=None,
                        help='kBk start from (default=0)')
    parser.add_argument('-q', '--qty', metavar='n', type=int, nargs='?', default=1,
                        help='kBk to process (default=1)')
    parser.add_argument('-l', '--log', action='store_true',
                        help='Logfile (default=false)')
    parser.add_argument('-o', '--out', action='store_true',
                        help='DB output (default=false)')
    parser.add_argument('-c', '--cache', type=str, metavar='dir', nargs='?',
                        help='Tokyocabinet dir (or Redis if none)')
    return parser


def main():
    """
    CLI commands/options handler.
    """
    parser = init_cli()
    args = parser.parse_args()
    # print(args)
    if not args.indir:
        parser.print_help()
        return
    heap.Opts.jsdir = args.indir[0].replace('~', str(pathlib.Path.home()))  # macos trick
    if not os.path.isdir(heap.Opts.jsdir):
        eprint("Output path '{}' is not directory or not exists.".format(heap.Opts.jsdir))
        return
    if args.log:
        heap.Opts.log = True
        heap.logfile = open("%s.log" % datetime.datetime.now().strftime('%y%m%d%H%M%S'), 'wt')
    heap.Opts.out = args.out
    heap.Opts.kvdir = args.cache
    walk(args.beg, args.qty)
