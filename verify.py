from web3 import Web3
from eth_account.messages import encode_defunct
import eth_account
import random
from web3.middleware import geth_poa_middleware
import json
from eth_hash.auto import keccak
import hashlib

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
    #w3 = connect_to_eth.connect_to_eth()
    w3 = Web3(Web3.HTTPProvider("https://api.avax-test.network/ext/bc/C/rpc"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"


    with open('NFT_abi.json', 'r') as f:
        contract_abi = json.load(f)
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    sk = '7909e1cfd3d865eccdbcd9676804f16bedebba61963d7c44406ecb53e2653787'#"YOUR SECRET KEY HERE"

    acct = w3.eth.account.from_key(sk)
    nonce = "393857392092739"# Example nonce
    hash_result = keccak(nonce.encode('utf-8'))
    contract.functions.claim(acct.address,hash_result).call()
    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )

