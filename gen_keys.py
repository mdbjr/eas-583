from web3 import Web3
import eth_account
import os

def get_keys(challenge,keyId = 0, filename = "eth_mnemonic.txt"):
    """
    Generate a stable private key
    challenge - byte string
    keyId (integer) - which key to use
    filename - filename to read and store mnemonics

    Each mnemonic is stored on a separate line
    If fewer than (keyId+1) mnemonics have been generated, generate a new one and return that
    """

    w3 = Web3()

    msg = eth_account.messages.encode_defunct(challenge)

	#YOUR CODE HERE
    #acct = w3.eth.account.create()
    eth_addr = '91544d32c71630d1963cb0fbbd643814591845d3826984d34126debf044053ae'#acct.key.hex()
    acct = w3.eth.account.from_key(eth_addr)
    sig = w3.eth.account.sign_message(msg, private_key=eth_addr)
    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == acct.address, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig, acct.address

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
