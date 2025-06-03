# Air Quality Monitoring - Batch Data Pipeline

This project implements a scalable, Docker-based batch data processing pipeline to monitor and analyze air pollution trends using the U.S. Pollution Dataset.

---

## 🔧 Architecture Overview

This modular pipeline follows a layered architecture:

1. **Ingestion Layer** (Python): Loads CSV data from Kaggle into HDFS.
2. **Storage Layer** (HDFS): Stores raw and processed data in a fault-tolerant file system.
3. **Processing Layer** (Spark + PySpark): Cleans, aggregates, and summarizes data.
4. **Data Layer** (MongoDB): Holds processed outputs for querying.
5. **Delivery Layer** (Flask API): Exposes endpoints for external use.
6. **Presentation Layer** (Streamlit): Interactive dashboard for data visualization.
7. **Orchestration Layer** (Apache Airflow): Manages automated scheduling.


---

## 🗂 Dataset

- Source: [U.S. Pollution Dataset – Kaggle](https://www.kaggle.com/datasets/sogun3/uspollution)
- Format: CSV
- Size: 1.5M+ time-stamped records

---

## 🔧 Requirements

- Docker & Docker Compose
- Python 3.9+
- Spark
- Hadoop (via Docker images)
- MongoDB
- Apache Airflow
- Streamlit
- Flask

---

## 📊 Endpoints (Flask)

| Endpoint       | Description                         |
|----------------|-------------------------------------|
| `http://localhost:5000/summary`     | Shows top summary of records        |
| `http://localhost:5000/filter?state=California&year=2005`      | Filter by state or year parameters  |

---

## 📈 Visualization

The dashboard presents interactive charts:
- Pollution trends per state/year
- Average levels of NO2, O3, SO2, and CO

The dashboard is available at `http://localhost:8501`  
![Example Dashboard](https://github.com/MojganBehravan/air-quality-monitoring/raw/main/dashboard/dashboard.png)

---

## 🚀 How to Run the Project

Since the Storage Layer (HDFS) must be initialized before any data is ingested or processed, follow this sequence to ensure all required folders (`/raw`, `/processed`) exist before the pipeline starts.

### 📥 Dataset Setup

Before running the pipeline, you must download the air pollution dataset:

1. Download it from Kaggle:  
   👉 https://www.kaggle.com/datasets/sogun3/uspollution

2. Place the downloaded CSV file (e.g., `pollution_us_2000_2016.csv`) into the `data/` directory at the root of the project:
> ⚠️ Ensure the filename matches what the `ingest.py` script expects. If different, update the script accordingly.

### 🧭 Execution Steps

```bash
# Step 1: Start only HDFS components
docker-compose up -d namenode datanode

# Step 2: Run the HDFS setup script to create required folders
python ingestion/setup_hdfs.py

# Step 3: Start the rest of the pipeline (Airflow, Spark, MongoDB, etc.)
docker-compose up -d
```

This ensures:
- `/user/hadoop/raw` and `/user/hadoop/processed` exist
- Spark and ingestion won’t fail due to missing HDFS paths
- A smooth and consistent startup process


## 👤 Author

Mojgan Behravan  


