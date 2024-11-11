# config.py

# API Credentials
API_KEY = 'JEL7kt8ixm11zvou5Ky8w5xsLZi1zOOnvoMQiNFjfefcGSr2QQMQzAs8plzTTdPh'
API_SECRET = 'Amt1TcJ2aC09opU1SxTl9j5vt6GffTH19rKQuvngRRHjw28JJUdGSx20Z48mQvKG'

# Grid Trading Parameters
SYMBOL = 'BTCUSDT'  # Trading pair (e.g., Bitcoin/USDT)
GRID_SIZE = 10       # Number of grid levels (e.g., 10 levels)
INVESTMENT_PERCENTAGE = 0.50  # Percentage per trade (e.g., 10% of account balance)
BUY_THRESHOLD = 0.002  # 0.2% drop in price to trigger a buy
SELL_THRESHOLD = 0.04  # 0.3% increase in price to trigger a sell (for profits)

# Optional: Set the stop-loss price and sell percentage increment
STOP_LOSS_PRICE = 84000  # Stop loss price for safety
PRICE_RANGE_PERCENTAGE = 0.001  # Buffer percentage for lower and upper price (1%)
