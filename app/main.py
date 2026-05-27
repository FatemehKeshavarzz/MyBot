from flask import Flask, request, jsonify
from binance.client import Client
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY, API_SECRET)

# IMPORTANT
client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

symbol = "BTCUSDT"
leverage = 10
quantity = 0.001

# =========================
# LOGGING SETUP
# =========================
logging.basicConfig(
    filename="webhook_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

print(f"Leverage set")

# Set leverage
client.futures_change_leverage(
    symbol=symbol,
    leverage=leverage
)

print(f"Bot started with leverage set to {leverage}x")

def open_long():
    order = client.futures_create_order(
        symbol=symbol,
        side="BUY",
        type="MARKET",
        quantity=quantity
    )
    print("OPEN LONG")
    logging.info("OPEN LONG executed")
    
    return order

def open_short():
    order = client.futures_create_order(
        symbol=symbol,
        side="SELL",
        type="MARKET",
        quantity=quantity
    )
    print("OPEN SHORT")
    logging.info("OPEN SHORT executed")
    
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
            logging.info("CLOSE LONG executed")

        elif amt < 0:
            # close short
            client.futures_create_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quantity=abs(amt)
            )
            print("CLOSE SHORT")
            logging.info("CLOSE SHORT executed")

@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.get_json(force=True)

    print("Webhook received:", data)
    
    logging.info(f"Webhook received: {data}")
    logging.info(f"Headers: {dict(request.headers)}")
    logging.info(f"Raw body: {request.data}")

    value = float(data["test"])

    # Close existing position first
    close_position()

    # Trading logic
    if value > 1:
        open_long()
        
        logging.info(f"LONG opened | value={value}")
        
        return jsonify({
            "message": "LONG opened",
            "value": value
        })

    elif value < 1:
        open_short()
        
        logging.info(f"SHORT opened | value={value}")

        return jsonify({
            "message": "SHORT opened",
            "value": value
        })

    logging.info(f"No trade | value={value}")

    return jsonify({
        "message": "No trade",
        "value": value
    })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)