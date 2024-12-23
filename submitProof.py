import eth_account
import random
import string
import json
from pathlib import Path
from web3 import Web3, EthereumTesterProvider
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider
from eth_account.messages import encode_defunct


def merkle_assignment():
    """
        The only modifications you need to make to this method are to assign
        your "random_leaf_index" and uncomment the last line when you are
        ready to attempt to claim a prime. You will need to complete the
        methods called by this method to generate the proof.
    """
    # Generate the list of primes as integers
    num_of_primes = 8192
    #num_of_primes = 8
    primes = generate_primes(num_of_primes)

    # Create a version of the list of primes in bytes32 format
    leaves = convert_leaves(primes)

    # Build a Merkle tree using the bytes32 leaves as the Merkle tree's leaves
    tree = build_merkle(leaves)

    # Select a random leaf and create a proof for that leaf
    random_leaf_index = random.randint(0, num_of_primes-1) #TODO generate a random index from primes to claim (0 is already claimed)
    proof = prove_merkle(tree, random_leaf_index)

    # This is the same way the grader generates a challenge for sign_challenge()
    challenge = ''.join(random.choice(string.ascii_letters) for i in range(32))
    # Sign the challenge to prove to the grader you hold the account
    addr, sig = sign_challenge(challenge)

    if sign_challenge_verify(challenge, addr, sig):
        tx_hash = '0x'
        # TODO, when you are ready to attempt to claim a prime (and pay gas fees),
        #  complete this method and run your code with the following line un-commented
        #tx_hash = send_signed_msg(proof, leaves[random_leaf_index])


def generate_primes(num_primes):
    """
        Function to generate the first 'num_primes' prime numbers
        returns list (with length n) of primes (as ints) in ascending order
    """
    primes_list = []
    i = 2
    while len(primes_list)<num_primes:
        factors_of_i = []
        for j in [1,2]+primes_list+[i]:
            remainder = i % j
            if remainder == 0:
                factors_of_i.append(j)
        if len(factors_of_i)==2:
            primes_list.append(i)
            #print(str(i)+" is prime")
            #print("GOT "+str(len(primes_list))+" primes")
        i+=1

    return [2]+primes_list[0:-1]


def convert_leaves(primes_list):
    """
        Converts the leaves (primes_list) to bytes32 format
        returns list of primes where list entries are bytes32 encodings of primes_list entries
    """

    # TODO YOUR CODE HERE
    bytes_list = []
    for i in primes_list:
        bytes_value = i.to_bytes(32, byteorder='big')  # 'big' for big-endian format
        bytes_list.append(bytes_value)

    return bytes_list


def build_merkle(leaves):
    """
        Function to build a Merkle Tree from the list of prime numbers in bytes32 format
        Returns the Merkle tree (tree) as a list where tree[0] is the list of leaves,
        tree[1] is the parent hashes, and so on until tree[n] which is the root hash
        the root hash produced by the "hash_pair" helper function
    """
    #TODO YOUR CODE HERE
    if len(leaves)%2==1:
        leaves.append(leaves[-1])
    tree = []
    tree.append(leaves)
    len_last_layer = len(leaves)
    last_layer = leaves.copy()
    while len_last_layer>1:
        next_layer = []
        for i in range(0, len(last_layer), 2):
            pair_to_hash = sorted([last_layer[i], last_layer[i+1]])
            hash = hash_pair(pair_to_hash[0], pair_to_hash[1])
            next_layer.append(hash)
        tree.append(next_layer)
        len_last_layer = len(next_layer)
        last_layer = next_layer.copy()


    return tree


def prove_merkle(merkle_tree, random_indx):
    """
        Takes a random_index to create a proof of inclusion for and a complete Merkle tree
        as a list of lists where index 0 is the list of leaves, index 1 is the list of
        parent hash values, up to index -1 which is the list of the root hash.
        returns a proof of inclusion as list of values
    """
    merkle_proof = []
    # TODO YOUR CODE HERE
    sibling_hashes = []
    if random_indx % 2 == 1:
        merkle_proof.append(merkle_tree[0][random_indx-1])
    else:
        merkle_proof.append(merkle_tree[0][random_indx+1])
    sorted_pair = sorted([merkle_tree[0][random_indx], merkle_proof[0]])
    next_hash = hash_pair(sorted_pair[0], sorted_pair[1])
    last_layer = merkle_tree[0]
    next_layer = merkle_tree[1]
    cur_index = random_indx
    i = 0
    while len(next_layer)>1:
        i+=1
        index_of_hash = next_layer.index(next_hash)
        if index_of_hash % 2 == 1:
            merkle_proof.append(next_layer[index_of_hash-1])
            a = next_layer[index_of_hash-1]
            b = next_layer[index_of_hash]
        else:
            merkle_proof.append(next_layer[index_of_hash + 1])
            a = next_layer[index_of_hash]
            b = next_layer[index_of_hash+1]
        sorted_pair = sorted([a, b])
        next_hash = hash_pair(sorted_pair[0], sorted_pair[1])
        #if cur_index % 2 == 1:
        #    next_layer_index = int((cur_index-1)/2)
        #else:
        #    next_layer_index = int(cur_index / 2)
        #cur_layer_index = next_layer_index
        #cur_layer = merkle_tree[i]
        #cur_index = next_layer_index
        #bytes_pair = []
        #bytes_pair.append(cur_layer[cur_layer_index])
        #bytes_pair.append(cur_layer[cur_layer_index-1])
        #bytes_pair = sorted(bytes_pair)
        #sibling_hashes.append(bytes_pair)
        #last_layer = cur_layer
        next_layer = merkle_tree[i+1]
    #merkle_proof.append(bytes(merkle_tree[i+1][0])) #append root

    #print('stop')
    return merkle_proof


