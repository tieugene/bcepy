"""m7: ..."""

def prn_head():
    Log_Header: str = "kBk\tTime\tTx\tAddr\tMsizez\tRAM\n===\t====\t===\t====\t=====\t==="

def prn_data():
    lprint("%d\t%d\t%d\t%d\t%d\t%d" % (
        int(bk_no / Bulk_Size), timer.now(), Tx.get_count(), Addr.get_count(), bk_vol, memer.now()))

def job_bk():
    tx_l = block["tx"]
    assert len(tx_l) == block["nTx"], "bk=%d, len(tx) <> nTx" % bk_no
    for tx in tx_l:
        # 2. each tx
        tx_hash_s: str = tx["txid"]  # str repr
        tx_hash_i: int = int(tx_hash_s, 16)  # int id
        tx_no: int = Tx.get(tx_hash_i)
        if tx_no is None:
            tx_no = Tx.add(tx_hash_i)
        else:  # already exists
            if not keep:
                eprint("Err: bk=%d, tx '%064x' already stored" % (bk_no, tx_hash_i))
                exit(1)  # TODO: raise exception
            # else:
            #    eprint("Tx %d skiped" % tx_no)
        sql.add_tx(tx_no, bk_no, tx_hash_s)
        # 2.1. vins: chk vouts exist
        for vin_n, vin in enumerate(tx["vin"]):
            if 'coinbase' in vin:
                continue
            vout_hash: int = int(vin['txid'], 16)
            vout_no: int = Tx.get(vout_hash)  # FIXME: strict get
            assert vout_no is not None, "bk=%d, tx '%064x', vout '%064x' not exists" % (bk_no, tx_hash_i, vout_hash)
            sql.add_vin(tx_no, vin_n, vout_no, vin["vout"])
            # tx_in_id <= tx_hash_i
            # tx_in_n <= simply vin counter (?!)
            # tx_out_id == vin.tx_hash_i
            # tx_out_n == vin.vout
        # 2.2. vout: add addresses
        for vout in tx["vout"]:
            # TODO: assert vout.n <= len(tx.vout)
            # 2.2.1. addresses
            addr_l: list = vout["scriptPubKey"].get('addresses', None)
            if addr_l is None:
                addr_no = None
            else:
                # print("Address get (block %d)" % (bk_no,))
                # TODO: assert len(addresses) > 0
                if len(addr_l) == 1:
                    addr_s = addr_l[0]
                else:
                    # print("Multisig:", bk_no, addresses, file=sys.stderr)
                    addr_l.sort()
                    addr_s: str = ' '.join(addr_l)  # convert into ' ' separated string
                addr_no = Addr.get(addr_s)  # FIXME: soft get
                if addr_no is None:
                    addr_no = Addr.add(addr_s)
                    sql.add_addr(addr_no, addr_l)
            # 2.2.2. vout itself
            # satosh = (value < -0.0) ? (int64_t) (BC_SPB * value - 0.5) : (int64_t) (BC_SPB * value + 0.5);
            sql.add_vout(tx_no, vout["n"], int(vout["value"] * 100000000), addr_no)
