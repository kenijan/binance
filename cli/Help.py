import os
from dotenv import load_dotenv

# Load colors from .env
load_dotenv()
def decode_escapes(s):
    return s.encode('utf-8').decode('unicode_escape')

YELLOW = decode_escapes(os.getenv("YELLOW"))
BLUE = decode_escapes(os.getenv("BLUE"))
RED = decode_escapes(os.getenv("RED"))
GREEN = decode_escapes(os.getenv("GREEN"))
RESET = decode_escapes(os.getenv("RESET"))

class Help:
    @staticmethod
    def show_help():
        print(f"""
{YELLOW}🪪  CryptoPilot - Binance API Trading Terminal
📦  Version : 1.0.0
🧑  Author  : Kenijan
🏢  Company : TCL
{RESET}
Usage:{GREEN}
# 📦 Basic System Setup
  apt update && apt upgrade -y
  apt install  3 -y
  apt install  3-pip -y

# 📚 Install Required   Packages
  pip install requests
  pip install  -dotenv
  pip install binance

# 🚀 Run the App
    main.py
{RESET}
Description:{GREEN}
  CryptoPilot is a command-line tool for interacting with the Binance API.
  It allows you to view account info, check prices, place buy/sell orders,
  and manage trading accounts with multiple API keys.
{RESET}
Options Menu:{BLUE}
  [1] Account Info            - View your Binance account balances
  [2] Get Current Price       - Check current market prices
  [3] Buy Order               - Place a market buy order (coming soon)
  [4] Sell Order              - Place a market sell order (coming soon)
  [5] Order Status            - View status of an existing order (coming soon)
  [6] Order History           - Show recent trades or orders (coming soon)
  [7] Available Trading Pairs - List supported trading pairs (coming soon)
  [8] Withdrawal              - Withdraw crypto to an external wallet (coming soon)
  [9] Change User             - Switch to another Binance API account
 [10] Exit                    - Exit the terminal
{RESET}
Environment Setup:{YELLOW}
  🔐 Requires API key and secret for each user (from `keys.py` file)
  🎨 Uses color values from `.env` file
{RESET}
Tips:{BLUE}
  - To add users, edit the `keys.py` file and insert your API credentials.
  - Secure your keys and secrets. Never share your `keys.py` file publicly.
{RESET}
Need help?{BLUE}
  👉 Contact: kenijanvip@gmail.com
  👉 Telegram: @kenijan
""")
        print("\033[93mThis is yellow text\033[0m")
        exit()

# Example usage
if __name__ == "__main__":
    Help.show_help()