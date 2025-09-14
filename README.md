# Apache Airflow Market Volume DAG

## Overview

Demonstration of a basic Apache Airflow DAG for orchestrating a stock market data pipeline.  Utilizes **Yahoo Finance API** to download one-minute interval intraday stock data for 'AAPL' and 'TSLA', saves it to CSV, moves it to a data directory, and performs a simple analytical query.

### DAG Name
'marketvol'

### DAG Schedule
- **Runs:** Weekdays only (Mon–Fri)
- **Time:** 6:00 PM (local time)
- **Retries:** 2 retries on failure
- **Retry Delay:** 5 minutes

---

# Project Structure

```bash
AirflowProject/  
├── airflow_home/  
│   └── dags/  
│       └── marketvol_dag.py  
├── README.md  
```

### Prerequisites

Before running this DAG, ensure the following are installed:

- Python 3.8+
- Apache Airflow
- Pandas
- yfinance
- Linux operating system or macOS/Windows operating with Docker or WSL2

### How to Run  

#### Step 1: Set up virtual environment

Navigate to your project directory
```bash
# Create virtual environment
python3 -m venv airflow_venv

# Activate the virtual environment (Linux/macOS)
source airflow_venv/bin/activate

# Activate the virtual environment (Windows)
.\airflow_venv\Scripts\activate
```
#### Step 2: Set up Airflow (bash)

```bash
# Set Airflow home
export AIRFLOW_HOME=~/airflow_home

#Initialize Airflow DB
airflow db migrate
```

#### Step 3: Ensure DAG is in dags/ directory

Ensure that marketvol_dag.py is located in the dags/ directory under $AIRFLOW_HOME

#### Step 4: Run Airflow

```bash
airflow standalone
```

#### Step 5: View Airflow UI

After launching Airflow with 'standalone' command, the UI can be viewed at http://localhost:8080  
Log in using credentials stored at ~/airflow/simple_auth_manager_passwords.json.generated

### DAG Structure

- t0: BashOperator to create a date-named temp directory

- t1: PythonOperator to download AAPL data

- t2: PythonOperator to download TSLA data

- t3: BashOperator to move AAPL data to /data location

- t4: BashOperator to move TSLA data to /data location

- t5: PythonOperator to run custom query on both files

### Output

CSV files: Stored under /tmp/data/<execution_date>/  
Query Result: Printed to Airflow logs
