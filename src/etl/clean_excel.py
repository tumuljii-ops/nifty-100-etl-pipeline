import pandas as pd
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

dirty_files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

for file in dirty_files:

    path = os.path.join(RAW_PATH, file)

    df = pd.read_excel(path, header=None)

    # actual column names are in row 1
    headers = df.iloc[1]

    # keep data from row 2 onwards
    df = df.iloc[2:].copy()

    df.columns = headers

    df.reset_index(drop=True, inplace=True)

    output_file = os.path.join(
        PROCESSED_PATH,
        file.replace(".xlsx", ".csv")
    )

    df.to_csv(output_file, index=False)

    print(f"Cleaned {file}")