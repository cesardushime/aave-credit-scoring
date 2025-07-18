import json
import pandas as pd
from datetime import datetime

def load_json_to_df(filepath):
    #Load and convert raw JSON to a DataFrame
    with open(filepath, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print("✅ Loaded JSON with", len(df), "rows")
    print(df.head())

    return df
def preprocess_transactions(df):
    # Keep useful columns, dropping __v, createdAt, updatedAt
    df = df[[
        'userWallet', 'timestamp', 'action', 'actionData', 'txHash'
    ]].copy()

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Extract values from actionData dictionary
    df['amount'] = df['actionData'].apply(lambda x: float(x.get('amount', 0)))
    df['token'] = df['actionData'].apply(lambda x: x.get('assetSymbol', 'Unknown'))

    # Drop actionData now that we've extracted values
    df.drop(columns='actionData', inplace=True)

    return df

if __name__ == "__main__":
    filepath = 'C:\\Users\\Cesar Dushimimana\\Documents\\aave-credit-scoring\\data\\transactions.json' 
    df_raw = load_json_to_df(filepath)
    df_clean = preprocess_transactions(df_raw)

    print("📄 Cleaned DataFrame:")
    print(df_clean.head())
    print("\n🔢 Action types:", df_clean['token'].value_counts())
