import json
import os

wallet_path = "wallet_data.json"

def get_wallet():
    if not os.path.exists(wallet_path):
        with open(wallet_path, "w") as f:
            json.dump({}, f)
    with open(wallet_path) as f:
        return json.load(f)

def update_balance(source, amount):
    data = get_wallet()
    data[source] = data.get(source, 0) + amount
    with open(wallet_path, "w") as f:
        json.dump(data, f)
