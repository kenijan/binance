from binance.client import Client
import logging

class BinanceAccount:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
    
    def get_balances(self):
      try:
        account_info = self.client.get_account()
        logging.info("✅ Account info fetched")
        balances = {}
        for asset in account_info['balances']:
            free_amount = float(asset['free'])
            locked_amount = float(asset['locked'])
            total = free_amount + locked_amount
            if total > 0:
                balances[asset['asset']] = total
        logging.info(f"✅ Balances: {balances}")
        return balances
      except Exception as e:
        logging.error(f"❌ Error fetching balances: {e}")
        return {}
if __name__ == "__main__":
    from keys import user_keys
    user = "kenu"
    key, secret = user_keys[user]
    print(f"Testing API Key: {key}")
    acc = BinanceAccount(key, secret)
    balances = acc.get_balances()
    print("Balances:", balances)