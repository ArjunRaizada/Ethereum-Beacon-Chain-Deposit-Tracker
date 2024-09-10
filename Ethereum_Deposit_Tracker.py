# Importing necessary libraries
import requests
import os
from dotenv import load_dotenv, dotenv_values
from web3 import Web3
import pymongo
from datetime import datetime

load_dotenv()

# Initilizing our MongoDB Database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Luganodes"]
collection = db["Ethereum1"]

# Alchemy API URL
alchemy_url = os.getenv("ALCHEMY")
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check connection
if web3.is_connected():
    print("Connected to Ethereum node")
else:
    print("Failed to connect")
    exit()

# Beacon Deposit Contract address and ABI
contract_address = os.getenv("BEACON")
abi = '''
[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
 {"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes","name":"pubkey","type":"bytes"},
                             {"indexed":false,"internalType":"bytes","name":"withdrawal_credentials","type":"bytes"},
                             {"indexed":false,"internalType":"bytes","name":"amount","type":"bytes"},
                             {"indexed":false,"internalType":"bytes","name":"signature","type":"bytes"},
                             {"indexed":false,"internalType":"bytes","name":"index","type":"bytes"}],
  "name":"DepositEvent","type":"event"},
 {"inputs":[{"internalType":"bytes","name":"pubkey","type":"bytes"},
           {"internalType":"bytes","name":"withdrawal_credentials","type":"bytes"},
           {"internalType":"bytes","name":"signature","type":"bytes"},
           {"internalType":"bytes32","name":"deposit_data_root","type":"bytes32"}],
  "name":"deposit","outputs":[],"stateMutability":"payable","type":"function"},
 {"inputs":[],"name":"get_deposit_count","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],
  "stateMutability":"view","type":"function"},
 {"inputs":[],"name":"get_deposit_root","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],
  "stateMutability":"view","type":"function"},
 {"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],
  "name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"}]
'''

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Signature of the DepositEvent
deposit_event_signature = web3.keccak(text="DepositEvent(bytes,bytes,bytes,bytes,bytes)").hex()
Deposits = []

# Setting up Telegram Bot
TOKEN = os.getenv("TOKEN")
chat_id = os.getenv("ID")


##Defining Necessary Functions

# for sending notification to telegram
def send_notification(block_no, timestamp, fee, hash, pubkey, amt):
    message = f"Transaction has been made\n\nBlock Number : {block_no}\nTimestamp : {timestamp}\nFee : {fee}\nHashkey : {hash}\nAmount : {amt} ETH\nPubkey: {pubkey}\n\nFor more details click here : https://etherscan.io/block/{block_no}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()  # this sends the message
    pass


# for getting deposit logs from each block
def get_deposit_logs(start_block, end_block):
    try:
        # Ensure that start_block is not negative
        if start_block < 0:
            start_block = 0

        filter_params = {
            'fromBlock': start_block,
            'toBlock': end_block,
            'address': contract_address,
        }

        print(f"Fetching logs from block {start_block}...")
        logs = web3.eth.get_logs(filter_params)
        return logs

    # Error handling
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []


def process_deposits():
    latest_block = web3.eth.get_block('latest')['number']
    logs = get_deposit_logs(latest_block, latest_block)

    for log in logs:
        try:
            decoded_event = contract.events.DepositEvent().process_log(log)
            pubkey = decoded_event['args']['pubkey']
            withdrawal_credentials = decoded_event['args']['withdrawal_credentials']
            amount = int.from_bytes(decoded_event['args']['amount'], "big") / 10 ** 18  # Convert wei to ETH
            signature = decoded_event['args']['signature']
            index = decoded_event['args']['index']

            # Sending Notification to Telegram regarding received a Transaction
            send_notification(block_no=latest_block,
                              timestamp=datetime.utcfromtimestamp(web3.eth.get_block('latest')['timestamp']).strftime(
                                  '%Y-%m-%d %H:%M:%S'), fee=amount, hash=web3.eth.get_block('latest')['hash'].hex(),
                              pubkey=pubkey.hex(), amt=amount)

            print(f"New deposit detected!")
            print(f"  PubKey: {pubkey.hex()}")
            print(f"  Withdrawal Credentials: {withdrawal_credentials.hex()}")
            print(f"  Amount: {amount} ETH")
            print(f"  Signature: {signature.hex()}")
            print(f"  Index: {index.hex()}")

        #Error handling
        except Exception as e:
            print(f"Error processing log: {e}")

        dep = {
            "block number": latest_block,
            "block_time_stamp": f"{web3.eth.get_block('latest')['timestamp']}",
            "gas_fee": web3.eth.gas_price,
            "Hash": web3.eth.get_block('latest')['hash'].hex(),
            "Pubkey": pubkey.hex(),
            "Withdrawal Credentials": withdrawal_credentials.hex(),
            "Amount": amount,
            "Index": index.hex(),
            "Signature": signature.hex(),
        }

        # Inserting this dep dictionary in the MongoDB database
        collection.insert_one(dep)


# will be used later to prevent redundancy in the blocks being captured
prev_block = web3.eth.get_block('latest')['number']

# This makes the program run continuously and check for new blocks
while True:
    latest_block = web3.eth.get_block('latest')['number']
    if prev_block != latest_block:
        process_deposits()
        prev_block = latest_block
