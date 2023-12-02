# Investor and Account Data Loading Readme

This set of Python scripts is designed to simulate the creation and loading of investor, account, and stock ownership data into a Redis database. Follow the detailed instructions below to execute each script and understand their functionalities.

## Prerequisites

### Redis Server

Ensure that a Redis server is installed and running on your localhost. If Redis is hosted elsewhere or has non-default configurations, adjust the `redis_host` and `redis_port` variables in the scripts accordingly.

## Script Descriptions and Instructions

### 1. `load_investor_account_data.py`

#### Purpose:

This script generates random investor data along with associated accounts and loads them into the Redis database.

#### Instructions:

1. **Configuration:**
   - Adjust the `config.json` file to configure the total number of investors (`total_investors`) if needed.

2. **Execution:**
   - Run the script:
     ```bash
     python load_investor_account_data.py
     ```

3. **Output:**
   - The script will print the total number of investors created and the total number of accounts created.

### 2. `load_security_lot.py`

#### Purpose:

This script generates random stock ownership data for each account and establishes relationships between accounts and stock ownership.

#### Instructions:

1. **Prerequisites:**
   - Ensure that `load_investor_account_data.py` has been executed to create investor and account data.

2. **Execution:**
   - Run the script:
     ```bash
     python load_security_lot.py
     ```

3. **Output:**
   - The script will print messages when stock ownership data is loaded for each account.

### 3. `brokerage_query_simulation.py`

#### Purpose:

This script simulates querying investor, account, and stock ownership data from Redis using username-based indexing.

#### Instructions:

1. **Prerequisites:**
   - Ensure that both `load_investor_account_data.py` and `load_security_lot.py` have been executed.

2. **Execution:**
   - Run the script:
     ```bash
     python brokerage_query_simulation.py
     ```

3. **Output:**
   - The script will print the queried account and stock ownership data for a sample username and the time taken for the query.

## Important Notes:

- These scripts provide a simulated environment using random data for testing purposes.
  
- Ensure that Redis is running and accessible from the scripts.

- You can explore and modify the scripts based on your specific requirements or integrate them into a larger system.

- For any issues or additional details, refer to the official [Redis documentation](https://redis.io/documentation).

