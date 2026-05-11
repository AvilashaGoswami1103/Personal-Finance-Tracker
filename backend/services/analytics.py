def calculate_analytics(transactions):
    total_spending = 0
    category_breakdown = {}    # An empty dictionary to store spending grouped by category

    for t in transactions:
        total_spending += t["amount"]      # Adds the amount field of the current transaction to the running total.

        # Checks if the transaction’s category already exists in the dictionary.
        # If yes, add the amount to the existing total.
        # If no, create a new entry with the amount.
        if t["category"] in category_breakdown:
            category_breakdown[t["category"]] += t["amount"]
        else:
            category_breakdown[t["category"]] = t["amount"]

    return {
        "total_spending": total_spending,
        "category_breakdown": category_breakdown
    }
