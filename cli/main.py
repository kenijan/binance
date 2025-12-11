import os
import sys
import time
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceOrderException
from account import BinanceAccount
from price import BinancePrice
from keys import user_keys
from Help import Help

# Load colors from .env
load_dotenv()

def decode_escapes(s):
    return s.encode('utf-8').decode('unicode_escape')

YELLOW = decode_escapes(os.getenv("YELLOW"))
BLUE = decode_escapes(os.getenv("BLUE"))
RED = decode_escapes(os.getenv("RED"))
GREEN = decode_escapes(os.getenv("GREEN"))
RESET = decode_escapes(os.getenv("RESET"))

current_user = None
binance_account = None
price_checker = None

def progressLoader(delay):
    for i in range(21):
        print(f"\r🔄 Loading: [{'#'*i:<20}] {i*5}%", end='', flush=True)
        time.sleep(delay)
    print()

def banner():
    # You can put ASCII art or logo here
    print(f"{GREEN}Welcome to Binance Terminal{RESET}")

def choose_user():
    global current_user, binance_account, price_checker
    while True:
        print(f"\n{YELLOW}  🔑 Available Users:{RESET}")
        for i, user in enumerate(user_keys.keys(), start=1):
            print(f"   {BLUE}[{i}] {user}{RESET}")
        choice = input(f"{YELLOW} Enter user name or number: {RESET}").strip()

        # Match by number
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(user_keys):
                current_user = list(user_keys.keys())[index]
            else:
                print(f"{RED}❌ Invalid number.{RESET}")
                continue
        elif choice in user_keys:
            current_user = choice
        else:
            print(f"{RED}❌ Invalid username.{RESET}")
            continue

        # Load API keys
        api_key = user_keys[current_user]['api']
        api_secret = user_keys[current_user]['key']
        binance_account = BinanceAccount(api_key, api_secret)
        price_checker = BinancePrice(api_key, api_secret)
        print(f"{GREEN}✅ Logged in as {current_user} - UID: {binance_account.client.get_account().get('uid', 'Unknown')}{RESET}")
        break

def show_menu():
    print(f"\n🧾 {YELLOW}Binance API OPTIONS for {current_user}:{RESET}")
    menulist = [
        'Account Info',
        'Get Current Price',
        'UI View',
        'Buy Order',
        'Sell Order',
        'Order Status',
        'Order History',
        'Available Trading Pairs',
        'Withdrawal (external only)',
        'Change User',
        'Exit'
    ]
    for i, option in enumerate(menulist, 1):
        print(f"   {BLUE}[{i}] {option}{RESET}")

if "--help" in sys.argv:
    Help.show_help()

if __name__ == "__main__":
    try:
        os.system('clear')
        banner()
        choose_user()

        while True:
            show_menu()
            try:
                option = int(input("Choose an option: "))

                if option == 1:
                    progressLoader(0.05)
                    balances = binance_account.get_account_info()
                    if not balances:
                        print("No balances found.")
                    else:
                        binance_account.display_balances_fancy(balances)

                elif option == 2:
                    progressLoader(0.03)
                    symbol, quote = price_checker.get_symbol()
                    price = price_checker.get_current_price(symbol, quote)
                    if price:
                        price_checker.display_price(price, symbol, quote)

                elif option == 3:
                    progressLoader(0.03)
                    balances = binance_account.get_account_info()
                    if balances:
                        binance_account.display_balances_html(balances)
                    else:
                        print(f"{RED}❌ No balances found.{RESET}")

                elif option == 9:
                    choose_user()

                elif option == 10:
                    print(f"{GREEN}Exiting...{RESET}")
                    break

                else:
                    print(f"{RED}Option {option} not implemented yet.{RESET}")

            except BinanceAPIException as e:
                print(f"🚫 {RED}Binance API Error: {e.message}{RESET}")

            except BinanceOrderException as e:
                print(f"🚫 {RED}Binance Order Error: {e.message}{RESET}")

            except ValueError:
                print(f"{RED}Please enter a valid number.{RESET}")

            except Exception as e:
                print(f"⚠️ {YELLOW}Unknown Error: {str(e)}{RESET}")

            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n\n🚫 {RED} Ctrl + C is disabled. Restarting...{RESET}")
        progressLoader(0.5)
        os.execv(sys.executable, [' '] + sys.argv)