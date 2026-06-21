import pandas as pd
import os

DATA_PATH = "data/raw"

for file in os.listdir(DATA_PATH):

    if file.endswith(".xlsx"):

        print("\n" + "="*80)
        print("FILE:", file)

        df = pd.read_excel(
            os.path.join(DATA_PATH, file)
        )

        print("Shape:", df.shape)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nData Types:")
        print(df.dtypes)