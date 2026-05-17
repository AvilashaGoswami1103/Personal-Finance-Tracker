# Rule-based NLP classification


import joblib

# Load trained model
model = joblib.load("backend/models/category_model.pkl")

# Load vectorizer
vectorizer = joblib.load("backend/models/vectorizer.pkl")

def categorize_transaction(description):

    # Convert input text into vectors
    description_vector = vectorizer.transform([description])

    # Predict category
    prediction = model.predict(description_vector)

    return prediction[0]

# def categorize_transaction(description):

#     description = description.lower()

#     # Food category
#     food_keywords = [
#         "swiggy",
#         "zomato",
#         "restaurant",
#         "food",
#         "pizza",
#         "burger"
#     ]

#     # Travel category
#     travel_keywords = [
#         "uber",
#         "ola",
#         "bus",
#         "train",
#         "flight"
#     ]

#     # Shopping category
#     shopping_keywords = [
#         "amazon",
#         "flipkart",
#         "shopping",
#         "clothes"
#     ]

#     # Check food keywords
#     for word in food_keywords:
#         if word in description:
#             return "Food"

#     # Check travel keywords
#     for word in travel_keywords:
#         if word in description:
#             return "Travel"

#     # Check shopping keywords
#     for word in shopping_keywords:
#         if word in description:
#             return "Shopping"

#     return "Others"