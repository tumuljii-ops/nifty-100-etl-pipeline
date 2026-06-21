# NIFTY100 ETL Pipeline

## Project Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline for NIFTY100 financial datasets. The pipeline ingests raw Excel files, performs data cleaning and validation, loads the processed data into a SQLite database, and generates audit and data quality reports.

---

## Dataset Information

The project uses 12 source datasets containing company fundamentals, financial statements, ratios, sector information, market capitalization data, and stock prices.

### Core Datasets

* companies.xlsx
* profitandloss.xlsx
* balancesheet.xlsx
* cashflow.xlsx
* analysis.xlsx
* documents.xlsx
* prosandcons.xlsx

### Supporting Datasets

* financial_ratios.xlsx
* market_cap.xlsx
* peer_groups.xlsx
* sectors.xlsx
* stock_prices.xlsx

---

## Tech Stack

* Python
* Pandas
* SQLite
* VS Code

---

## Project Structure

```text
NIFTY100-ETL
│
├── data
│   ├── raw
│   └── processed
│
├── db
│   ├── schema.sql
│   └── nifty100.db
│
├── outputs
│   ├── load_audit.csv
│   ├── validation_failures.csv
│   └── validation_summary.csv
│
├── src
│   └── etl
│
├── tests
│
└── README.md
```

---

## ETL Workflow

### Extract

* Read 12 source Excel datasets
* Discover schema and data structure

### Transform

* Clean malformed Excel files
* Standardize column headers
* Generate processed CSV files
* Validate data quality rules

### Load

* Create SQLite database schema
* Load cleaned datasets into database tables
* Generate load audit reports

---

## Database Tables

* companies
* profitandloss
* balancesheet
* cashflow
* financial_ratios
* market_cap
* peer_groups
* sectors
* stock_prices
* documents

---

## Data Quality Validation

### DQ01 - Primary Key Uniqueness

Ensures primary key values are unique across all tables.

Status: PASS

### DQ03 - Foreign Key Integrity

Checks whether all company_id values exist in the companies master table.

Status: FAIL (source data inconsistency detected)

### DQ04 - Balance Sheet Equation Validation

Validates:

Total Assets = Total Liabilities

Status: PASS

### DQ05 - Operating Profit Margin Validation

Validates:

OPM % = (Operating Profit / Sales) × 100

Status: REVIEW

---

## Load Statistics

| Table            | Records |
| ---------------- | ------: |
| companies        |      92 |
| profitandloss    |    1276 |
| balancesheet     |    1312 |
| cashflow         |    1187 |
| financial_ratios |    1184 |
| market_cap       |     552 |
| peer_groups      |      56 |
| sectors          |      92 |
| stock_prices     |    5520 |

---

## Generated Outputs

* load_audit.csv
* validation_failures.csv
* validation_summary.csv
* balance_sheet_failures.csv
* opm_failures.csv

---

## Key Learnings

* ETL Pipeline Development
* Data Cleaning and Transformation
* SQLite Database Design
* Data Quality Validation
* Foreign Key Integrity Checks
* Financial Data Analysis
* Audit Reporting
