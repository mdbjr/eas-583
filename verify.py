from web3 import Web3
from eth_account.messages import encode_defunct
import eth_account
import random
from web3.middleware import geth_poa_middleware
import json
from eth_hash.auto import keccak
import random
import hashlib
import secrets

import connect_to_eth


def signChallenge( challenge ):

    w3 = Web3()
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    #This is the only line you need to modify
    sk = '7909e1cfd3d865eccdbcd9676804f16bedebba61963d7c44406ecb53e2653787'#"YOUR SECRET KEY HERE"

    acct = w3.eth.account.from_key(sk)
    print(acct.address)

    signed_message = w3.eth.account.sign_message( challenge, private_key = acct._private_key )

    return acct.address, signed_message.signature


def verifySig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing 
    """


    challenge_bytes = random.randbytes(32)

    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge( challenge )

    w3 = Web3()

    return w3.eth.account.recover_message( challenge , signature=sig ) == address

if __name__ == '__main__':
    """
        Test your function
    """
    w3 = Web3(Web3.HTTPProvider("https://avalanche-fuji-c-chain-rpc.publicnode.com"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"


    with open('NFT_abi.json', 'r') as f:
        contract_abi = json.load(f)
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    sk = '7909e1cfd3d865eccdbcd9676804f16bedebba61963d7c44406ecb53e2653787'#"YOUR SECRET KEY HERE"

    acct = w3.eth.account.from_key(sk)
    max_nonce_value = 40

    nonce = random.randint(0, max_nonce_value)

    nonce = secrets.token_bytes(32)
    nft_id = contract.functions.claim(acct.address,nonce).call()
    contract.functions.ownerOf(nft_id).call()

    tx_raw = contract.functions.claim(acct.address, nonce).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
    })

    signed_tx = w3.eth.account.sign_transaction(tx_raw, private_key=acct.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )

