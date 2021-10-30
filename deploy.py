from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# takes compiled_sol json and dump it into file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# to deploy a contract, you need the bytecode and the ABI

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337 # ganache known issue, use 1337 instead of 5777 for now, 30 Oct 2021
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"  # fake address
private_key = os.getenv("PRIVATE_KEY")  # fake private key

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# Send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# at this point, once you run deploy.py, there will be a transacion made in ganache
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# working with the contract -> we need address and ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> simulate making the call and getting a return value
# Transact -> actually make a state change

# Initial value of fav number
print("Initial: ", simple_storage.functions.retrieve().call())
print("Updating contract...")

store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1 #nonce can only be used once in each transaction, so we gotta +1
})
signed_stored_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_stored_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx) # instead of contract creation in ganache, we have a Contract Call

print("Updated: ", simple_storage.functions.retrieve().call())

# ran ganache-cli --deterministic, update localhost, first eth address and private key, run python deploy.py on another terminal

# how to deploy to testnet? in Remix, all we need to do is change env to Injected Web3
# we can check out and use Infura.io, swap our localhost address, chain id and private key to test on rinkeby
