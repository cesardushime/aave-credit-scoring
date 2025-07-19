import pandas as pd
import numpy as np

def generate_user_features(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Group by user
    grouped = df.groupby('userid')

    # Feature: total deposit and borrow volume
    total_deposit = df[df['action_type'] == 'deposit'].groupby('userid')['amount_usd'].sum().rename('total_deposit_usd')
    total_borrow = df[df['action_type'] == 'borrow'].groupby('userid')['amount_usd'].sum().rename('total_borrow_usd')

    # Feature: borrow-to-deposit ratio
    ratio_df = pd.DataFrame({'total_deposit_usd': total_deposit, 'total_borrow_usd': total_borrow}).fillna(0)
    ratio_df['borrow_deposit_ratio'] = np.where(ratio_df['total_deposit_usd'] == 0, 0,
                                                ratio_df['total_borrow_usd'] / ratio_df['total_deposit_usd'])

    # Feature: number of unique assets
    unique_assets = grouped['asset_symbol'].nunique().rename('num_unique_assets')

    # Feature: number of transactions
    txn_count = grouped.size().rename('num_transactions')

    # Feature: days active
    first_seen = grouped['timestamp'].min()
    last_seen = grouped['timestamp'].max()
    days_active = (last_seen - first_seen).dt.days.rename('days_active')

    # Feature: average transaction amount
    avg_txn_amt = grouped['amount_usd'].mean().rename('avg_txn_amount_usd')

    # Feature: average time between transactions
    def avg_time_between_txn(user_df):
        sorted_ts = user_df.sort_values('timestamp')['timestamp']
        deltas = sorted_ts.diff().dropna()
        return deltas.mean().total_seconds() / 3600 if len(deltas) > 0 else np.nan

    avg_time_between = grouped.apply(avg_time_between_txn).rename('avg_time_between_txn_hrs')

    # Combine all features into one DataFrame
    features_df = pd.concat([
        ratio_df,
        unique_assets,
        txn_count,
        days_active,
        avg_txn_amt,
        avg_time_between
    ], axis=1).fillna(0).reset_index()

    return features_df
