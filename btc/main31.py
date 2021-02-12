#!/bin/env python3
"""
Export bvitcoind data to gziped jsons.
3rd parties: None
time (kbk, macbook, wifi):
1   4
100 718 (60=>396MB)
"""
# 1. system
import argparse
import datetime
import os
import time
import gzip
import pathlib
import json
# 2. local
from .authproxy import AuthServiceProxy as Proxy
from .utils import load_conf, eprint

# Dup_Blocks = {91722, 91812}  # duplicate 91880, 91842
Bulk_Size = 1000
Interim_Size = 1000
logfile = None
outdir = None
tpl = (
    ("kBk\tSize\tTx\tTime", "===\t=======\t=======\t=====", "%03d\t%d\t%d\t%d"),
    ("kBk\tSize\tTx\tIn\tOut\tTime", "===\t=======\t=======\t=======\t=======\t=====", "%03d\t%d\t%d\t%d\t%d\t%d")
)
waste_bk = {
    'confirmations',
    'strippedsize',
    'size',
    'weight',
    'versionHex',
    'merkelroot',
    'mediantime',
    'nonce',
    'bits',
    'difficulty',
    'chainwork',
    'nTx'
}

wanted_bk = {
    'hash',
    'height',
    'time',
}
wanted_tx = {
    'txid',
}
wanted_vin = {
    'coinbase',     # ?
    'txid',         # ? <> coinbase
    'vout'          # ? <> coinbase
}
wanted_vout = {     # *
    'value',
    'n'
    'scriptPubKey'
}
wanted_script = {
    'type',
    'asm',
    'hex',
    'addresses',    # ?
}


def save_bk(bk: dict) -> bool:
    """
    Save block json as light and compressed file
    :param bk: block dict
    :return: True if ok
    """
    def __copy_bk(bk: dict) -> dict:
        txs = list()
        for tx in bk['tx']:
            vins = list()
            for vin in tx['vin']:
                if 'coinbase' in vin:
                    vins.append({'coinbase': 1})
                else:
                    vins.append({
                        'txid': vin['txid'],
                        'vout': vin['vout'],
                    })
            vouts = list()
            for vout in tx['vout']:
                vouts.append(vout)
            txs.append({
                'txid': tx['txid'],
                'vin': vins,
                'vout': vouts,
            })
        # 2. generate
        return({
            'hash': bk['hash'],
            'height': bk['height'],
            'time': bk['time'],
            'tx': txs
        })
    bk_no = int(bk["height"])
    fname = "%06d.json.gz" % bk_no
    dname = fname[:3]
    dpath = os.path.join(outdir, dname)
    os.makedirs(dpath, exist_ok=True)
    fpath = os.path.join(dpath, fname)
    with gzip.open(fpath, "wt") as f:
        f.write(json.dumps(__copy_bk(bk), indent=1))
    return True


def walk(kbeg: int, kty: int, v: bool):
    """
    Main loop
    :param kbeg: starting Kblock
    :param kty: Kblocks to process
    :param v: verbosity
    """
    # 0. prepare
    bk_no = kbeg * Bulk_Size
    bk_to = bk_no + (kty * Bulk_Size)
    size = 0
    txs = 0
    ins = 0
    outs = 0
    cfg = load_conf()
    url = "http://{}:{}@{}:{}".format(cfg['rpcuser'], cfg['rpcpassword'], cfg['rpcconnect'], cfg['rpcport'])
    rpc_connection = Proxy(url, timeout=300)  # for heavy load
    bk_hash = rpc_connection.getblockhash(bk_no)
    eprint("%s\n%s" % (tpl[v][0], tpl[v][1]))
    # 1. go
    t0 = time.time()
    while bk_no < bk_to:
        bk = rpc_connection.getblock(bk_hash, 1 + v)
        # if int(bk['height']) not in Dup_Blocks:
        # TODO: assert bk_no == int(bk["height"])
        size += bk['size']
        txs += bk['nTx']
        if v:
            for tx in bk['tx']:
                ins += len(tx['vin'])
                outs += len(tx['vout'])
            if outdir:
                if not save_bk(bk):
                    break
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
    parser.add_argument('-o', '--out', metavar='path', type=str, nargs='?', help='Output directory')
    return parser


def main():
    """
    CLI commands/options handler.
    """
    global logfile, outdir
    parser = init_cli()
    args = parser.parse_args()
    if args.log:
        logfile = open("%s.log" % datetime.datetime.now().strftime('%y%m%d%H%M%S'), 'wt')
    if args.out:
        if not args.verbose:
            eprint("'-o' option has no sense without -v")
            return
        outdir = args.out.replace('~', str(pathlib.Path.home()))  # macos trick
        if not os.path.isdir(outdir):
            eprint("Output path '{}' is not directory or not exists.".format(outdir))
            return
    walk(args.beg, args.qty, args.verbose)
