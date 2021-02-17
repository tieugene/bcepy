# bcepy - BitCoin Export (*py*thon version)

Exports BTC blockchain into SQL DB loadable data.

## Explanation

Storing blocks/transactions/addresses in SQL DB with their hashes as primary keys makes DBs extreme huge.
The solution is to use their order numbers.  
This application:
- get blocks from bitcoind
- enumerates objects (bk/tx/address) using key-value storage
- and exports results in compact text representation, ready to load into SQL DB.

_Note: see [compilable version](https://github.com/tieugene/bce2) to compare_

## Documentation

- [Installation](doc/Install.md)
- [Usage](doc/Usage.md)
- [Output](doc/Output.md) format

## License

This application is distributing under GPL v3.0 [LICENSE](LICENSE)
