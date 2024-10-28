from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time
from connect_to_eth import connect_to_eth

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)
DELAY = 5
#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
#with open('/home/codio/workspace/abi.json', 'r') as f:
with open('abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = 'https://ipfs.io/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq'#YOU WILL NEED TO TO PROVIDE THE URL OF AN ETHEREUM NODE
#provider = HTTPProvider(api_url)
#web3 = Web3(provider)

web3 = connect_to_eth()

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	data = {'owner': "", 'image': "", 'eyes': "" }
	
	#YOUR CODE HERE
	response = requests.get(api_url+"//"+str(apeID))
	data_obj = response.json()

	contract = web3.eth.contract(address=contract_address, abi=abi)
	owner = contract.functions.ownerOf(apeID).call()
	image = data_obj['image']
	for attribute in data_obj['attributes']:
		if attribute['trait_type']=='Eyes':
			eyes = attribute['value']

	data['owner'] =  owner
	data['image'] = image
	data['eyes'] =  eyes
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

get_ape_info(5)