PROJECT_ID = "crypto-etl-pipeline-486305"
DATASET_ID = "crypto_dw"
TABLE_ID = "crypto_prices"
import os
from pathlib import Path
import pandas as pd
from google.cloud import bigquery
KEY_PATH = Path(__file__).resolve().parents[1] / "crypto-etl-pipeline-486305-1d92cfa3f673.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(KEY_PATH)
project_id = "crypto-etl-pipeline-486305"
dataset_id = "crypto_dw"
table_id = "crypto_prices"
clean_dir = Path("data/clean")
def get_latest_clean_file():
    files = sorted(clean_dir.glob("crypto_prices_*.csv"))
    if not files:
        raise FileNotFoundError("No Clean CSV files found in data/clean. Run etl_transform.py first.")
    return files[-1]
def read_clean_csv(csv_path: Path):
    df = pd.read_csv(csv_path)
    return df
def load_to_bigquery(df):
    from datetime import datetime, timezone
    if "date_utc" not in df.columns:
        df["date_utc"] = datetime.now(timezone.utc).date().isoformat()
    if "ingested_at_utc" not in df.columns:
        df["ingested_at_utc"] = datetime.now(timezone.utc).isoformat()
    if "last_updated_at" in df.columns and "source_updated_at_utc" not in df.columns:
        df = df.rename(columns={"last_updated_at": "source_updated_at_utc"})
    required_cols = ["date_utc", "coin", "currency", "price", "source_updated_at_utc", "ingested_at_utc"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None
    df = df[required_cols]

    print("Columns being loaded:", list(df.columns))
    print("First rows:\n", df.head())
    client = bigquery.Client(project=project_id)
    table_full_id = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(
        write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    )
    job = client.load_table_from_dataframe(df, table_full_id, job_config = job_config)
    job.result()
    return table_full_id
    
if __name__ == "__main__":
    latest = get_latest_clean_file()
    df = read_clean_csv(latest)
    from datetime import datetime, timezone
    df["date_utc"] = datetime.now(timezone.utc).date().isoformat()
    table_id = load_to_bigquery(df)
    print("Loaded into BigQuery table:", table_id)
    print("Rows Loaded:", len(df))

