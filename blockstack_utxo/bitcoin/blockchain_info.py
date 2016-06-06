# -*- coding: utf-8 -*-
"""
    blockstack-utxo
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json, requests, traceback

BLOCKCHAIN_API_BASE_URL = "https://blockchain.info"

from .blockchain_client import BlockchainClient
from virtualchain.lib.transactions import VirtualPaymentOutput

class BlockchainInfoClient(BlockchainClient):
    def __init__(self, api_key=None):
        self.type = 'blockchain.info'
        if api_key:
            self.auth = (api_key, '')
        else:
            self.auth = None


def reverse_hash(hash, hex_format=True):
    """ hash is in hex or binary format
    """
    if not hex_format:
        hash = hexlify(hash)
    return "".join(reversed([hash[i:i+2] for i in range(0, len(hash), 2)]))


def format_unspents(unspents):
    vouts = []
    for s in unspents:
        vout = VirtualPaymentOutput( s['script'], s['value'], [], \
                                     transaction_hash=reverse_hash(s['tx_hash']), confirmations=s['confirmations'], output_index=s['tx_output_n'] )

        vouts.append( vout )

    return vouts


def get_inputs(address, blockchain_client=BlockchainInfoClient()):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    if not isinstance(blockchain_client, BlockchainInfoClient):
        raise Exception('A BlockchainInfoClient object is required')

    url = BLOCKCHAIN_API_BASE_URL + "/unspent?format=json&active=" + address

    auth = blockchain_client.auth
    if auth and len(auth) == 2 and isinstance(auth[0], str):
        url = url + "&api_code=" + auth[0]

    r = requests.get(url, auth=auth)
    try:
        unspents = r.json()["unspent_outputs"]
    except ValueError, e:
        raise Exception('Invalid response from blockchain.info.')
    
    return format_unspents(unspents)

def broadcast_transaction(hex_tx, blockchain_client=BlockchainInfoClient()):
    """ Dispatch a raw transaction to the network.
    """
    url = BLOCKCHAIN_API_BASE_URL + '/pushtx'
    payload = {'tx': hex_tx}
    r = requests.post(url, data=payload, auth=blockchain_client.auth)
    
    if 'submitted' in r.text.lower():
        return {'success': True}
    else:
        raise Exception('Invalid response from blockchain.info.')


