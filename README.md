# Thunder Energy - Data Engineering Challenge

## Setup Instructions

### Prerequisites
- Docker Desktop or PostgreSQL 13+
- Python 3.9+

### Start PostgreSQL

docker run --name postgres-energy -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=thunder_energy -p 5432:5432 -d postgres:15

### Install Dependencies

pip install -r requirements.txt

### Load Data

python load_data.py

### Run Calculation

python task2_run_hours.py
python task3_power_kw.py

### Assumptions

Source detection – Case-insensitive substring match (ILIKE '%DG%'). "DG+Solar" counts for both DG and Solar.

Run hours – Each row = 3 minutes. Formula: (count × 3) ÷ 60. Max = 1.0 hour per source per hour.

Negative battery current – Indicates discharging. Negative kW is correct per spec.

Timezone – CSV timestamps have +05 offset. PostgreSQL stores as TIMESTAMPTZ (UTC). Hour windows use DATE_TRUNC('hour', timestamp).

No Mains data – Grid query included but dataset has no "Mains" rows.

### Reproduce Results

On a fresh machine perform the following steps:

git clone https://github.com/AliMateen012/thunder-energy-challenge.git
cd thunder-energy-challenge
docker run --name postgres-energy -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=thunder_energy -p 5432:5432 -d postgres:15
pip install -r requirements.txt
python load_data.py
python task2_run_hours.py
python task3_power_kw.py
Expected Output
480 rows loaded

output/run_hours.csv – 45 rows, run_hours ≤ 1.0

output/power_kw.csv – 45 rows, kw rounded to 2 decimals

### Worked Example (Section 8)
Reading at 00:06:00 (DG): 109.3A × 48.9V ÷ 1000 = 5.345 kW ✅

Run hours per reading = 3 ÷ 60 = 0.05 hours ✅

### Technologies
Python, PostgreSQL, Pandas, SQLAlchemy, Docker


