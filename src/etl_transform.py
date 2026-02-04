import json
from datetime import datetime, timezone
from pathlib import Path
CLEAN_DIR = Path("data/clean")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
raw_dir = Path("data/raw")
def get_latest_raw_file():
    files = sorted(raw_dir.glob("coingecko_raw_*.json"))
    if not files:
        raise FileNotFoundError("No raw files found in data/raw. Run etl_extract.py first.")
    return files[-1]
def load_raw_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
def transform_to_rows(raw_data: dict):
    rows = []
    for coin, values in raw_data.items():
        row = {"coin": coin, "currency": "usd", "price": values.get("usd"), "last_updated_at" : values.get("last_updated_at"),}
        rows.append(row)
    return rows
def save_clean_csv(rows: list[dict]):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = CLEAN_DIR/ f"crypto_prices_{ts}.csv"
    header = "coin,currency,price,last_updated_at\n"
    lines = [header]
    for r in rows:
        lines.append(f"{r['coin']},{r['currency']},{r['price']},{r['last_updated_at']}\n")
    out_path.write_text("".join(lines), encoding="utf-8")
    return out_path
if __name__ == "__main__":
    latest = get_latest_raw_file()
    raw_data = load_raw_json(latest)
    rows = transform_to_rows(raw_data)
    out_file = save_clean_csv(rows)
    print("Clean CSV saved successfully!", out_file)

  