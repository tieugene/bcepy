# Usage

Bitcoind connection are loading from bitcoin.conf as it is required for bitcoin-cli.  
Options (use `bcepy -h` for help):

- `-f` *int*: from kiloblock (default 0)
- `-q` *int*: kiloblocks to process (default 1 kbk)
- `-l`: write log file (yymmddhhMMss.log)
- `-m` *mode*:
  - `0`: counts blocks (bk), their size and transactions (tx) querying bitcoind like `bitcoin-cli getblock <hash> 1`.
  - `1`: == `0` + vouts and vins.
  - `2`: == `1` + addresses. Uses key-value storage (default in-memory; see `-c`). Quiet without `-o` option (just fills out key-values)
- `-o`: generates text output (`-m 2` only, stdout)
- `-c` *dir*: set file-based key-value storage.
  - Using `kc:` (kyotocabinet) or `tk:` path prefix set exact key-value backend.
  - Ommiting prefix cause trying kyotocabinet then tkrzw then exception if both are absent.
  - Ommiting path at all cause usage of in-memory k-v.
