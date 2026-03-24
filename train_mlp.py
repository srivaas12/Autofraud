import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"]

scaler = joblib.load("scaler.pkl")
autoencoder = joblib.load("autoencoder.pkl")

X_scaled = scaler.transform(X)

X_reconstructed = autoencoder.predict(X_scaled)
reconstruction_error = np.mean(
    np.square(X_scaled - X_reconstructed), axis=1
)

X_final = np.hstack([
    X_scaled,
    reconstruction_error.reshape(-1, 1)
])

X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42, stratify=y
)

mlp = MLPClassifier(
    hidden_layer_sizes=(32, 16),
    activation="relu",
    solver="adam",
    max_iter=20,
    random_state=42
)

mlp.fit(X_train, y_train)

y_pred = mlp.predict(X_test)

print("MLP Classification Report:")
print(classification_report(y_test, y_pred))

joblib.dump(mlp, "mlp_model.pkl")

print("MLP model saved successfully")
