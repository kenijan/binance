# price.py

from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv

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

    def get_current_price(self, base, quote='USDT'):
        try:
            symbol = f"{base.upper()}{quote.upper()}"
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price']), symbol
        except BinanceAPIException as e:
            return None, f"🚫 Binance API Error: {e.message}"
        except Exception as e:
            return None, f"⚠️ Unknown Error: {str(e)}"

    def format_price(self, price, symbol, quote='USDT'):
        if price is None:
            return f"⚠️ Could not retrieve price for {symbol}."
        else:
            formatted = f"{price:,.10f}".rstrip("0").rstrip(".")
            return (
                f"📈 Current Price for {symbol}:\n"
                f"💰 {formatted} {quote}"
            )