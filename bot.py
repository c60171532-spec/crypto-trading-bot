import requests
import time

# Live Crypto Price Fetcher (Binance Public API)
def get_live_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url).json()
        return float(response['price'])
    except Exception as e:
        print(f"⚠️ Price fetch error: {e}")
        return None

def main():
    print("🤖 DEMO CRYPTO TRADING BOT INITIALIZED...")
    print("------------------------------------------")
    
    # Fake/Demo Balance Simulator for safe learning
    demo_balance = 1000.0  # $1000 USDT Virtual Cash
    crypto_held = 0.0      # Shuruat mein hamare paas koi coin nahi hai
    buy_price = 0.0
    
    # Live market rate check karte hain
    current_price = get_live_price("BTCUSDT")
    if not current_price:
        return
        
    print(f"📈 Current Live Bitcoin Price: ${current_price}")
    
    # Simple Technical Strategy Simulator
    # Hum bot ko aik test standard target de rahe hain
    target_buy_signal = current_price - 50    # Agar rate $50 nichay gire toh buy kare
    target_sell_signal = current_price + 100  # Agar rate $100 upar jaye toh sell kare
    
    print(f"🎯 Strategy Configured -> Target Buy at: ${target_buy_signal} | Target Sell at: ${target_sell_signal}")
    print("------------------------------------------")
    
    # Simulation logic check
    print("🔄 Checking market movements...")
    time.sleep(2)
    
    # Fake Demo Trade Execute loop (Sample Run)
    if crypto_held == 0.0:
        print(f"🛒 SIMULATION: Market is low! Buying 1 Bitcoin at live rate: ${current_price}")
        crypto_held = demo_balance / current_price
        demo_balance = 0.0
        buy_price = current_price
        print(f"💰 Virtual Wallet Updated -> Balance: ${demo_balance} | Crypto Assets: {crypto_held:.5f} BTC")
        
    print("------------------------------------------")
    print("🏆 Bot executed successfully without any errors.")

if __name__ == "__main__":
    main()
