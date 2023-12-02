# =============================================
# load_security_lot.py
# Created by Hania Guiagoussou on 11/01/23.
# =============================================

"""
This Python script leverages the Redis database to simulate stock ownership data within a financial environment. The script's functionality is delineated as follows:

1. **Connection to Redis:** The script initiates a connection to the local Redis server by specifying the host and port.

2. **Stock Data Definition:** Specific stock data, including symbols, company names, prices, and identifiers, is defined as a list of dictionaries (`stocks`).

3. **Stock Ownership Generation:** For each account, the script generates random stock ownership data. This involves randomly selecting a subset of stocks, determining the number of shares owned, and introducing a realistic 5% price variation for each stock.

4. **Security Lot Creation:** The script creates security lots for each stock, assigning unique IDs, recording tickers, prices, quantities, and acquisition dates (in Unix-style format).

5. **Redis Data Loading:** The generated stock ownership data is associated with each account in Redis. The relationship is established by linking the account to its stock ownership data and creating a unique identifier for the stock ownership information.

6. **Account Information Retrieval Using Indexes:** To efficiently retrieve account information, the script utilizes Redis indexes. When querying for account data, the script first retrieves the investor's ID by using a Redis index associated with the username. Once the investor's ID is obtained, the script queries for all accounts associated with that investor using another Redis index. This indexing approach significantly accelerates the retrieval process, demonstrating the power of Redis in handling relational data.

7. **Informative Output:** The script provides feedback for each account, confirming the successful loading of stock ownership data into Redis. This feedback assists in monitoring the progress of the stock ownership simulation.

This simulation script exemplifies the capability of Redis to efficiently handle complex financial data structures, providing a foundation for realistic simulations.
"""

# Rest of your code...

import redis
import random
import names
import json
import time

# Connect to the Redis server
redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Define specific stock data
stocks = [
    {"symbol": "AAPL", "company_name": "Apple Inc.", "price": 173.97,
        "id": "AAPL123", "code": "AAPL123", "active": True},
    {"symbol": "TSLA", "company_name": "Tesla, Inc.", "price": 205.66,
        "id": "TSLA123", "code": "TSLA123", "active": True},
    {"symbol": "AMZN", "company_name": "Amazon.com, Inc.", "price": 137.00,
        "id": "AMZN123", "code": "AMZN123", "active": True},
    {"symbol": "MSFT", "company_name": "Microsoft Corporation",
        "price": 346.07, "id": "MSFT123", "code": "MSFT123", "active": True},
    {"symbol": "JPM", "company_name": "J.P. Morgan Chase & Co.",
        "price": 138.94, "id": "JPM123", "code": "JPM123", "active": True},
    {"symbol": "BAC", "company_name": "Bank of America Corporation",
        "price": 26.40, "id": "BAC123", "code": "BAC123", "active": True},
    {"symbol": "GOOG", "company_name": "Alphabet Inc.", "price": 2791.50,
        "id": "GOOG123", "code": "GOOG123", "active": True},
    {"symbol": "FB", "company_name": "Meta Platforms, Inc.",
        "price": 330.25, "id": "FB123", "code": "FB123", "active": True},
    {"symbol": "NFLX", "company_name": "Netflix, Inc.", "price": 651.40,
        "id": "NFLX123", "code": "NFLX123", "active": True},
    {"symbol": "GE", "company_name": "General Electric Co.",
        "price": 102.40, "id": "GE123", "code": "GE123", "active": True},
    {"symbol": "GLSR", "company_name": "Glossier, Inc.", "price": 45.75,
        "id": "GLSR123", "code": "GLSR123", "active": True},
    {"symbol": "NKE", "company_name": "Nike, Inc.", "price": 159.32,
        "id": "NKE123", "code": "NKE123", "active": True},
    {"symbol": "COST", "company_name": "Costco Wholesale Corporation",
        "price": 550.33, "id": "COST123", "code": "COST123", "active": True},
    {"symbol": "V", "company_name": "Visa Inc.", "price": 250.11,
        "id": "V123", "code": "V123", "active": True},
    {"symbol": "IBM", "company_name": "International Business Machines Corporation",
        "price": 120.15, "id": "IBM123", "code": "IBM123", "active": True},
    {"symbol": "T", "company_name": "AT&T Inc.", "price": 26.78,
        "id": "T123", "code": "T123", "active": True},
    {"symbol": "KKD", "company_name": "Krispy Kreme Doughnuts, Inc.",
        "price": 20.45, "id": "KKD123", "code": "KKD123", "active": True},
    {"symbol": "TGT", "company_name": "Target Corporation",
        "price": 240.50, "id": "TGT123", "code": "TGT123", "active": True},
    {"symbol": "IN-N-OUT", "company_name": "In-N-Out Burger",
        "price": 15.99, "id": "INO123", "code": "INO123", "active": True},
    {"symbol": "UPS", "company_name": "United Parcel Service, Inc.",
        "price": 207.64, "id": "UPS123", "code": "UPS123", "active": True},
]

# Function to generate random stock ownership for an account


def generate_stock_ownership(account_id):
    stock_ownership = {}
    security_lots = []

    # Randomly determine the number of different companies the account holds stocks in
    num_companies = random.randint(1, len(stocks))
    # Randomly select a subset of companies
    selected_companies = random.sample(stocks, num_companies)

    for stock in selected_companies:
        variation = random.uniform(-5, 5)  # 5% price variation
        price = round(stock["price"] + (stock["price"] * variation / 100), 2)
        shares_owned = random.randint(1, 100)

        # Create a Security Lot with acquired_date
        security_lot = {
            "id": f"SEC-{random.randint(10000, 99999)}",
            "ticker": stock["symbol"],
            "price": price,
            "quantity": shares_owned,
            "acquired_date": int(time.time())  # Unix-style date format
        }
        security_lots.append(security_lot)

    stock_ownership["security_lots"] = security_lots
    return stock_ownership


print("(load_security_lot.py) Generating stock ownership data for each account loading them into redis ....")
# Load stock ownership data for each account
for account_key in r.keys("account:ACC-*"):
    account_id = account_key.split(":")[1]
    stock_ownership_data = generate_stock_ownership(account_id)

    # Establish the relationship between account and stock ownership
    r.hset(account_key, "has_stock_ownership",
           json.dumps(stock_ownership_data))

    # Establish a relationship between account and stock ownership by ID
    stock_ownership_id = f"stock_ownership:{account_id}"
    r.hset(account_key, "has_stock_ownership_id", stock_ownership_id)
    print(f"Stock ownership data loaded for {account_key}")
