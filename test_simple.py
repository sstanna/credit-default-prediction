import pandas as pd

# Load data
df = pd.read_csv('data/raw/UCI_Credit_Card.csv')
print(f'Dataset shape: {df.shape}')
print(f'Columns: {list(df.columns)}')
print(f'Target distribution: {df["default.payment.next.month"].value_counts()}')
print(f'Target distribution (%): {df["default.payment.next.month"].value_counts(normalize=True)}')
