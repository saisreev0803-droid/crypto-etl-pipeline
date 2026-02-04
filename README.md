# 🚀 Crypto ETL Pipeline with BigQuery

A production-style **Data Engineering ETL pipeline** that extracts cryptocurrency market data from an external API, transforms it into analytics-ready format, and loads it into **Google BigQuery** for cloud-based analysis.

This project simulates how real-world data pipelines are designed to handle ingestion, transformation, storage, and warehouse loading.

---

## 🎯 Project Objective

Build an automated data pipeline that:

- Ingests cryptocurrency prices from a public API  
- Stores raw source data for traceability  
- Transforms nested JSON into structured tabular data  
- Loads clean historical data into a cloud warehouse  

This mirrors how companies build **daily ingestion pipelines** for analytics systems.

---

## 🧠 Skills Demonstrated

- API Data Ingestion  
- ETL Pipeline Design  
- JSON Processing  
- Data Modeling  
- Cloud Data Warehousing  
- Schema Handling  
- Data Lineage Concepts  

---

## 🏗 Pipeline Architecture

**Extract → Transform → Load (ETL)**

| Stage | Description |
|------|-------------|
| **Extract** | Python script calls CoinGecko API |
| **Raw Layer** | Saves immutable JSON data |
| **Transform** | Converts JSON into structured dataset |
| **Clean Layer** | Stores analytics-ready CSV |
| **Load** | Appends data into BigQuery warehouse |

---

## 📂 Project Structure

crypto-etl-pipeline/
│
├── src/
│ ├── etl_extract.py 
│ ├── etl_transform.py 
│ └── etl_load_bigquery.py 
│
├── data/
│ ├── raw/ 
│ └── clean/ 
│
├── requirements.txt
└── README.md


---

## 📊 Data Warehouse Table Schema

| Column | Description |
|--------|------------|
| `date_utc` | Reference date |
| `coin` | Cryptocurrency name |
| `currency` | Fiat currency (USD) |
| `price` | Market price |
| `source_updated_at_utc` | Timestamp from source API |
| `ingested_at_utc` | Pipeline ingestion time |

---

## ⚙️ How to Run the Pipeline

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
2️⃣ Extract API Data
python src/etl_extract.py
3️⃣ Transform Raw Data
python src/etl_transform.py
4️⃣ Load into BigQuery
python src/etl_load_bigquery.py
☁️ Cloud Configuration
This project uses Google BigQuery as the cloud data warehouse.

Set credentials before loading:

set GOOGLE_APPLICATION_CREDENTIALS=your-key-file.json
