# 📊 Suite Diamond Telegram Scanner Bot

Automated Telegram bot that scans 500+ tickers for **Green X** (bullish) and **Red X** (bearish) signals based on your TradingView Suite Diamond strategy.

## 🎯 Features

- **Daily Signal Scanning**: Scans 500 tickers in 1-2 minutes
- **Telegram Commands**: Control everything from your phone
- **Green X Detection**: Bullish reversals (8/21 EMA crossover)
- **Red X Detection**: Bearish reversals (8/21 EMA crossunder)
- **Volume Sorting**: Shows most liquid stocks first
- **Price & Change**: Real-time price data with daily % change

## 🚀 Quick Start

### Step 1: Create Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` to BotFather
3. Choose a name (e.g., "My Diamond Scanner")
4. Choose a username (e.g., "my_diamond_scanner_bot")
5. BotFather will give you a **token** like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. **Save this token** - you'll need it in Step 3

### Step 2: Install Python Dependencies

```bash
cd telegram_scanner
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8 or higher
- pip (Python package manager)

### Step 3: Configure Your Bot Token

**Option A: Environment Variable (Recommended)**
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

**Option B: Edit the File**
Open `telegram_bot.py` and replace line 13:
```python
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
```
Change to:
```python
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your actual token
```

### Step 4: Start the Bot

```bash
python telegram_bot.py
```

You should see:
```
🤖 Bot is starting...
📡 Press Ctrl+C to stop the bot
```

### Step 5: Use the Bot

1. Open Telegram
2. Search for your bot username (e.g., `@my_diamond_scanner_bot`)
3. Click "Start" or send `/start`
4. Use commands below!

## 📱 Telegram Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and help |
| `/help` | Show all available commands |
| `/scan_bullish` | Find all **GREEN X** signals today |
| `/scan_bearish` | Find all **RED X** signals today |
| `/scan_all` | Find both GREEN and RED X signals |
| `/test SYMBOL` | Test a specific ticker (e.g., `/test AAPL`) |

## 🧪 Example Usage

### Scan for Bullish Signals
```
You: /scan_bullish
Bot: 🔍 Scanning 500 tickers for GREEN X signals...

🟢 GREEN X SIGNALS TODAY 🟢
Found 12 fresh signals:

1. AAPL
   💵 $175.43 📈 +2.34%
   📊 Vol: 54,234,567

2. NVDA
   💵 $495.22 📈 +1.87%
   📊 Vol: 42,123,456
...
```

### Test Single Ticker
```
You: /test TSLA
Bot: 🔍 Testing TSLA...

TSLA

💵 Price: $242.84
📊 Change: +3.21%
📈 Volume: 123,456,789

🟢 GREEN X SIGNAL TODAY ✓

🕐 2025-12-21 16:45:32
```

## 🔧 Customization

### Add More Tickers

Edit `tickers.txt` and add symbols (one per line):
```
AAPL
TSLA
NVDA
...
```

### Change Timeframe

Edit `scanner.py` line 164 to change from daily to hourly:
```python
# Change from:
interval = timeframe  # Default '1d'

# To:
interval = '1h'  # For hourly scans
```

### Modify Signal Logic

The Suite Diamond logic is in `scanner.py`, function `detect_suite_diamond_signals()`:

```python
# Current logic matches your Pine Script:
# Fast EMA: 8 periods
# Slow EMA: 21 periods
# Signal SMA: 5 periods

# Green X = EMA crossover (bullish)
# Red X = EMA crossunder (bearish)
```

## 📅 Automated Daily Scans

To automatically scan every day at market close, use a scheduler:

### Linux/Mac (crontab)

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 4:15 PM EST
15 16 * * 1-5 cd /path/to/telegram_scanner && python telegram_bot.py --auto-scan
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 4:15 PM
4. Action: Start Program → `python.exe`
5. Arguments: `/path/to/telegram_bot.py`

## 🌐 Hosting Options

### Option 1: Run on Your Computer
- Pros: Free, full control
- Cons: Computer must stay on

### Option 2: VPS (Recommended)
- **DigitalOcean**: $6/month
- **Linode**: $5/month
- **AWS EC2 Free Tier**: Free for 12 months

Setup on VPS:
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip

# Clone your files
cd /home/ubuntu
# Upload telegram_scanner folder

# Install dependencies
cd telegram_scanner
pip3 install -r requirements.txt

# Run bot in background
nohup python3 telegram_bot.py &
```

### Option 3: Railway/Render (Free Tier)
- Upload code to GitHub
- Connect to Railway/Render
- Set environment variable `TELEGRAM_BOT_TOKEN`
- Deploy!

## 🐛 Troubleshooting

### "No module named 'telegram'"
```bash
pip install -r requirements.txt
```

### "ERROR: Please set your TELEGRAM_BOT_TOKEN"
- Make sure you replaced the token in Step 3
- Check for typos in your token

### "Scan takes too long"
- Normal! 500 tickers = 1-2 minutes
- Reduce ticker list in `tickers.txt` for faster scans

### "No signals found"
- Normal on quiet days
- Try `/test AAPL` to verify bot is working
- Check TradingView to confirm signals exist

## 📊 How It Works

### Suite Diamond Logic

```
1. Calculate 8 EMA (fast)
2. Calculate 21 EMA (slow)
3. MACD = fast_ema - slow_ema
4. Signal = 5 SMA of MACD

Green X = MACD crosses ABOVE signal
Red X = MACD crosses BELOW signal
```

This matches your TradingView Pine Script exactly:
```pine
suiteFastEma = emaCalc(close, 8)
suiteSlowEma = emaCalc(close, 21)
suiteMacd = suiteFastEma - suiteSlowEma
suiteSignal = smaCalc(suiteMacd, 5)

suiteBlueDiamond = ta.crossover(suiteMacd, suiteSignal)
suitePinkDiamond = ta.crossunder(suiteMacd, suiteSignal)
```

## 📝 Files Overview

```
telegram_scanner/
├── telegram_bot.py      # Main bot (handles commands)
├── scanner.py           # Signal detection logic
├── tickers.txt          # List of 500 symbols to scan
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 💡 Pro Tips

1. **Start Small**: Test with `/test AAPL` before full scans
2. **Best Time**: Scan after market close (4:00-5:00 PM EST)
3. **Filter by Volume**: Bot shows highest volume first
4. **Daily Routine**: Run `/scan_bullish` every evening
5. **Combine with TradingView**: Verify signals on charts before trading

## 🔒 Security

- **Never share your bot token** publicly
- Use environment variables for tokens
- Run bot on trusted servers only
- Your ticker list is local (not shared)

## 📞 Support

Having issues? Check:
1. Python version: `python --version` (should be 3.8+)
2. Dependencies installed: `pip list | grep telegram`
3. Token is correct: Check BotFather message
4. Bot is running: Should show "Bot is starting..."

## 📜 License

Free to use for personal trading. Not financial advice!

---

**Built with:**
- Python 3.9+
- python-telegram-bot 21.0
- yfinance (market data)
- pandas & numpy (calculations)

**Based on your TradingView Suite Diamond Strategy**

🚀 Happy Trading!
