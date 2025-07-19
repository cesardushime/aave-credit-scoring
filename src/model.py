import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest

def score_wallets(features_df):
    features_df = features_df.copy()
    
    # Drop userid temporarily
    user_ids = features_df['userid']
    X = features_df.drop('userid', axis=1)

    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Unsupervised anomaly detection
    iso_forest = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    anomaly_scores = iso_forest.fit_predict(X_scaled)
    anomaly_score_values = iso_forest.decision_function(X_scaled)

    # Normalize anomaly scores to 0-1000 scale
    normalized_scores = MinMaxScaler(feature_range=(0, 1000)).fit_transform(anomaly_score_values.reshape(-1, 1)).flatten()
    
    # Flip the scores: higher score → better behavior
    final_scores = 1000 - normalized_scores

    scored_df = pd.DataFrame({
        'userid': user_ids,
        'credit_score': final_scores.round(2)
    })

    return scored_df.sort_values('credit_score', ascending=False)
