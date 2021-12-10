import asyncio
from apiFunctions import getBlockRange, getBlock
from addressFunctions import hasTaprootAddress

from_block = int(input("From block number: "))
to_block = int(input("To block number: "))

block_hashes = getBlockRange(from_block, to_block)

taproot = []

for block_num in block_hashes:
	txs = asyncio.run(getBlock(block_hashes[block_num]))

	print(f"Checking block {block_num}.")
	
	for tx in txs:
		if( hasTaprootAddress(tx) ):
			taproot.append(tx)

for tap in taproot:
	print(tap["txid"])
