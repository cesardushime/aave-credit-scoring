import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def compute_credit_score(features_df):
    df = features_df.copy()
    
    # Prevent division by zero
    df["borrow_to_deposit_ratio"] = df["total_borrow_usd"] / (df["total_deposit_usd"] + 1)

    # --- Normalize each subscore to 0-100 ---
    def scale(series, min_val, max_val, inverse=False):
        clipped = series.clip(lower=min_val, upper=max_val)
        norm = (clipped - min_val) / (max_val - min_val)
        if inverse:
            norm = 1 - norm
        return (norm * 100).fillna(0)
    
    df["score_borrow_ratio"] = scale(df["borrow_to_deposit_ratio"], 0, 1, inverse=True)
    df["score_txn_count"] = scale(df["num_transactions"], 5, 50)
    df["score_days_active"] = scale(df["days_active"], 5, 100)
    df["score_avg_txn_amt"] = scale(df["avg_txn_amount_usd"], 100, 5000)
    df["score_unique_assets"] = scale(df["num_unique_assets"], 1, 8)
    df["score_txn_frequency"] = scale(df["avg_time_between_txn_hrs"], 0.5, 7, inverse=True)
    df["score_borrow_volume"] = scale(df["total_borrow_usd"], 100, 50000)

    # --- Weighted average of all subscores ---
    df["raw_score"] = (
        df["score_borrow_ratio"] * 0.25 +
        df["score_txn_count"] * 0.15 +
        df["score_days_active"] * 0.15 +
        df["score_avg_txn_amt"] * 0.10 +
        df["score_unique_assets"] * 0.10 +
        df["score_txn_frequency"] * 0.10 +
        df["score_borrow_volume"] * 0.15
    )

    # --- Rescale to 0–1000 range ---
    df["credit_score"] = MinMaxScaler(feature_range=(0, 1000)).fit_transform(df["raw_score"].values.reshape(-1, 1)).flatten()

    return df[["userid", "credit_score"]].sort_values("credit_score", ascending=False)
