# -*- coding: utf-8 -*-
"""
    blockstack-utxo
    ~~~~~

    :copyright: (c) 2014 by Halfmoon Labs
    :license: MIT, see LICENSE for more details.
"""

import json, requests, traceback

CHAIN_API_BASE_URL = 'https://api.chain.com/v2'

from .blockchain_client import BlockchainClient
from virtualchain.lib.transactions import VirtualPaymentOutput

class ChainComClient(BlockchainClient):
    def __init__(self, api_key_id=None, api_key_secret=None):
        self.type = 'chain.com'
        if api_key_id and api_key_secret:
            self.auth = (api_key_id, api_key_secret)
        else:
            self.auth = None

def format_unspents(unspents):
    vouts = []
    for s in unspents:
        vout = VirtualPaymentOutput( s['script_hex'], s['value'], [], \
                                     transaction_hash=s['transaction_hash'], confirmations=s['confirmations'], output_index=s['output_index'],
                                     script_opcodes=s['script'], script_type=s['script_type'] )

        vouts.append( vout )

    return vouts


def get_inputs(address, blockchain_client=ChainComClient()):
    """ Get the spendable transaction outputs, also known as UTXOs or
        unspent transaction outputs.
    """
    if not isinstance(blockchain_client, ChainComClient):
        raise Exception('A ChainComClient object is required')

    url = CHAIN_API_BASE_URL + '/bitcoin/addresses/' + address + '/unspents'

    auth = blockchain_client.auth
    if auth:
        r = requests.get(url, auth=auth)
    else:
        r = requests.get(url + '?api-key-id=DEMO-4a5e1e4')

    try:
        unspents = r.json()
    except ValueError, e:
        raise Exception('Received non-JSON response from chain.com.')
    
    return format_unspents(unspents)


def broadcast_transaction(hex_tx, blockchain_client):
    """ Dispatch a raw hex transaction to the network.
    """
    if not isinstance(blockchain_client, ChainComClient):
        raise Exception('A ChainComClient object is required')

    auth = blockchain_client.auth
    if not auth or len(auth) != 2:
        raise Exception('ChainComClient object must have auth credentials.')

    url = CHAIN_API_BASE_URL + '/bitcoin/transactions/send'
    payload = json.dumps({ 'signed_hex': hex_tx })
    r = requests.post(url, data=payload, auth=auth)

    try:
        data = r.json()
    except ValueError, e:
        raise Exception('Received non-JSON from chain.com.')

    if 'transaction_hash' in data:
        reply = {}
        reply['tx_hash'] = data['transaction_hash']
        reply['success'] = True
        return reply
    else:
        raise Exception('Tx hash missing from chain.com response: ' + str(data) + '\noriginal: ' + str(payload))

