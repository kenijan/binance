import os
import tempfile
import subprocess
from binance.client import Client
from price import BinancePrice
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def decode_escapes(s):
    if s is None:
        return ""
    return s.encode('utf-8').decode('unicode_escape')

# Colors
YELLOW = decode_escapes(os.getenv("YELLOW"))
BLUE   = decode_escapes(os.getenv("BLUE"))
RED    = decode_escapes(os.getenv("RED"))
GREEN  = decode_escapes(os.getenv("GREEN"))
RESET  = decode_escapes(os.getenv("RESET"))

class BinanceAccount:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        self.price_checker = BinancePrice(api_key, api_secret)

    def get_account_info(self):
        try:
            account_info = self.client.get_account()
            balances = account_info['balances']
            filtered = []

            for bal in balances:
                asset = bal['asset']
                free = float(bal['free'])
                locked = float(bal['locked'])

                if free == 0 and locked == 0:
                    continue

                if asset.startswith("LD") and len(asset) > 2:
                    asset = asset[2:]

                # USDT value calculation
                if asset == 'USDT':
                    total_usdt = free + locked
                else:
                    symbol = asset + 'USDT'
                    try:
                        price = self.price_checker.get_current_price(symbol)
                        total_usdt = price * (free + locked) if price else 0
                    except Exception:
                        total_usdt = 0

                filtered.append((asset, free, locked, total_usdt))

            return filtered

        except Exception as e:
            print(f"{RED}⚠️ Failed to fetch account info: {str(e)}{RESET}")
            return []

    def get_api_trading_status(self):
        try:
            return self.client.get_api_trading_status()
        except Exception as e:
            print(f"{RED}⚠️ Failed to get API trading status: {str(e)}{RESET}")
            return {}

    def get_account_snapshot(self):
        try:
            return self.client.get_account_snapshot(type='SPOT')
        except Exception as e:
            print(f"{RED}⚠️ Failed to get account snapshot: {str(e)}{RESET}")
            return {}

    def display_balances_fancy(self, balances):
        print(f"\n{GREEN}=== Your Account Balances ==={RESET}")
        print(f"\n{YELLOW}📦 Wallet Overview:{RESET}")
        print(f"{'-'*77}")
        print(f"{BLUE} {'Asset':<10} {'Free Balance':>20} {'Locked Balance':>20} {'USDT Value':>20}{RESET}")
        print(f"{'-'*77}")

        total_portfolio = 0
        for asset, free, locked, usdt_value in balances:
            total_portfolio += usdt_value
            print(
                f"  {BLUE}{asset:<10}{RESET} "
                f"{GREEN}{free:>20,.8f}{RESET} "
                f"{RED}{locked:>20,.8f}{RESET} "
                f"{YELLOW}{usdt_value:>20,.2f}{RESET}"
            )

        print(f"{'-'*77}")
        print(f"{YELLOW}Total Portfolio Value (USDT):{GREEN} {total_portfolio:,.2f}{RESET}")

    def display_balances_html(self, balances):
        account_info = self.client.get_account()
        uid = account_info.get('uid', 'N/A')
        html = f"""
        <html>
        <head><title>Binance Portfolio {uid}</title>
        """
        html += """<style>
    body {
        font-family: Arial;
        margin: 30px;
        background-color: #f9f9f9;
    }

    h2 {
        color: #f3ba2f; /* Binance yellow */
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    th, td {
        border: 1px solid #ccc;
        padding: 8px;
        text-align: center;
    }

    th {
        background-color: #eee;
    }

    tr:nth-child(odd) {
        background-color: #f2f2f2; /* Light gray for even rows */
    }
</style>
        </head>
        <body>"""
        html += f"""
            <h2>Binance Wallet Overview {uid}</h2>
            <table>
                <tr><th>Asset</th><th>Free Balance</th><th>Locked</th><th>USDT Value</th></tr>
        """

        total = 0
        for asset, free, locked, usdt in balances:
            html += f"<tr><td>{asset}</td><td>{free:,.8f}</td><td>{locked:,.8f}</td><td>{usdt:,.2f}</td></tr>\n"
            total += usdt

        html += f"""</table>
        <h3>Total Portfolio Value: {total:,.2f} USDT</h3>
        </body></html>
        """

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as f:
            f.write(html)
            html_path = f.name

        try:
            subprocess.run(['termux-open', html_path], check=True)
        except Exception as e:
            print(f"{RED}⚠️ Couldn't open browser automatically: {str(e)}{RESET}")
            print(f"{GREEN}✅ File saved at: {html_path} — open it manually if needed.{RESET}")