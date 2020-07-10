"""heap: global variables"""

# consts
Bulk_Size = 1000
Interim_Size = 1000
Dup_Blocks = {91722, 91842}  # duplicate 91880, 91812

# counters; TODO: object.attr
bk_vol = 0         # blocks size accumulator
bk_no = 0          # current block's no (height)
tx_count = 0       # tx count accumulator
in_count = 0
out_count = 0
addr_count = 0
max_bk_tx = 0
max_tx_in = 0
max_tx_out = 0
max_out_addr = 0

# CLI options
class   Opts(object):
    mode = 0
    keep = False
    log = False
    out = False
    kvdir = "."

# misc vars
logfile = None
timer = None
memer = None
