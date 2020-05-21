"""
m1: Deep walk.
(bk_size, txs, vins, vouts)
"""

from btc.utils import snow
import btc.heap as heap

__line = "===\t=======\t=======\t=======\t=======\t====="


def prepare():
    pass


def prn_head():
    return "kBk\tSize\tTx\tIn\tOut\tTime\t%s (m1)\n%s" % (snow(), __line)


def prn_interim():
    return "%03d\t%d\t%d\t%d\t%d\t%d" % (
        heap.bk_no // heap.Bulk_Size, heap.bk_vol, heap.tx_count, heap.in_count, heap.out_count, heap.timer.now())


def prn_tail():
    return "%s\n%03d\t%d\t%d\t%d\t%d\t%d\t%s\nMax tx/bk:\t%d\nMax in/tx:\t%d\nMax out/tx:\t%d" % (
        __line, heap.bk_no // heap.Bulk_Size, heap.bk_vol, heap.tx_count, heap.in_count, heap.out_count, heap.timer.now(), snow(),
        heap.max_bk_tx, heap.max_tx_in, heap.max_tx_out)


def work_bk(bk):
    heap.bk_vol += bk['size']
    if heap.bk_no in heap.Dup_Blocks:
        return
    nTx = bk['nTx']
    heap.tx_count += nTx
    heap.max_bk_tx = max(heap.max_bk_tx, nTx)
    for tx in bk['tx']:
        nIn = len(tx['vin'])
        heap.in_count += nIn
        heap.max_tx_in = max(heap.max_tx_in, nIn)
        nOut = len(tx['vout'])
        heap.out_count += nOut
        heap.max_tx_out = max(heap.max_tx_out, nOut)
