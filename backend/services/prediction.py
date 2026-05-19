def predict_spending(transactions):

    if len(transactions) == 0:
        return {
            "predicted_spending": 0
        }

    total_spending = 0

    for t in transactions:
        total_spending += t["amount"]

    average_spending = total_spending / len(transactions)

    predicted_spending = round(average_spending, 2)

    return {
        "predicted_spending": predicted_spending
    }