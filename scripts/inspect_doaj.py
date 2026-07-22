from pathlib import Path

import pandas as pd


def main():
    csv_path = Path("data/raw/doaj_journalcsv_20260621_2320_utf8.csv")

    df = pd.read_csv(csv_path)

    print("=" * 60)
    print("DOAJ Dataset Overview")
    print("=" * 60)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn Names")
    print("-" * 60)

    for i, column in enumerate(df.columns, start=1):
        print(f"{i:2}. {column}")

    print("\nFirst Five Rows")
    print("-" * 60)

    print(df.head())

    print("\nData Types")
    print("-" * 60)

    print(df.dtypes)


if __name__ == "__main__":
    main()