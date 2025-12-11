# help.py
class Help:
    @staticmethod
    async def show_help(update):
        help_text = (
          "📚 *CryptoPilot Help Menu*\n\n"
          "*Available commands:*\n"
            "/start      - Start the bot\n"
            "/users      - Change User\n"
            "/help       - Show this help message\n"
            "/account    - View Binance account balances\n"
            "/price <SYMBOL> - Get current price for SYMBOL (e.g., BTC)\n"
            "/buy        - Place a buy order (coming soon)\n"
            "/sell       - Place a sell order (coming soon)\n\n"
          "For any questions, contact @kenijan."
          )
        await update.message.reply_text(help_text, parse_mode='Markdown')