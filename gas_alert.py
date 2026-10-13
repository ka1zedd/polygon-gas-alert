import os 
import time 
import requests

POLYGON_RPC = "https://polygon-bor-rpc.publicnode.com"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GAS_LIMIT_GWEI = 350
CHECK_INTERVAL = 30  

def get_gas_price(): 
    payload = { "jsonrpc": "2.0", 
                "method": "eth_gasPrice", 
                "params": [], 
                "id": 1 
    }
    response = requests.post(
        POLYGON_RPC,
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    gas_wei = int(data["result"], 16)
    gas_gwei = gas_wei / 1_000_000_000

    return gas_gwei

def send_telegram_message(message):
    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(
        url,
        data=data,
        timeout=10
       
    )

    response.raise_for_status()

def main():
    print("Polygon Gas Alert started.")

    alert_sent = False

    while True:

        try:

            gas = get_gas_price()

            print(f"Current Polygon Gas: {gas:.2f} Gwei")

        # اگر گس به 100 یا کمتر رسید
            if gas <= GAS_LIMIT_GWEI and not alert_sent:

                message = (
                "🚨 Polygon Gas Alert!\n\n"
                f"Gas Price: {gas:.2f} Gwei\n"
                f"Threshold: {GAS_LIMIT_GWEI} Gwei"
                )

                send_telegram_message(message)

                print("Telegram notification sent.")

                alert_sent = True

        # وقتی دوباره گس بالا رفت،
        # آماده هشدار بعدی شو
            elif gas > GAS_LIMIT_GWEI:

                alert_sent = False

        except Exception as error:

            print("Error:", error)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__": 
    main()
