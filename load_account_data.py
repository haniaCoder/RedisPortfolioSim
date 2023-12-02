# =============================================
# load_account_data.py
# Created by Hania Guiagoussou on 11/01/23.
# =============================================

"""
This Python script harnesses the capabilities of the Redis database to simulate a dynamic financial environment, complete with the generation, management, and retrieval of investor and account data. The script's functionality is outlined as follows:

1. **Connection to Redis:** The script initiates a connection to the local Redis server by specifying the host and port.

2. **Configuration Loading:** Configuration parameters are loaded from a JSON file, providing flexibility in adjusting simulation settings.

3. **Investor Data Generation:** Utilizing the `names` library, the script creates random investor data, including unique identifiers, full names, and email-like usernames. The uniqueness of investor IDs is ensured to prevent duplication.

4. **Bulk Data Insertion:** A Redis list (`investor_keys_list`) is employed to track investor keys. The script utilizes a pipeline to execute bulk data insertion efficiently, enhancing the overall performance of these operations.

5. **Account Data Association:** Random account data is generated and associated with investors, ensuring the uniqueness of account IDs. The script maintains a set to track existing account IDs and facilitates the creation of a specified number of unique accounts per investor.

6. **Index Utilization:** The script effectively utilizes Redis indexes for optimized data retrieval. It leverages the Redis `rpush` command to maintain a list of investor keys, facilitating quick access to investor information.

7. **Informative Output:** The script provides informative output, including the total number of investors and accounts created. This feedback aids in monitoring the progress of the financial simulation.

This financial simulation script exemplifies the seamless integration of Redis, showcasing its efficiency in managing dynamic data structures essential for simulating realistic financial scenarios. The strategic use of indexes further enhances the script's performance by enabling swift data retrieval.
"""


import redis
import random
import json
import names

# Connect to the Redis server
redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Load configuration from a JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Use configuration values
total_investors = config.get('total_investors', 1000)

# Array of random domain names
domains = ["gmail.com", "yahoo.com",
           "icloud.com", "hotmail.com", "outlook.com"]

# Function to generate random investor data with email-like usernames


def generate_random_investor(existing_ids):
    investor_id = None
    while investor_id is None or investor_id in existing_ids:
        investor_id = f"INV-{random.randint(10000, 99999)}"
    existing_ids.add(investor_id)

    full_name = names.get_full_name()
    domain = random.choice(domains)
    username = f"{full_name.split()[0].lower()}_{
        full_name.split()[1].lower()}@{domain}"

    return {
        "id": investor_id,
        "name": full_name,
        "uid": f"UID-{random.randint(10000, 99999)}",
        "username": username
    }


# Create and load random investor data into Redis
investor_keys_list = "investor_keys"
existing_investor_ids = set()

# Bulk data to be set in Redis
bulk_data = []

# Ensure exactly total_investors are created
while len(existing_investor_ids) < total_investors:
    investor_data = generate_random_investor(existing_investor_ids)
    investor_key = f"investor:{investor_data['id']}"

    # Add investor key to the list
    r.rpush(investor_keys_list, investor_key)

    # Append investor data to the bulk_data list
    bulk_data.append((investor_key, investor_data))

# Use pipeline to execute bulk operations in a single round trip
with r.pipeline() as pipe:
    for key, data in bulk_data:
        pipe.hset(key, mapping=data)
    pipe.execute()

print(f"Total number of investors created: {len(existing_investor_ids)}")

# Count the number of accounts created
num_accounts_created = 0

# Set to track existing account IDs
existing_account_ids = set()

# Function to generate a single random account data associated with an investor


def generate_random_account(investor_id):
    global num_accounts_created
    account_id = None
    while account_id is None or account_id in existing_account_ids:
        account_id = f"ACC-{random.randint(1000, 9999)}"
    existing_account_ids.add(account_id)

    account_number = f"ACC-NO-{random.randint(10000, 99999)}"
    balance = round(random.uniform(1000, 10000), 2)
    num_accounts_created += 1
    return {
        "id": account_id,
        "account_number": account_number,
        "name": f"Account of {investor_id}",
        "balance": balance,
        "belongs_to_investor": investor_id
    }


# Create and load random account data associated with investors
for investor_key in r.lrange(investor_keys_list, 0, -1):
    investor_id = investor_key.split(":")[1]
    account_data = generate_random_account(investor_id)
    account_key = f"account:{account_data['id']}"
    r.hset(account_key, mapping=account_data)

# Print the number of accounts created
print(f"Total number of accounts created: {num_accounts_created}")
print("All Investor and Account Information:")
print("Data loading complete.")
