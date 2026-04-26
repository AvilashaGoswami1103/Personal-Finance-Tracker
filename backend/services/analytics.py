def calculate_analytics(transactions):
    total_spending = 0
    category_breakdown = {}

    for t in transactions:
        total_spending += t["amount"]

        if t.category in category_breakdown:
            category_breakdown[t["category"]] += t["amount"]
        else:
            category_breakdown[t["category"]] = t["amount"]

    return {
        "total_spending": total_spending,
        "category_breakdown": category_breakdown
    }