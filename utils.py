import sys
from binance.client import Client
from config import API_KEY, API_SECRET, INVESTMENT_PERCENTAGE, PRICE_RANGE_PERCENTAGE
from termcolor import colored
from prettytable import PrettyTable

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Try to fetch the balance of USDT (or another asset if preferred)
try:
    balance = client.get_asset_balance('USDT')
    print(f"USDT Balance: {balance}")
except Exception as e:
    print(f"Error: {e}")

def fetch_balance(symbol='USDT'):
    """Fetch the balance of the provided symbol (e.g., USDT)."""
    balance = client.get_asset_balance(asset=symbol)
    return float(balance['free']) if balance else 0.0

def calculate_order_quantity(price, percentage_of_balance):
    """Calculate how much of the asset to buy/sell based on percentage of available balance."""
    available_balance = fetch_balance('USDT')  # Default to USDT for calculating
    order_value = available_balance * percentage_of_balance
    quantity = order_value / price
    return round(quantity, 3)

def place_buy_order(symbol, price, percentage_of_balance):
    """Place a limit buy order at the specified price."""
    quantity = calculate_order_quantity(price, percentage_of_balance)
    order = client.order_limit_buy(
        symbol=symbol,
        quantity=quantity,
        price=str(round(price, 2))
    )
    print(colored(f"Buy Order placed at {price} for {quantity} {symbol[:3]}", 'green'))
    return order

def place_sell_order(symbol, price, quantity):
    """Place a limit sell order at the specified price."""
    order = client.order_limit_sell(
        symbol=symbol,
        quantity=quantity,
        price=str(round(price, 2))
    )
    print(colored(f"Sell Order placed at {price} for {quantity} {symbol[:3]}", 'red'))
    return order

def get_market_price(symbol):
    """Get the current market price of the symbol."""
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def calculate_dynamic_price_range(current_price, percentage_buffer):
    """Dynamically calculate the lower and upper price based on the current market price."""
    lower_price = current_price * (1 - percentage_buffer)
    upper_price = current_price * (1 + percentage_buffer)
    return lower_price, upper_price

def display_grid_metrics(grid_metrics):
    """Display grid metrics in a nice table format and overwrite the previous output."""
    table = PrettyTable()
    table.field_names = ["Grid #", "Buy Price", "Sell Price", "Profit/Loss (%)", "Status"]
    
    for i, metric in enumerate(grid_metrics):
        table.add_row([i+1, metric["buy_price"], metric["sell_price"], metric["profit_loss"], metric["status"]])

    # Clear previous output and print the updated table
    sys.stdout.write("\033[F" * len(grid_metrics))  # Move the cursor up to overwrite previous rows
    print(table)
