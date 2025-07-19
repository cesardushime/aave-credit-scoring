import pandas as pd
import pytest
from src.feature_engineering import generate_user_features

# Sample synthetic data to test
@pytest.fixture
def sample_df():
    data = {
        'userid': ['u1', 'u1', 'u2', 'u2', 'u3'],
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-03 10:00:00',
            '2023-01-02 12:00:00',
            '2023-01-05 12:00:00',
            '2023-01-07 14:00:00'
        ],
        'action_type': ['deposit', 'borrow', 'deposit', 'borrow', 'deposit'],
        'amount_usd': [100.0, 40.0, 200.0, 60.0, 150.0],
        'asset_symbol': ['USDC', 'USDC', 'DAI', 'DAI', 'USDC']
    }
    df = pd.DataFrame(data)
    return df

def test_generate_user_features_output_shape(sample_df):
    features_df = generate_user_features(sample_df)
    assert isinstance(features_df, pd.DataFrame)
    assert 'userid' in features_df.columns
    assert 'total_deposit_usd' in features_df.columns
    assert 'borrow_deposit_ratio' in features_df.columns
    assert features_df.shape[0] == 3  # 3 unique users

def test_feature_values(sample_df):
    features_df = generate_user_features(sample_df)
    
    # Check user u1 values
    u1 = features_df[features_df['userid'] == 'u1'].iloc[0]
    assert u1['total_deposit_usd'] == 100.0
    assert u1['total_borrow_usd'] == 40.0
    assert round(u1['borrow_deposit_ratio'], 2) == 0.4
    assert u1['num_unique_assets'] == 1
    assert u1['num_transactions'] == 2
    assert u1['days_active'] == 2

    # Check user u3 has no borrow
    u3 = features_df[features_df['userid'] == 'u3'].iloc[0]
    assert u3['total_borrow_usd'] == 0
    assert u3['borrow_deposit_ratio'] == 0
