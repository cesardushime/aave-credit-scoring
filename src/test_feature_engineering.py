import pandas as pd
from feature_engineering import generate_user_features

# Sample dummy data simulating your actual structure
sample_data = {
    'userid': ['user1', 'user1', 'user2', 'user2', 'user2'],
    'timestamp': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-03', '2023-01-05'],
    'blocknumber': [1, 2, 3, 4, 5],
    'action': ['action1', 'action2', 'action3', 'action4', 'action5'],
    'action_type': ['deposit', 'borrow', 'deposit', 'deposit', 'borrow'],
    'amount': [100, 200, 300, 400, 500],
    'asset_symbol': ['USDC', 'USDC', 'DAI', 'DAI', 'DAI'],
    'asset_price_usd': [1, 1, 1, 1, 1],
    'pool_id': ['pool1', 'pool1', 'pool2', 'pool2', 'pool2'],
    'user_id_nested': ['nested1', 'nested1', 'nested2', 'nested2', 'nested2'],
    'to_id': ['to1', 'to2', 'to3', 'to4', 'to5'],
    'amount_usd': [100, 200, 300, 400, 500],
    'user_differs': [False, False, True, True, True]
}

df = pd.DataFrame(sample_data)

# Test the feature generation function
features_df = generate_user_features(df)

# Print the resulting features
print(features_df)
