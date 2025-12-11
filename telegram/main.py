import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
from account import BinanceAccount
from price import BinancePrice
from Help import Help
from keys import user_keys

# Load environment variables
load_dotenv()

# Constants
CHOOSE_USER = 1

# Setup logging
logging.basicConfig(level=logging.INFO)

# Unicode escape decoding
def decode_escapes(s):
    return s.encode('utf-8').decode('unicode_escape')

# Colors
YELLOW = decode_escapes(os.getenv("YELLOW"))
BLUE   = decode_escapes(os.getenv("BLUE"))
RED    = decode_escapes(os.getenv("RED"))
GREEN  = decode_escapes(os.getenv("GREEN"))
RESET  = decode_escapes(os.getenv("RESET"))

# Globals
current_user = None
binance_account = None
price_fetcher = None

#   Handlers  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"👋 Welcome to CryptoPilot Terminal Bot!\n"
        f"🧑‍💼 Current User: `{current_user}`\n"
        f"Type /help to see available commands.\n"
        f"Use /users to switch Binance user."
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_list = "\n".join([f"{i+1}. {u}" for i, u in enumerate(user_keys.keys())])
    await update.message.reply_text(
        f"🔐 Available Users:\n{user_list}\n\nPlease reply with a username or number:"
    )
    return CHOOSE_USER

async def select_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_user, binance_account, price_fetcher

    user_input = update.message.text.strip()
    selected_key = None

    if user_input.isdigit():
        idx = int(user_input) - 1
        if 0 <= idx < len(user_keys):
            selected_key = list(user_keys.keys())[idx]
    elif user_input in user_keys:
        selected_key = user_input

    if selected_key:
        current_user = selected_key
        api_key, api_secret = user_keys[selected_key]
        binance_account = BinanceAccount(api_key, api_secret)
        price_fetcher = BinancePrice(api_key, api_secret)  # ✅ FIXED
        await update.message.reply_text(f"✅ User `{selected_key}` selected!", parse_mode='Markdown')
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Invalid selection. Please try again.")
        return CHOOSE_USER

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Help.show_help(update)

async def account_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if binance_account is None:
        await update.message.reply_text("❗ No user selected. Use /users to select a Binance user.")
        return
    
    balances = binance_account.get_balances()

    if not balances:
        await update.message.reply_text("⚠️ No balances found or error fetching them.")
        return

    def format_balance(b):
      s = f"{b:.8f}".rstrip('0').rstrip('.')
      return s if s else "0"
    reply = "📊 *Your Balances:*\n"
    for asset, balance in balances.items():
      clean_asset = asset.removeprefix("LD")
      formatted_balance = format_balance(balance)
      reply += f"🔹 {clean_asset}: {formatted_balance:>12}\n"
    
    await update.message.reply_text(reply, parse_mode='Markdown')

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if price_fetcher is None:
        await update.message.reply_text("❗ No user selected. Use /users to select a Binance user.")
        return
    if not context.args:
        await update.message.reply_text("❗ Usage: /price BTC")
        return
    symbol = context.args[0].upper()
    price, symbol_or_msg = price_fetcher.get_current_price(symbol)
    msg = price_fetcher.format_price(price, symbol_or_msg)
    await update.message.reply_text(msg)

async def signal_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Buy signal functionality coming soon!")

async def signal_sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Sell signal functionality coming soon!")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Unknown command. Use /help for options.")

#   Main  

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    # Set default user on startup
    if user_keys:
        default_user = list(user_keys.keys())[0]
        current_user = default_user
        api_key, api_secret = user_keys[default_user]
        binance_account = BinanceAccount(api_key, api_secret)
        price_fetcher = BinancePrice(api_key, api_secret)
        logging.info(f"✅ Default user '{default_user}' loaded.")
    else:
        logging.warning("⚠️ No users found in user_keys.")

    # Conversation handler for user selection
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("users", users)],
        states={
            CHOOSE_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_user)],
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("account", account_info))
    app.add_handler(CommandHandler("price", get_price))
    app.add_handler(CommandHandler("buy", signal_buy))
    app.add_handler(CommandHandler("sell", signal_sell))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logging.info("✅ Telegram bot started...")
    app.run_polling()