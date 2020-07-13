"""
m2: Process (inmem).
inmem tx.id, addr.id storage
"""

import datetime, os
import json

import btc.heap as heap
# from btc.kv.inmem import KV
# from btc.kv.rds import KV
from btc.kv.kc import KV
from btc.utils import snow, Memer, pk2addr

Tx = None
Addr = None

__line = "===\t=======\t=======\t=======\t=======\t=======\t=======\t====="


def prepare():
    global Tx, Addr
    Tx = KV()
    # Tx.open(0)
    Tx.open(os.path.join(heap.kvdir, "tx"))
    Tx.clean()
    Addr = KV()
    # Addr.open(1)
    Addr.open(os.path.join(heap.kvdir, "addr"))
    Addr.clean()
    heap.memer = Memer()
    heap.memer.start()


def prn_head():
    return "kBk\tSize\tTx\tIn\tOut\tAddr\tRAM\tTime\t%s (m2)\n%s" % (snow(), __line)


def prn_interim():
    return "%03d\t%d\t%d\t%d\t%d\t%d\t%d\t%d" % (
        heap.bk_no // heap.Bulk_Size, heap.bk_vol, heap.tx_count, heap.in_count, heap.out_count, heap.addr_count,
        heap.memer.now(), heap.timer.now())


def prn_tail():
    return "%s\n%03d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\nMax tx/bk:\t%d\nMax in/tx:\t%d\nMax out/tx:\t%d\nMax addr/out:\t%d" % \
           (__line, heap.bk_no // heap.Bulk_Size, heap.bk_vol, heap.tx_count, heap.in_count, heap.out_count,
            heap.addr_count, heap.memer.now(), heap.timer.now(), snow(),
            heap.max_bk_tx, heap.max_tx_in, heap.max_tx_out, heap.max_out_addr)


def __out_bk(bk_no: int, ts: int, hsh: str):
    if heap.Opts.out:
        print("b\t%d\t'%s'\t'%s'" % (bk_no, datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"), hsh))


def __out_tx(tx_no: int, bk_no: int, hsh: str):
    if heap.Opts.out:
        print("t\t%d\t%d\t%s" % (tx_no, bk_no, hsh))


def __out_vin(out_no: int, out_n: int, in_no: int):
    if heap.Opts.out:
        print("i\t%d\t%d\t%d" % (out_no, out_n, in_no))


def __out_addr(addr_no: int, lst: list):
    if heap.Opts.out:
        if len(lst) == 1:
            s = '"%s"' % lst[0]
            n = 1
        else:
            s = json.dumps(lst)
            n = len(s)
        print("a\t%d\t%s\t%d" % (addr_no, s, n))


def __out_vout(tx_no: int, n: int, satoshi: int, addr: int):
    if heap.Opts.out:
        print("o\t%d\t%d\t%d\t%s" % (tx_no, n, satoshi, '\\N' if addr is None else str(addr)))


def work_bk(bk):
    nTx = bk['nTx']
    heap.bk_vol += bk['size']
    heap.tx_count += nTx
    heap.max_bk_tx = max(heap.max_bk_tx, nTx)
    # 1. bk
    __out_bk(heap.bk_no, int(bk['time']), bk['hash'])
    if heap.bk_no in heap.Dup_Blocks:
        return
    for tx in bk['tx']:
        # misc statistics
        nIn = len(tx['vin'])
        heap.in_count += nIn
        heap.max_tx_in = max(heap.max_tx_in, nIn)
        nOut = len(tx['vout'])
        heap.out_count += nOut
        heap.max_tx_out = max(heap.max_tx_out, nOut)
        # 2. tx
        tx_hash_s = tx["txid"]  # str repr
        tx_hash_b = bytes.fromhex(tx_hash_s)
        tx_no = Tx.add(tx_hash_b)
        __out_tx(tx_no, heap.bk_no, tx_hash_s)
        for vin_n, vin in enumerate(tx["vin"]):
            # 3. vin
            if 'coinbase' in vin:
                continue
            vout_hash = bytes.fromhex(vin['txid'])
            vout_no = Tx.get(vout_hash)  # FIXME: strict get
            assert vout_no is not None, "bk=%d, tx '%s', vin # %d: vout '%s' not exists" % \
                                        (heap.bk_no, tx_hash_s, vin_n, vout_hash.hex())
            __out_vin(vout_no, vin['vout'], tx_no)
        for vout in tx["vout"]:
            # FIXME: assert vout.n <= len(tx.vout)
            # 4. addresses
            spk = vout["scriptPubKey"]
            if spk['type'] == 'pubkey':
                addr_l = [pk2addr(spk['asm'].split(' ')[0])]
            else:
                addr_l = spk.get('addresses', None)
            if addr_l is None:
                addr_no = None
            else:
                if len(addr_l) == 1:
                    addr_s = addr_l[0]
                else:
                    addr_l.sort()
                    addr_s = ' '.join(addr_l)  # convert into ' ' separated string
                addr_no = Addr.get(addr_s)
                if addr_no is None:
                    addr_no = Addr.add(addr_s)
                    heap.addr_count += 1
                    heap.max_out_addr = max(heap.max_out_addr, len(addr_l))
                    __out_addr(addr_no, addr_l)
            # 5. vout
            # satosh = (value < -0.0) ? (int64_t) (BC_SPB * value - 0.5) : (int64_t) (BC_SPB * value + 0.5);
            # sql.add_vout(tx_no, vout["n"], int(vout["value"] * 100000000), addr_no)
            __out_vout(tx_no, vout['n'], int(vout["value"] * 100000000), addr_no)
