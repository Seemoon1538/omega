import os
from web3 import Web3 #Example for Ethereum
from dotenv import load_dotenv

load_dotenv() #Загружаем переменные окружения из .env файла

#Blockchain settings
BLOCKCHAIN_NODE_URL = os.environ.get('BLOCKCHAIN_NODE_URL')
PRIVATE_KEY = os.environ.get('BLOCKCHAIN_PRIVATE_KEY')


if not BLOCKCHAIN_NODE_URL or not PRIVATE_KEY:
    raise ValueError("BLOCKCHAIN_NODE_URL and BLOCKCHAIN_PRIVATE_KEY environment variables must be set.")



w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_NODE_URL))

#Check connection
if not w3.isConnected():
    raise ConnectionError("Failed to connect to the blockchain node.")

account = w3.eth.account.privateKeyToAccount(PRIVATE_KEY)
account_address = account.address



def get_balance(address):
    """Retrieves the balance of a given address."""
    balance = w3.eth.getBalance(address)
    return w3.fromWei(balance, 'ether')


def send_transaction(recipient, amount, data=None):
  """Sends a transaction to the specified recipient."""
  nonce = w3.eth.getTransactionCount(account_address)
  transaction = {
      'nonce': nonce,
      'to': recipient,
      'value': w3.toWei(amount, 'ether'),
      'gas': 21000, # Adjust as needed
      'gasPrice': w3.toWei('2', 'gwei'), # Adjust as needed
      'data': data or '',
  }

  signed_txn = account.signTransaction(transaction)
  tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
  return tx_hash.hex()


def deploy_contract(contract_interface, *args, **kwargs):
    """Deploys a smart contract."""
    contract = w3.eth.contract(**contract_interface)
    tx_hash = contract.constructor(*args, **kwargs).transact({'from': account_address})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    return contract_address



# Example of interacting with a deployed contract
def interact_with_contract(contract_address, contract_abi, function_name, *args, **kwargs):
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    tx_hash = getattr(contract, function_name)(*args, **kwargs).transact({'from': account_address})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt
