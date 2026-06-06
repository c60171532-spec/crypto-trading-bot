import requests
import json
import os

# Live Price Fetch karne ka function
def get_live_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url).json()
        return float(response['price'])
    except Exception as e:
        print(f"⚠️ Price fetch error: {e}")
        return None

DATA_FILE = "wallet.json"

# 🌟 CRASH-PROOF WALLET LOADER
def load_wallet():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            print("⚠️ Wallet file corrupt thi, reset kar rahe hain.")
            
    # Agar file nahi hai ya kharab hai, toh default create karo aur save karo
    default_wallet = {"balance": 1000.0, "crypto_held": 0.0, "buy_price": 0.0}
    save_wallet(default_wallet)
    return default_wallet

# 🌟 CRASH-PROOF WALLET SAVER
def save_wallet(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("💾 Wallet state securely saved on disk.")
    except Exception as e:
        print(f"❌ Wallet save error: {e}")

def main():
    print("🤖 AUTO-PILOT CRYPTO TRADING BOT ACTIVE...")
    print("------------------------------------------")
    
    # Wallet load hotay hi file automatic ban jaye gi
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
        # Profit target: 0.5% gain
        target_price = bought_at * 1.005 
        
        print(f"📌 Entry Price: ${bought_at} | Target to Sell: ${target_price:.2f}")
        
        if current_price >= target_price:
            print("🔥 TARGET HIT! Selling for profit...")
            profit_cash = wallet['crypto_held'] * current_price
            
            wallet['balance'] = profit_cash
            wallet['crypto_held'] = 0.0
            wallet['buy_price'] = 0.0
            save_wallet(wallet)
            print(f"🏆 Profit Booked! New Balance: ${profit_cash:.2f}")
        else:
            print("⏳ Market abhi target tak nahi pohnchi. HODL (Wait) kar rahe hain...")

    print("------------------------------------------")
    print("🏁 Run complete. System automatically 30 mins baad dubara check karega.")

if __name__ == "__main__":
    main()
