import requests
import json
import os

def pin_to_ipfs(data):

	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
	headers = {
		"pinata_api_key": '762ac7e9496097ca686a',
		"pinata_secret_api_key": '69eb5d1b961580285fac48d08f0475d2bfdd5ccbf77864458fae5ae5edf8ba38',
		"Content-Type": "application/json"
	}

	response = requests.post(url, data=json.dumps(data), headers=headers)
	cid = response.json()['IpfsHash']
	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE
	url = f"https://ipfs.io/ipfs/{cid}"
	response = requests.get(url)
	data = response.json()
	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data


if __name__ == "__main__":

	test_dict = {1:'one', 2:'two', 3:'three'}
	cid = pin_to_ipfs(test_dict)
	data = get_from_ipfs(cid, content_type="json")
