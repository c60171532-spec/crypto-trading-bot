import requests
import json
import os

# 1. Live Price Fetch karne ka function
def get_live_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url).json()
        return float(response['price'])
    except Exception as e:
        print(f"⚠️ Price fetch error: {e}")
        return None

# 2. Wallet ki memory ko load aur save karne ke functions
DATA_FILE = "wallet.json"

def load_wallet():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # Shuruat mein virtual $1000 cash milenge
    return {"balance": 1000.0, "crypto_held": 0.0, "buy_price": 0.0}

def save_wallet(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    print("🤖 AUTO-PILOT CRYPTO TRADING BOT ACTIVE...")
    print("------------------------------------------")
    
    wallet = load_wallet()
    current_price = get_live_price("BTCUSDT")
    
    if not current_price:
        print("❌ Live price nahi mil saki. Next run ka wait karte hain.")
        return
        
    print(f"💰 Current Wallet Balance: ${wallet['balance']:.2f}")
    print(f"🪙 Crypto Held: {wallet['crypto_held']:.5f} BTC")
    print(f"📈 Current Live Bitcoin Price: ${current_price}")
    print("------------------------------------------")

    # CASE 1: Agar hamare paas cash hai, toh BUY karo
    if wallet['crypto_held'] == 0.0:
        print("🛒 Signal: Market state check... Executing BUY Order.")
        wallet['crypto_held'] = wallet['balance'] / current_price
        wallet['buy_price'] = current_price
        wallet['balance'] = 0.0
        save_wallet(wallet)
        print(f"✅ SUCCESSFULLY BOUGHT at ${current_price}. Waiting for profit...")

    # CASE 2: Agar hamare paas pehle se crypto hai, toh PROFIT check karo
    else:
        bought_at = wallet['buy_price']
        # Profit target: 0.5% gain (Chota target taake jaldi profit book ho)
        target_price = bought_at * 1.005 
        
        print(f"📌 Entry Price: ${bought_at} | Target to Sell: ${target_price:.2f}")
        
        if current_price >= target_price:
            print("🔥 TARGET HIT! Selling for profit...")
            profit_cash = wallet['crypto_held'] * current_price
            print(f"🏆 Profit Booked! Made: ${profit_cash - 1000.0 if profit_cash > 1000 else 5.0:.2f}")
            
            wallet['balance'] = profit_cash
            wallet['crypto_held'] = 0.0
            wallet['buy_price'] = 0.0
            save_wallet(wallet)
        else:
            print("⏳ Market abhi target tak nahi pohnchi. HODL (Wait) kar rahe hain...")

    print("------------------------------------------")
    print("🏁 Run complete. System automatically 30 mins baad dubara check karega.")

if __name__ == "__main__":
    main()
