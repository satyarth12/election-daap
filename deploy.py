import json
from web3 import Web3
from web3 import contract
from web3.contract import ConciseContract

ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

print(web3.isConnected())

default_account = "0x6BA0C6D52831dCc4D21a0D932574748E9512e2aD"
private_key =  "7a4dfac01d753f96bc56acf792b4a1f92389e70595f59618fcc75bf6de444b46"

'''
Compiling the smart contracts with truffle first
'''
truffle_file = json.load(open('./build/contracts/Election.json'))
abi =  truffle_file['abi']
print(abi)
bytecode = truffle_file['bytecode']
contract = web3.eth.contract(bytecode=bytecode, abi=abi)

'''
Building transaction for the contract
'''
txn = contract.constructor().buildTransaction({
    'from': default_account,
    'nonce': web3.eth.get_transaction_count(default_account),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei')
})

sign_txn = web3.eth.account.sign_transaction(txn, private_key)
txn_hash = web3.eth.send_raw_transaction(sign_txn.rawTransaction)
print(web3.toHex(txn_hash))
txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
print("Contract Deployed At:", txn_receipt['contractAddress'])


'''
Storing the Contract Address and Abi into a json file
'''
with open("elections/contract_source.json", "w") as outfile:
    dictionary = {
        'abis': abi,
        'contractAddress': txn_receipt['contractAddress']
    }
    json.dump(dictionary, outfile, indent=4)


print(contract.all_functions())