import json
from datetime import datetime, timezone
from pathlib import Path

import requests


RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)  


def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
        "include_last_updated_at": "true"
    }

    print("Calling CoinGecko API...")
    print("   URL:", url)
    print("   Params:", params)

    try:
        resp = requests.get(url, params=params, timeout=30)

        
        print("✅ Response received!")
        print("   Status code:", resp.status_code)

        
        resp.raise_for_status()

        data = resp.json()
        print(" JSON parsed successfully!")
        print("   Data:", data)

        return data

    except requests.exceptions.RequestException as e:
        print(" API request failed.")
        print("   Error:", e)
        return None


def save_raw_json(payload):

    if payload is None:
        print(" Nothing to save because payload is None.")
        return

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = RAW_DIR / f"coingecko_raw_{ts}.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(" Raw JSON saved successfully!")
    print("   Saved at:", out_path)


if __name__ == "__main__":

    data = fetch_prices()
    save_raw_json(data)
