import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import joblib

# Load dataset
data = pd.read_csv("transactions_dataset.csv")

# Inputs and labels
X = data["description"]

y = data["category"]

# Convert text into numerical vectors
vectorizer = TfidfVectorizer()

X_vectors = vectorizer.fit_transform(X)

# Create model
model = LogisticRegression()

# Train model
model.fit(X_vectors, y)

# Save trained model
joblib.dump(model, "category_model.pkl")

# Save vectorizer
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully!")