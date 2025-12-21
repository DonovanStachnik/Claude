"""
Telegram Bot for Suite Diamond Signal Scanner
Responds to commands and scans tickers for Green X and Red X signals
"""

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from scanner import scan_all_tickers, format_results, scan_ticker
from datetime import datetime


# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TICKER_FILE = 'tickers.txt'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued"""
    welcome_message = """
🤖 *Suite Diamond Signal Scanner Bot*

I scan hundreds of tickers for fresh Green X and Red X signals!

*Available Commands:*
/scan\_bullish - Find all fresh GREEN X signals today
/scan\_bearish - Find all fresh RED X signals today
/scan\_all - Find both GREEN and RED X signals
/test <SYMBOL> - Test a specific ticker (e.g., /test AAPL)
/help - Show this message

*What are these signals?*
🟢 *GREEN X* = Bullish reversal (Suite Diamond crossover)
🔴 *RED X* = Bearish reversal (Suite Diamond crossunder)

Based on 8/21 EMA crossover system from your TradingView strategy.

_Note: Scans may take 1-2 minutes to complete._
    """
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN_V2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    await start(update, context)


async def scan_bullish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Scan for bullish (Green X) signals"""
    await update.message.reply_text("🔍 Scanning 500 tickers for GREEN X signals...\nThis may take 1-2 minutes...")

    try:
        # Run scan
        results = scan_all_tickers(
            ticker_file=TICKER_FILE,
            signal_type='bullish',
            timeframe='1d'
        )

        # Format and send results
        message = format_results(results, 'bullish')

        # Telegram has a 4096 character limit
        if len(message) > 4096:
            # Split into chunks
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(f"❌ Error during scan: {str(e)}")


async def scan_bearish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Scan for bearish (Red X) signals"""
    await update.message.reply_text("🔍 Scanning 500 tickers for RED X signals...\nThis may take 1-2 minutes...")

    try:
        # Run scan
        results = scan_all_tickers(
            ticker_file=TICKER_FILE,
            signal_type='bearish',
            timeframe='1d'
        )

        # Format and send results
        message = format_results(results, 'bearish')

        # Telegram has a 4096 character limit
        if len(message) > 4096:
            # Split into chunks
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(f"❌ Error during scan: {str(e)}")


async def scan_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Scan for both bullish and bearish signals"""
    await update.message.reply_text("🔍 Scanning 500 tickers for ALL signals...\nThis may take 1-2 minutes...")

    try:
        # Run scans for both
        bullish_results = scan_all_tickers(
            ticker_file=TICKER_FILE,
            signal_type='bullish',
            timeframe='1d'
        )

        bearish_results = scan_all_tickers(
            ticker_file=TICKER_FILE,
            signal_type='bearish',
            timeframe='1d'
        )

        # Format and send results
        bullish_message = format_results(bullish_results, 'bullish')
        bearish_message = format_results(bearish_results, 'bearish')

        combined_message = bullish_message + "\n\n" + "─" * 30 + "\n\n" + bearish_message

        # Handle message length
        if len(combined_message) > 4096:
            await update.message.reply_text(bullish_message, parse_mode=ParseMode.MARKDOWN)
            await update.message.reply_text(bearish_message, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(combined_message, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(f"❌ Error during scan: {str(e)}")


async def test_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test a specific ticker"""
    if not context.args:
        await update.message.reply_text("⚠️ Please provide a ticker symbol.\nExample: /test AAPL")
        return

    symbol = context.args[0].upper()
    await update.message.reply_text(f"🔍 Testing {symbol}...")

    try:
        result = scan_ticker(symbol, '1d')

        if result.get('error'):
            await update.message.reply_text(f"❌ Error: {result['error']}")
            return

        # Build message
        message = f"*{symbol}*\n\n"
        message += f"💵 Price: ${result['price']:.2f}\n"
        message += f"📊 Change: {result['change_pct']:+.2f}%\n"
        message += f"📈 Volume: {result['volume']:,}\n\n"

        if result['green_x_today']:
            message += "🟢 *GREEN X SIGNAL TODAY* ✓\n"
        elif result['current_green']:
            message += "🟢 Green X active (last 5 bars)\n"

        if result['red_x_today']:
            message += "🔴 *RED X SIGNAL TODAY* ✓\n"
        elif result['current_red']:
            message += "🔴 Red X active (last 5 bars)\n"

        if not result['green_x_today'] and not result['red_x_today'] and not result['current_green'] and not result['current_red']:
            message += "⚪ No active signals\n"

        message += f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def main():
    """Start the bot"""
    # Check if token is configured
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ ERROR: Please set your TELEGRAM_BOT_TOKEN environment variable")
        print("   or edit telegram_bot.py and replace 'YOUR_BOT_TOKEN_HERE' with your actual token")
        return

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("scan_bullish", scan_bullish))
    application.add_handler(CommandHandler("scan_bearish", scan_bearish))
    application.add_handler(CommandHandler("scan_all", scan_all))
    application.add_handler(CommandHandler("test", test_ticker))

    # Start bot
    print("🤖 Bot is starting...")
    print("📡 Press Ctrl+C to stop the bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
