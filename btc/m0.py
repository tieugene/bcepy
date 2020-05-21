"""
m0: Just walk.
(+txs, +bk_sizes)
"""

from btc.utils import snow
import btc.heap as heap

__line = "===\t=======\t=======\t====="


def prepare():
    pass


def prn_head():
    return "kBk\tSize\tTx\tTime\t%s (m0)\n%s" % (snow(), __line)


def prn_interim():
    return "%03d\t%d\t%d\t%d" % (heap.bk_no // heap.Bulk_Size, heap.bk_vol, heap.tx_count, heap.timer.now())


def prn_tail():
    return "%s\n%03d\t%d\t%d\t%d\t%s\nMax tx/bk: %d" % (
        __line, heap.bk_no // heap.Bulk_Size, heap.bk_vol, heap.tx_count, heap.timer.now(), snow(),
        heap.max_bk_tx)


def work_bk(bk):
    heap.bk_vol += bk['size']
    if heap.bk_no in heap.Dup_Blocks:
        return
    nTx = bk['nTx']
    heap.tx_count += nTx
    heap.max_bk_tx = max(heap.max_bk_tx, nTx)
