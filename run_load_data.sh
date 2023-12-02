#!/usr/bin/bash

echo "STEP 1: Deleting flushing database...."

# Specify your Redis server host and port
REDIS_HOST="localhost"
REDIS_PORT=6379
redis-cli -h $REDIS_HOST -p $REDIS_PORT flushall
echo "Redis database flushed."

echo "STEP 2: Generating & Loading Investors & Accounts....."
python3 load_account_data.py

echo "STEP 3: Generating & Loading Security Lots....."
python3 load_security_lot.py


