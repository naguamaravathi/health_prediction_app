from sklearn.linear_model import LogisticRegression
import numpy as np
import joblib

# Sample training data
X = np.array([
    [150, 11.5, 250],
    [90, 13.0, 180],
    [200, 10.0, 300],
    [100, 14.0, 170],
    [180, 11.0, 260]
])

# 1 = Risk, 0 = Healthy
y = np.array([1, 0, 1, 0, 1])

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "risk_model.pkl")

print("Model trained successfully!")