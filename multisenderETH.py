from web3 import Web3
from colorama import init, Fore
import time

# Initialize Web3 with provider
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/[your id]'))
starting_private_key = '[your private key]'
starting_address = w3.eth.account.from_key(starting_private_key).address

# List of addresses and corresponding amounts
recipients = {
    '0xa77fecc8060b42b7b5b1a4b3001fc4951588a429': 0.02,
    '0xe2bed6673b3335c4e7ccc214fc19a580a99168ba': 0.015,
    '0x2c18b6bf5cdf6aa7f8db7e247251484baa34f290': 0.012,
    '0x45794954665ea80cfd0ec69cc3a8b84dd734dbcf': 0.001,
    '0xf0acf595deecdd362c63bacc02e5e19b7eb0fcf8': 0.002,
}

# Function to send ETH
def send_eth(from_address, to_address, private_key, value):
    # Get balance of the account
    balance = w3.eth.get_balance(from_address)

    if balance <= 0:
        raise ValueError(f"No funds available in account {from_address}.")

    # Set gas limit and gas price
    gas_limit = 21000
    gas_price = w3.eth.gas_price

    # Increase gas price
    gas_price = int(gas_price * 1.2)

    # Calculate gas cost
    gas_cost = gas_limit * gas_price

    # Calculate value to send
    value_to_send = w3.to_wei(value, 'ether')

    if value_to_send + gas_cost > balance:
        raise ValueError(f"{Fore.RED}Insufficient funds for gas fee in account {from_address}.")

    nonce = w3.eth.get_transaction_count(from_address)

    # Create transaction
    transaction = {
        'to': to_address,
        'value': value_to_send,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': 11155111  # Chain ID for Sepolia
    }

    print(f"Transaction to be sent: {transaction}")

    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)  # Corrected line

    time.sleep(5)  # Wait for transaction to complete
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"{Fore.YELLOW}Transaction {tx_hash.hex()}{Fore.LIGHTMAGENTA_EX} successful!")
    except Exception as e:
        raise ValueError(f"Transaction {tx_hash.hex()} not found or failed: {str(e)}")

# Sending ETH to all addresses in the list
for recipient, amount in recipients.items():
    try:
        print(f"{Fore.CYAN} Sending {amount} ETH from {starting_address} to {recipient}...")
        send_eth(starting_address, w3.to_checksum_address(recipient), starting_private_key, amount)
    except ValueError as e:
        print(f"Error: {e}. Retrying in 10 seconds...")
        time.sleep(10)

print(f"{Fore.LIGHTRED_EX} THE END ")
