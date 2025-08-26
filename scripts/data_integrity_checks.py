import pandas as pd

def check_missing_values(df):
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    print("Missing Values Summary:")
    print(pd.DataFrame({'Count': missing, 'Percent': missing_pct}).sort_values(by='Percent', ascending=False))
    print("-" * 50)

def check_duplicates(df):
    dup_count = df.duplicated().sum()
    print(f"Total duplicate rows: {dup_count}")
    for col in df.columns:
        dup_col_count = df[col].duplicated().sum()
        print(f"Duplicates in column '{col}': {dup_col_count}")
    print("-" * 50)

def check_data_types(df):
    print("Column Data Types:")
    print(df.dtypes)
    print("-" * 50)

if __name__ == "__main__":
    df = pd.read_csv('googleplaystore.csv')
    check_missing_values(df)
    check_duplicates(df)
    check_data_types(df)
