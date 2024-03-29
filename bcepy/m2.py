"""
m2: Process (inmem).
inmem tx.id, addr.id storage
"""
# 1. system
import datetime
import json
import os
# 2. local
from . import heap
from .utils import snow, pk2addr, eprint, Memer

# consts
PFX_KC = 'kc:'
PFX_TK = 'tk:'
__line = "===\t=======\t=======\t=======\t=======\t=======\t======="
__fmt_head = "kBk\tTx\tIn\tOut\tAddr\tRAM,M\tTime,s\t{} (m2, {})\n{}"
__fmt_interim = "{:03d}\t{}\t{}\t{}\t{}\t{}\t{}"
__fmt_end = "{}\n{:03d}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\nMax tx/bk:\t{}\nMax in/tx:\t{}\nMax out/tx:\t{}\nMax addr/out:\t{}"

# vars
Tx = None
Addr = None


def prepare(kbeg: int) -> bool:
    """
     t  beg kv  res
     =  === ==  ===
     +  N   0   ok
     +  0   0   ok
     +  1+  0   err ("k-v empty")
     +  N   1+  err ("set -f")
     +  0   1+  ok (+clear)
     x! 1+  1+  ok
    :param kbeg: begining kbk
    :return: True if ok
    redis:
        from .kv.rds import KV
        Tx = KV()
        Tx.open(0)
        Addr = KV()
        Addr.open(1)
    """
    global Tx, Addr
    if heap.Opts.kvdir:  # defined => file-based (kyotocabinet | tkrzw)
        if heap.Opts.kvdir.startswith(PFX_KC):
            from .kv.kc import KV
            kv_dir = heap.Opts.kvdir[len(PFX_KC):]
        elif heap.Opts.kvdir.startswith(PFX_TK):
            from .kv.tkx import KV
            kv_dir = heap.Opts.kvdir[len(PFX_TK):]
        else:
            kv_dir = heap.Opts.kvdir
            try:
                from .kv.tkx import KV  # default
            finally:
                from .kv.kc import KV
        if not os.path.isdir(kv_dir):
            eprint("'{} is not folder or not exists".format(kv_dir))
            return
        Tx = KV()
        Tx.open(os.path.join(kv_dir, "tx"))
        Addr = KV()
        Addr.open(os.path.join(kv_dir, "addr"))
    else:  # inmem
        from .kv.inmem import KV
        Tx = KV()
        Addr = KV()
    tx_count = Tx.get_count()
    if tx_count:
        if kbeg is None:
            eprint("Error: Tx is not empty ({} items). Set -f option.".format(tx_count))
            return
        if kbeg == 0:
            Tx.clean()
            Addr.clean()
    else:
        if kbeg:
            eprint("Error: Tx is empty. Use '-f 0' or skip it.")
            return
    heap.memer = Memer()
    heap.memer.start()
    return True


def prn_head():
    return __fmt_head.format(snow(), Tx.name(), __line)


def prn_interim():
    return __fmt_interim.format(
        heap.bk_no // heap.Bulk_Size, heap.tx_count, heap.in_count, heap.out_count, heap.addr_count,
        heap.memer.now(), heap.timer.now())


def prn_tail():
    return __fmt_end.format(
        __line, heap.bk_no // heap.Bulk_Size, heap.tx_count, heap.in_count, heap.out_count,
        heap.addr_count, heap.memer.now(), heap.timer.now(), snow(),
        heap.max_bk_tx, heap.max_tx_in, heap.max_tx_out, heap.max_out_addr)


def __out_bk(bk_no: int, ts: int, hsh: str):
    if heap.Opts.out:
        print("b\t{}\t'{}'\t'{}'".format(bk_no, datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"), hsh))


def __out_tx(tx_no: int, bk_no: int, hsh: str):
    if heap.Opts.out:
        print("t\t{}\t{}\t{}".format(tx_no, bk_no, hsh))


def __out_vin(out_no: int, out_n: int, in_no: int):
    if heap.Opts.out:
        print("i\t{}\t{}\t{}".format(out_no, out_n, in_no))


def __out_addr(addr_no: int, lst: list):
    if heap.Opts.out:
        if len(lst) == 1:
            s = '"%s"' % lst[0]
        else:
            s = json.dumps(lst)
        print("a\t{}\t{}\t{}".format(addr_no, s, len(lst)))


def __out_vout(tx_no: int, n: int, satoshi: int, addr: int):
    if heap.Opts.out:
        print("o\t{}\t{}\t{}\t{}".format(tx_no, n, satoshi, '\\N' if addr is None else str(addr)))


def work_bk(bk):
    tx_qty = len(bk['tx'])  # bk['nTx']
    # heap.bk_vol += bk['size']
    heap.tx_count += tx_qty
    heap.max_bk_tx = max(heap.max_bk_tx, tx_qty)
    # 1. bk
    __out_bk(heap.bk_no, int(bk['time']), bk['hash'])
    if heap.bk_no in heap.Dup_Blocks:
        return
    for tx in bk['tx']:
        # misc statistics
        vin_qty = len(tx['vin'])
        heap.in_count += vin_qty
        heap.max_tx_in = max(heap.max_tx_in, vin_qty)
        vout_qty = len(tx['vout'])
        heap.out_count += vout_qty
        heap.max_tx_out = max(heap.max_tx_out, vout_qty)
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
            assert vout_no is not None, "bk={}, tx '{}', vin # {}: vout '{}' not exists".format(
                heap.bk_no, tx_hash_s, vin_n, vout_hash.hex())
            __out_vin(vout_no, vin['vout'], tx_no)
        for vout in tx['vout']:
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
            __out_vout(tx_no, vout['n'], int(vout["value"] * 100000000), addr_no)  # FIXME: float
