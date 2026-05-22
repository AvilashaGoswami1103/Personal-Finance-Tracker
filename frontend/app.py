import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Finance Tracker",
    layout="wide"
)

st.title("💳 AI-Powered Finance Tracker")

st.header("Add Transaction")

amount = st.number_input(
    "Amount",
    min_value=0.0
)

description = st.text_input(
    "Description"
)

if st.button("Add Transaction"):

    data = {
        "amount": amount,
        "description": description
    }

    response = requests.post(
        f"{API_URL}/add_transaction",
        json=data
    )

    result = response.json()

    st.success(
        f"Predicted Category: {result['predicted_category']}"
    )

# Fetch analytics
analytics_response = requests.get(
    f"{API_URL}/analytics"
)

analytics_data = analytics_response.json()

# Fetch prediction
prediction_response = requests.get(
    f"{API_URL}/prediction"
)

prediction_data = prediction_response.json()

# Fetch transactions
transactions_response = requests.get(
    f"{API_URL}/transactions"
)



transactions_data = transactions_response.json()

st.header("Financial Analytics")

transactions_df = pd.DataFrame(
    transactions_data
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Spending",
        f"₹ {analytics_data['total_spending']}"
    )

with col2:

    st.metric(
        "Predicted Monthly Spending",
        f"₹ {prediction_data['predicted_next_month_spending']}"
    )

st.header("Transaction History")

st.dataframe(transactions_df)



st.header("Category Breakdown")

category_data = analytics_data[
    "category_breakdown"
]

labels = list(category_data.keys())

sizes = list(category_data.values())

fig, ax = plt.subplots()

ax.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

ax.axis("equal")

st.pyplot(fig)


st.header("Category Spending")

fig2, ax2 = plt.subplots()

ax2.bar(
    labels,
    sizes
)

ax2.set_xlabel("Category")

ax2.set_ylabel("Amount")

st.pyplot(fig2)
