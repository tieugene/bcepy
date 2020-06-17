# Bitcoin API
<dl>
<dt> getblockchaininfo:
	<dd> Get info about tip blockchain<br/>
	blocks: int - downloaded<br/>
	headers: int - all blocks<br/>
	bestblockhash: hash - tip block<br/>
	mediantime: unixtime - timestamp of last downloaded block (GMT)
<dt> getblockcount:
	<dd> == getblockchaininfo.blocks
<dt> getbestblockhash:
	<dd> == getblockchaininfo.bestblockhash
<dt> getblockhash <height:int>:
	<dd> get block info (1st is #0; no previousblockhash)
<dt> getblock <hash> [verb:int]:
	<dd>
	time: int - time of block generated
	mediantime: int == time
	chainwork: hash
	nTx: int
	tx: hash[nTx]
	[previousblockhash: hash]
	nextblockhash: hash
<dt> getblockheader &lt;blockhash&gt; ( verbose ):
<dt> getblockstats hash_or_height (stats):
<dt> ?decodescript "hexstring":
<dt> ?getrawtransaction "txid" (verbose "blockhash"):
</dl>
