import sys
import time
from config import SYMBOL, GRID_SIZE, INVESTMENT_PERCENTAGE, BUY_THRESHOLD, SELL_THRESHOLD, STOP_LOSS_PRICE, PRICE_RANGE_PERCENTAGE
from utils import calculate_order_quantity, place_buy_order, place_sell_order, get_market_price, fetch_balance, calculate_dynamic_price_range, display_grid_metrics
from termcolor import colored

# Store grid trade metrics
grid_metrics = []

def run_grid_bot():
    """Main function to run the grid trading bot."""
    print(colored("Starting the Binance Grid Trading Bot...", 'blue'))
    
    # Get current market price
    current_price = get_market_price(SYMBOL)
    print(colored(f"Starting price: {current_price}", 'yellow'))

    # Dynamically calculate lower and upper price range based on current market price
    lower_price, upper_price = calculate_dynamic_price_range(current_price, PRICE_RANGE_PERCENTAGE)
    print(colored(f"Lower Price for Grid: {lower_price}", 'magenta'))
    print(colored(f"Upper Price for Grid: {upper_price}", 'magenta'))

    # Place the initial buy order at the start price
    buy_price = current_price
    place_buy_order(SYMBOL, buy_price, INVESTMENT_PERCENTAGE)

    # Add the buy order details to the grid metrics
    grid_metrics.append({
        "buy_price": buy_price,
        "sell_price": None,
        "profit_loss": None,
        "status": "Buy Order Placed"
    })

    grid_count = 1  # Starting grid count
    last_buy_price = buy_price  # Initialize last buy price for percentage-based trading

    # Main loop for monitoring and placing buy/sell orders
    while True:
        current_price = get_market_price(SYMBOL)
        sys.stdout.write("\033[F")  # Moves the cursor up to overwrite the previous line
        print(colored(f"Current Market Price: {current_price}", 'yellow'))

        # Dynamically update lower and upper prices as market price changes
        lower_price, upper_price = calculate_dynamic_price_range(current_price, PRICE_RANGE_PERCENTAGE)

        # Check if the price dropped enough to place a new buy order
        if (last_buy_price - current_price) / last_buy_price >= BUY_THRESHOLD:
            print(colored(f"Price dropped by {BUY_THRESHOLD * 100}% from {last_buy_price}. Buying more...", 'green'))
            last_buy_price = current_price  # Update the last buy price to current price
            place_buy_order(SYMBOL, current_price, INVESTMENT_PERCENTAGE)
            grid_count += 1

            # Add the buy order details to the grid metrics
            grid_metrics.append({
                "buy_price": current_price,
                "sell_price": None,
                "profit_loss": None,
                "status": "Buy Order Placed"
            })

        # Check if the price has increased enough to sell
        if (current_price - last_buy_price) / last_buy_price >= SELL_THRESHOLD:
            print(colored(f"Price increased by {SELL_THRESHOLD * 100}% from {last_buy_price}. Selling for profit...", 'red'))
            quantity_to_sell = calculate_order_quantity(current_price, INVESTMENT_PERCENTAGE)
            place_sell_order(SYMBOL, current_price, quantity_to_sell)

            # Update grid metrics with the sell order
            grid_metrics[-1]["sell_price"] = current_price
            grid_metrics[-1]["profit_loss"] = round((current_price - grid_metrics[-1]["buy_price"]) / grid_metrics[-1]["buy_price"] * 100, 2)
            grid_metrics[-1]["status"] = "Sell Order Placed"

            # Reset last buy price
            last_buy_price = current_price

        # Stop-Loss Check (if market price is lower than stop-loss price)
        if current_price <= STOP_LOSS_PRICE:
            print(colored(f"Stop-Loss Triggered! Market price is below the stop-loss threshold of {STOP_LOSS_PRICE}.", 'red'))
            break

        # Display live grid metrics after each cycle
        display_grid_metrics(grid_metrics)

        # Sleep before checking again
        time.sleep(60)  # Check market price every minute

if __name__ == '__main__':
    run_grid_bot()
