#!/usr/bin/bash
# Get all account keys
account_keys=$(redis-cli keys "account:*")

# Iterate through each account key
for key in $account_keys; do
  # Check if the key has_stock_ownership field
  has_stock_ownership=$(redis-cli hget "$key" "has_stock_ownership")

  # Print the result
  if [ -n "$has_stock_ownership" ]; then
    echo "Account key: $key, has_stock_ownership: $has_stock_ownership"
  else
    echo "Account key: $key does not have has_stock_ownership field"
  fi
done