def sign_challenge(challenge):
    """
        Takes a challenge (string)
        Returns address, sig
        where address is an ethereum address and sig is a signature (in hex)
        This method is to allow the auto-grader to verify that you have
        claimed a prime
    """
    acct = get_account()

    addr = acct.address
    eth_sk = acct.key

    # TODO YOUR CODE HERE
    url = "https://eth-mainnet.g.alchemy.com/v2/FMNPnXuLyjNygdKSWThkEHGMyXg7ihZV"  # FILL THIS IN
    w3 = Web3(HTTPProvider(url))
    eth_sig_obj = w3.eth.account.sign_message(encode_defunct(text=challenge), private_key=eth_sk)
    #eth_sig_obj = 'placeholder'

    return addr, eth_sig_obj.signature.hex()


def send_signed_msg(proof, random_leaf):
    """
        Takes a Merkle proof of a leaf, and that leaf (in bytes32 format)
        builds signs and sends a transaction claiming that leaf (prime)
        on the contract
    """
    chain = 'bsc'

    acct = get_account()
    address, abi = get_contract_info(chain)
    w3 = connect_to(chain)

    # TODO YOUR CODE HERE
    contract = w3.eth.contract(address=address, abi=abi)

    string_of_hashes = []
    string_of_hashes.append(proof[0])
    next_hash = hash_pair(random_leaf, proof[0])
    string_of_hashes.append(next_hash)
    for j in range(1, len(proof)):
        sorted_pair = sorted([next_hash, proof[j]])
        prev_hash = next_hash
        next_hash = hash_pair(sorted_pair[0], sorted_pair[1])
        string_of_hashes.append(next_hash)

    tx_raw = contract.functions.submit(proof, random_leaf).build_transaction({
        #"proof": proof,
        #"leaf": random_leaf,
        #"to": contract.address,
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),

    })
    url = "https://data-seed-prebsc-1-s1.binance.org:8545/"  # FILL THIS IN
    w3 = Web3(HTTPProvider(url))
    signed_tx = w3.eth.account.sign_transaction(tx_raw, private_key=acct.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash


# Helper functions that do not need to be modified
def connect_to(chain):
    """
        Takes a chain ('avax' or 'bsc') and returns a web3 instance
        connected to that chain.
    """
    if chain not in ['avax','bsc']:
        print(f"{chain} is not a valid option for 'connect_to()'")
        return None
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc"  # AVAX C-chain testnet
    else:
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/"  # BSC testnet
    w3 = Web3(Web3.HTTPProvider(api_url))
    # inject the poa compatibility middleware to the innermost layer
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    return w3


def get_account():
    """
        Returns an account object recovered from the secret key
        in "sk.txt"
    """
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir.joinpath('sk.txt'), 'r') as f:
        sk = f.readline().rstrip()
    if sk[0:2] == "0x":
        sk = sk[2:]
    return eth_account.Account.from_key(sk)


def get_contract_info(chain):
    """
        Returns a contract address and contract abi from "contract_info.json"
        for the given chain
    """
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir.joinpath("contract_info.json"), "r") as f:
        d = json.load(f)
        d = d[chain]
    return d['address'], d['abi']


def sign_challenge_verify(challenge, addr, sig):
    """
        Helper to verify signatures, verifies sign_challenge(challenge)
        the same way the grader will. No changes are needed for this method
    """
    eth_encoded_msg = eth_account.messages.encode_defunct(text=challenge)

    if eth_account.Account.recover_message(eth_encoded_msg, signature=sig) == addr:
        print(f"Success: signed the challenge {challenge} using address {addr}!")
        return True
    else:
        print(f"Failure: The signature does not verify!")
        print(f"signature = {sig}\naddress = {addr}\nchallenge = {challenge}")
        return False


def hash_pair(a, b):
    """
        The OpenZeppelin Merkle Tree Validator we use sorts the leaves
        https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/MerkleProof.sol#L217
        So you must sort the leaves as well

        Also, hash functions like keccak are very sensitive to input encoding, so the solidity_keccak function is the function to use

        Another potential gotcha, if you have a prime number (as an int) bytes(prime) will *not* give you the byte representation of the integer prime
        Instead, you must call int.to_bytes(prime,'big').
    """
    if a < b:
        return Web3.solidity_keccak(['bytes32', 'bytes32'], [a, b])
    else:
        return Web3.solidity_keccak(['bytes32', 'bytes32'], [b, a])


if __name__ == "__main__":
    merkle_assignment()
