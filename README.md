# ⚡ Thunder Energy — Data Engineering Challenge

A PostgreSQL + Python pipeline that ingests energy telemetry data and computes **run hours** and **power output (kW)** per energy source per hour.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Assumptions](#assumptions)
- [Expected Output](#expected-output)
- [Worked Examples](#worked-examples)
- [Tech Stack](#tech-stack)

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) **or** PostgreSQL 13+
- Python 3.9+

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/AliMateen012/thunder-energy-challenge.git
cd thunder-energy-challenge
```

### 2. Start PostgreSQL

```bash
docker run --name postgres-energy \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=thunder_energy \
  -p 5432:5432 \
  -d postgres:15
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Load data

```bash
python load_data.py
```

> ✅ Expect **480 rows** to be loaded.

### 5. Run calculations

```bash
python task2_run_hours.py
python task3_power_kw.py
```

Results are written to the `output/` directory.

---

## Project Structure

```
thunder-energy-challenge/
├── load_data.py            # Ingests CSV data into PostgreSQL
├── task2_run_hours.py      # Calculates run hours per source per hour
├── task3_power_kw.py       # Calculates power output (kW) per source per hour
├── requirements.txt
└── output/
    ├── run_hours.csv       # 45 rows, run_hours ≤ 1.0
    └── power_kw.csv        # 45 rows, kW rounded to 2 decimals
```

---

## Assumptions

| Topic | Assumption |
|---|---|
| **Source detection** | Case-insensitive substring match (`ILIKE '%DG%'`). `"DG+Solar"` counts for both DG and Solar. |
| **Run hours** | Each row = 3 minutes. Formula: `(count × 3) ÷ 60`. Max = 1.0 hour per source per hour. |
| **Battery current** | Negative current indicates discharging. Negative kW values are correct per spec. |
| **Timezone** | CSV timestamps carry a `+05` offset. PostgreSQL stores as `TIMESTAMPTZ` (UTC). Hour windows use `DATE_TRUNC('hour', timestamp)`. |
| **Mains data** | Grid query is included, but the dataset contains no `"Mains"` rows. |

---

## Expected Output

| File | Rows | Notes |
|---|---|---|
| `output/run_hours.csv` | 45 | `run_hours` ≤ 1.0 per source per hour |
| `output/power_kw.csv` | 45 | `kw` rounded to 2 decimal places |

---

## Worked Examples

**DG power calculation:**

```
DG kW = voltage × current ÷ 1000
      = 109.3 × 48.9 ÷ 1000
      = 5.35 kW ✅
```

**Run hours per reading:**

```
run_hours = 3 minutes ÷ 60
          = 0.05 hours per reading ✅
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Database | PostgreSQL 15 |
| Libraries | Pandas, SQLAlchemy, Psycopg2 |
| Infrastructure | Docker |