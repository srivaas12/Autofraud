# train_universal_model.py

import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

# --------------------------------------------------
# 1. Load ONE representative banking dataset
# --------------------------------------------------
df = pd.read_csv("creditcard.csv")
# This can be ANY transaction dataset you already have

# --------------------------------------------------
# 2. Define canonical fraud feature inference
# --------------------------------------------------
def infer_fraud_features(df):
    features = {}

    numeric_cols = df.select_dtypes(include=np.number)

    # Amount score
    if not numeric_cols.empty:
        col = numeric_cols.columns[0]
        features["amount_score"] = (
            numeric_cols[col] - numeric_cols[col].mean()
        ).mean() / (numeric_cols[col].std() + 1e-5)
    else:
        features["amount_score"] = 0.0

    # Velocity score (simulated)
    features["velocity_score"] = np.random.rand()

    # Frequency score (simulated)
    features["frequency_score"] = np.random.rand()

    # Novelty score
    features["novelty_score"] = len(df.columns)

    # Channel risk
    features["channel_risk"] = 1.0

    # Location risk
    features["location_risk"] = np.random.rand()

    # Entropy score
    features["entropy_score"] = np.random.rand()

    return pd.DataFrame([features])


X = infer_fraud_features(df)

# Simulated labels (for training demo)
y = np.random.randint(0, 2, size=len(X))

# --------------------------------------------------
# 3. Scaling
# --------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --------------------------------------------------
# 4. Train Autoencoder
# --------------------------------------------------
input_dim = X_scaled.shape[1]

inp = Input(shape=(input_dim,))
enc = Dense(8, activation="relu")(inp)
dec = Dense(input_dim, activation="linear")(enc)

autoencoder = Model(inp, dec)
autoencoder.compile(optimizer=Adam(0.001), loss="mse")
autoencoder.fit(X_scaled, X_scaled, epochs=50, verbose=0)

# --------------------------------------------------
# 5. Anomaly score
# --------------------------------------------------
reconstructed = autoencoder.predict(X_scaled)
anomaly_score = np.mean((X_scaled - reconstructed) ** 2, axis=1)

X_final = np.hstack([X_scaled, anomaly_score.reshape(-1, 1)])

# --------------------------------------------------
# 6. Train MLP
# --------------------------------------------------
mlp = MLPClassifier(
    hidden_layer_sizes=(16, 8),
    max_iter=500,
    random_state=42
)
mlp.fit(X_final, y)

# --------------------------------------------------
# 7. Save models
# --------------------------------------------------
joblib.dump(scaler, "scaler.pkl")
joblib.dump(autoencoder, "autoencoder.pkl")
joblib.dump(mlp, "mlp_model.pkl")

print("✅ Universal fraud models trained and saved")
