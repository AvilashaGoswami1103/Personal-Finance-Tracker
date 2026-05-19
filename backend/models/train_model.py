import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
# converts text descriptions into numerical features using TF‑IDF (Term Frequency–Inverse Document Frequency).
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

# fit_transform learns the vocabulary from all descriptions and converts each description into a sparse numerical vector.
# Example:
# "Bought groceries" → [0.3, 0.0, 0.7, ...]
# "Paid electricity bill" → [0.0, 0.5, 0.2, ...]

# Create model
model = LogisticRegression()

# Train model
model.fit(X_vectors, y)

# Save trained model
joblib.dump(model, "category_model.pkl")
# The model contains learned weights for classification.

# Save vectorizer
joblib.dump(vectorizer, "vectorizer.pkl")
# The vectorizer contains the vocabulary and TF‑IDF transformation rules.

print("Model trained successfully!")