# =============================================
# brokerage_query_simulation.py
# Created by Hania Guiagoussou on 11/01/23.
# =============================================

"""
This Python script demonstrates the retrieval of investor data, including account information and associated stock ownership data, from a Redis database. The script's functionality is elucidated as follows:

1. **Connection to Redis:** The script establishes a connection to the local Redis server, specifying the host and port.

2. **Investor Data Query Function:** The primary function, `query_investor_data`, accepts a username as a parameter and initiates the process of querying investor data.

3. **Querying Investor ID:** The script utilizes a Redis index to query the investor's ID based on the provided username. This is achieved by using the `get` method on the Redis key composed of the username and the term ':usernames'. If a valid investor ID is retrieved, the script proceeds to the next step.

4. **Querying Associated Accounts:** The script employs another Redis index to retrieve all account keys associated with the investor. It utilizes the `keys` method, searching for keys with a pattern of 'account:{investor_id}*'. These keys represent accounts linked to the investor, and the script iterates through them to fetch the associated account data.

5. **Displaying Account and Stock Ownership Data:** For each account, the script queries and displays detailed account information using the `hgetall` method. Subsequently, it uses the index stored in the account data to fetch and display stock ownership data.

6. **Output for Nonexistent Investor:** If no investor is found for the provided username, a corresponding message is printed to inform the user.

7. **Query Execution Time Calculation:** The script calculates and prints the elapsed time taken for the entire query operation, providing insights into the efficiency of the data retrieval process.

8. **Example Query:** The script includes an example query using the username 'john_doe' to simulate the process of querying data for a specific investor.

This script showcases the practical usage of Redis indexes to swiftly and efficiently retrieve investor data, exemplifying its capabilities in handling real-time queries within a financial context.
"""

import redis
import time

# Connect to the Redis server
redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


def query_investor_data(username):
    start_time = time.time()

    # Query investor ID by username using the index
    investor_id = r.get(f"{username}:usernames")

    if investor_id:
        # Query all accounts associated with the investor using the index
        account_keys = r.keys(f"account:{investor_id}*")

        for account_key in account_keys:
            # Query account data
            account_data = r.hgetall(account_key)
            print(f"Account Data for {username}: {account_data}")

            # Query stock ownership data for the account using the index
            stock_ownership_id = r.hget(account_key, "has_stock_ownership_id")
            stock_ownership_data = r.hgetall(stock_ownership_id)
            print(
                f"Stock Ownership Data for {username}: {stock_ownership_data}")

    else:
        print(f"No investor found with username: {username}")

    end_time = time.time()
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60

    print(
        f"\nQuery completed in {elapsed_time_seconds:.4f} seconds ({elapsed_time_minutes:.4f} minutes)")


# Example: Simulate querying data for a specific username
sample_username = "john_doe"
query_investor_data(sample_username)
