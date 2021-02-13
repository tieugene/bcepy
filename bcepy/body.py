"""
All together.
- 0 - just walk (+bk_size, +txs)
- 1 - +vins,+vouts
- 2 - +store (file) txs (tx.id:no), addrs; gen data
- 3 - +txout (tx.no:vout.n)
"""

# 2. local
from .authproxy import AuthServiceProxy as Proxy
from .utils import load_conf, eprint, Timer
from . import heap


def walk(kbeg: int, kty: int):
    """
    Main loop
    @param kbeg: 1st Kblock
    @param kty: Kblocks to process
    """
    if heap.Opts.mode == 0:
        from . import m0 as mode
    elif heap.Opts.mode == 1:
        from . import m1 as mode
    else:
        from . import m2 as mode
    # 0. prepare
    cfg = load_conf()
    url = "http://{}:{}@{}:{}".format(cfg['rpcuser'], cfg['rpcpassword'], cfg['rpcconnect'], cfg['rpcport'])
    rpc_connection = Proxy(url, timeout=300)  # for heavy load
    if not mode.prepare(kbeg):
        return
    if kbeg is None:    # FIXME: wut?
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
