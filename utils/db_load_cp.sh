#!/bin/sh
# Load DB using COPY (~30')
date +"=== Start: %y-%m-%d %H:%M:%S ==="
echo "b"; unpigz -c b.txt.gz | psql -q -c "COPY blocks (b_id, b_time) FROM STDIN;" btcdb btcuser
echo "t"; unpigz -c t.txt.gz | psql -q -c "COPY transactions (t_id, b_id, hash) FROM STDIN;" btcdb btcuser
echo "a"; unpigz -c a.txt.gz | psql -q -c "COPY addresses (a_id, a_list, n) FROM STDIN;" btcdb btcuser
echo "d"; unpigz -c d.txt.gz | psql -q -c "COPY data (t_out_id, t_out_n, satoshi, a_id, t_in_id) FROM STDIN;" btcdb btcuser
date +"=== End: %y-%m-%d %H:%M:%S ==="
