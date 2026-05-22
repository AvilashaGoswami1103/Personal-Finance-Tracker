from collections import defaultdict # A defaultdict automatically initializes missing keys with a default value (here, float → 0.0).

def predict_future_spending(transactions):  # takes a list of transactions

    category_totals = defaultdict(float)    #Dictionary mapping each category to its total spending, starting at 0.0.

    total_spending = 0

    transaction_count = 0

    # Process all transactions
    # Extracts amount and category from each transaction (assumed to be a dictionary).
    for t in transactions:

        amount = t["amount"]

        category = t["category"]

        total_spending += amount

        transaction_count += 1

        category_totals[category] += amount

    # Calculate average spending
    if transaction_count == 0:
        average_spending = 0

    else:
        average_spending = total_spending / transaction_count

    # Simple monthly prediction
    predicted_next_month = average_spending * 30    
    # Assumes ~30 transactions per month.
    # Predicts next month’s spending by multiplying average transaction spending by 30.

    return {

        "total_transactions": transaction_count,

        "average_transaction_spending": round(
            average_spending,
            2
        ),

        "predicted_next_month_spending": round(
            predicted_next_month,
            2
        ),

        "category_spending": dict(category_totals)
    }

    # Forecasting Engine

    # It:

    # Reads historical transactions
    # Calculates averages
    # Estimates future spending
    # Computes category trends