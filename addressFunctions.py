def getTxAddresses(tx):
    addresses = []

    for inp in tx["vin"]:
        if( inp["prevout"] and inp["prevout"].get("scriptpubkey_address") ):
            addresses.append(inp["prevout"]["scriptpubkey_address"])

    for out in tx["vout"]:
        if( out.get("scriptpubkey_address") ):
            addresses.append(out["scriptpubkey_address"])

    return addresses

def hasTaprootAddress(tx):
    address_list = getTxAddresses(tx)

    for address in address_list:
        if( address.startswith("bc1p") ):
            return True

    return False