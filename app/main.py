from binance.client import Client
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY, API_SECRET)

# IMPORTANT
client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

symbol = "BTCUSDT"
leverage = 10
quantity = 0.001

print(f"Leverage set")

# Set leverage
client.futures_change_leverage(
    symbol=symbol,
    leverage=leverage
)

print(f"Leverage set to {leverage}x")

print("Bot started with 10x leverage")

def open_long():
    order = client.futures_create_order(
        symbol=symbol,
        side="BUY",
        type="MARKET",
        quantity=quantity
    )
    print("OPEN LONG")
    return order

def open_short():
    order = client.futures_create_order(
        symbol=symbol,
        side="SELL",
        type="MARKET",
        quantity=quantity
    )
    print("OPEN SHORT")
    return order

def close_position():
    # This closes BOTH long or short depending on position size
    positions = client.futures_position_information(symbol=symbol)

    for p in positions:
        amt = float(p["positionAmt"])

        if amt > 0:
            # close long
            client.futures_create_order(
                symbol=symbol,
                side="SELL",
                type="MARKET",
                quantity=abs(amt)
            )
            print("CLOSE LONG")

        elif amt < 0:
            # close short
            client.futures_create_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quantity=abs(amt)
            )
            print("CLOSE SHORT")

while True:

    # STEP 1: open long
    open_long()
    time.sleep(60)

    # STEP 2: close
    close_position()
    time.sleep(2)

    # STEP 3: open short
    open_short()
    time.sleep(60)

    # STEP 4: close
    close_position()
    time.sleep(2)