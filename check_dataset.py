import pandas as pd

df = pd.read_csv("creditcard.csv")

print("Dataset loaded successfully")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nFraud class distribution:")
print(df["Class"].value_counts())
