import requests
import requests.packages.urllib3.util.connection
import aiohttp
import asyncio

# force ipv4
from socket import AF_INET
requests.packages.urllib3.util.connection.allowed_gai_family = lambda: AF_INET

ERROR_MESSAGE = "start index out of range"

async def getBlockTxs(session, hash, n):
    while( True ):
        resp = await session.get(f"https://mempool.space/api/block/{hash}/txs/{n}")
        text = await resp.text()

        if( resp.ok ):
            resp = await resp.json()
            return resp
        elif( text == ERROR_MESSAGE ):
            break

    return []

async def getBlock(hash):
    session = aiohttp.ClientSession()

    tasks = [asyncio.ensure_future(getBlockTxs(session, hash, n)) for n in range(0, 6000, 25)]
    i = await asyncio.gather(*tasks)

    await session.close()
    
    txs = sum(i, start = [])

    return txs

def getBlockRange(n1, n2):
    hashs = {}

    while( n2 >= n1 ):
        last_blocks = requests.get(f"https://mempool.space/api/blocks/{n2}").json()

        for block in last_blocks:
            if( block["height"] < n1 ):
                break

            hashs[block["height"]]= block["id"]

        n2 = last_blocks[-1]["height"] - 1

    return dict(reversed(list(hashs.items())))