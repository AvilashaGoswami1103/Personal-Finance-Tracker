def categorize_transaction(description):

    description = description.lower()

    # Food category
    food_keywords = [
        "swiggy",
        "zomato",
        "restaurant",
        "food",
        "pizza",
        "burger"
    ]

    # Travel category
    travel_keywords = [
        "uber",
        "ola",
        "bus",
        "train",
        "flight"
    ]

    # Shopping category
    shopping_keywords = [
        "amazon",
        "flipkart",
        "shopping",
        "clothes"
    ]

    # Check food keywords
    for word in food_keywords:
        if word in description:
            return "Food"

    # Check travel keywords
    for word in travel_keywords:
        if word in description:
            return "Travel"

    # Check shopping keywords
    for word in shopping_keywords:
        if word in description:
            return "Shopping"

    return "Others"