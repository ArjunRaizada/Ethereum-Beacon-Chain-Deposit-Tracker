# Ethereum Beacon Chain Deposit Tracker

This project fetches deposit event logs from the Ethereum Beacon Chain, processes the deposit data, stores it in a MongoDB database, and sends notifications via Telegram whenever a deposit is detected.

## Prerequisites

Ensure you have the following installed on your system:

1. **Python 3.8+**
2. **MongoDB**
3. **Alchemy Account** (to access the Ethereum blockchain via an API key)
4. **Telegram Bot Token** (to send notifications)
5. **web3.py** library
6. **pymongo** library
7. **requests** library
8. **dotenv** library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Luganodes_Placement/ethereum-beacon-tracker.git
   cd ethereum-beacon-tracker
   ```

2. Install the necessary Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up a MongoDB instance on your local machine or server.

4. Create a `.env` file in the project directory to store environment variables:

   ```
   ALCHEMY=<Your Alchemy API Key>
   BEACON=<Beacon Chain Deposit Contract Address>
   TOKEN=<Your Telegram Bot Token>
   ID=<Your Telegram Chat ID>
   ```

## Usage

1. **Start the MongoDB server:**
   ```bash
   mongod --dbpath /path/to/your/mongodb/data
   ```

2. **Run the script:**
   ```bash
   python beacon_tracker.py
   ```

   The script will:

   - Continuously monitor the Ethereum Beacon Chain for new deposit events.
   - Process the deposit logs for each block.
   - Store the deposit information in a MongoDB database.
   - Send a notification to your Telegram bot when a new deposit is detected.

## Project Structure

- `beacon_tracker.py`: Main script for monitoring deposit events, storing them in MongoDB, and sending Telegram notifications.
- `.env`: Environment configuration file (not included in the repository, needs to be created).
- `README.md`: Project documentation.

## Functions

### `send_notification(block_no, timestamp, fee, hash, pubkey, amt)`
Sends a Telegram notification with details about a detected deposit event.

### `get_deposit_logs(start_block, end_block)`
Fetches logs from the specified block range on the Ethereum Beacon Chain.

### `process_deposits()`
Processes the fetched deposit logs and decodes them into readable data. Also stores this data in MongoDB and sends a notification via Telegram.

## Environment Variables

- **ALCHEMY**: Your Alchemy API URL for interacting with the Ethereum blockchain.
- **BEACON**: The Beacon Chain Deposit Contract address.
- **TOKEN**: The Telegram bot token for sending notifications.
- **ID**: The Telegram chat ID to which notifications should be sent.

## Sample Screenshots

- **TELEGRAM NOTIFICATIONS** 

<img src="https://github.com/user-attachments/assets/408daf6d-df32-4dff-adc7-c5ef957541ce" alt="IMG_0325" width="300"/>
<img src="https://github.com/user-attachments/assets/a8d0686e-7384-4bee-9822-36080d4e6d6e" alt="IMG_0324" width="300"/>

- **MONGO DB ENTRIES** 
<img src="https://github.com/user-attachments/assets/ca0d6caf-3439-4052-8281-f6c7844cfaa8" alt="IMG_0325" width="300"/>
<img src="https://github.com/user-attachments/assets/a756490f-cd42-4b23-9af8-ca858738466c" alt="IMG_0325" width="300"/>





## License

This project is open source.

## Authors
*Arjun Raizada*
