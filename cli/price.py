from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
import os

load_dotenv()


def decode_escapes(s):
    if s is None:
        return ""
    return s.encode('utf-8').decode('unicode_escape')


YELLOW = decode_escapes(os.getenv("YELLOW"))
BLUE   = decode_escapes(os.getenv("BLUE"))
RED    = decode_escapes(os.getenv("RED"))
GREEN  = decode_escapes(os.getenv("GREEN"))
RESET  = decode_escapes(os.getenv("RESET"))


class BinancePrice:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_symbol(self):
        while True:
            try:
                base = input(f"{YELLOW}📥 Enter coin symbol (e.g., BTC): {RESET}").strip().upper()
                if not base:
                    print(f"{RED}🚫 Symbol cannot be empty. Please try again.{RESET}")
                    continue

                quote = input(f"{YELLOW}💱 Enter quote currency (default is USDT): {RESET}").strip().upper()
                if not quote:
                    quote = "USDT"

                symbol = base + quote
                return symbol, quote

            except Exception as e:
                print(f"{RED}⚠️ Unknown Error: {str(e)}{RESET}")

    def get_current_price(self, symbol, quote='USDT'):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            print(f"{RED}🚫 Binance API Error: {e.message}{RESET}")
            return None
        except Exception as e:
            print(f"{RED}⚠️ Unknown Error: {str(e)}{RESET}")
            return None

    def display_price(self, price, symbol, quote='USDT'):
        if price is None:
            print(f"{RED}⚠️ Could not retrieve price for {symbol}.{RESET}")
        else:
            formatted = f"{price:,.10f}".rstrip("0").rstrip(".")
            print(f"\n{YELLOW}📈 Current Price for {BLUE}{symbol}{YELLOW}:")
            print(f"{GREEN}💰 {formatted} {quote}{RESET}\n")