import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Finance Dashboard",
    page_icon="💳",
    layout="wide"
)

# --------------------------------------------------
# Backend URL
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

st.sidebar.title("💳 Finance Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Transaction",
        "Transactions"
    ]
)

# --------------------------------------------------
# Fetch Backend Data
# --------------------------------------------------

analytics_data = requests.get(
    f"{API_URL}/analytics"
).json()

prediction_data = requests.get(
    f"{API_URL}/prediction"
).json()

transactions_data = requests.get(
    f"{API_URL}/transactions"
).json()

# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":

    st.title("📊 AI Financial Analytics Dashboard")

    col1, col2, col3 = st.columns(3)

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

    with col3:
        st.metric(
            "Total Transactions",
            prediction_data["total_transactions"]
        )

    st.divider()

    # ------------------------------------------
    # Pie Chart
    # ------------------------------------------

    st.subheader("Category Breakdown")

    category_data = analytics_data["category_breakdown"]

    labels = list(category_data.keys())
    sizes = list(category_data.values())

    if len(labels) > 0:

        fig, ax = plt.subplots()

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%"
        )

        ax.axis("equal")

        st.pyplot(fig)

    else:
        st.info("No transaction data available yet.")

    # ------------------------------------------
    # Bar Chart
    # ------------------------------------------

    st.subheader("Category Spending")

    if len(labels) > 0:

        fig2, ax2 = plt.subplots()

        ax2.bar(
            labels,
            sizes
        )

        ax2.set_xlabel("Category")
        ax2.set_ylabel("Amount")

        st.pyplot(fig2)

    # ------------------------------------------
    # Recent Transactions
    # ------------------------------------------

    st.subheader("Recent Transactions")

    transactions_df = pd.DataFrame(
        transactions_data
    )

    st.dataframe(
        transactions_df,
        width="stretch"
    )

# --------------------------------------------------
# ADD TRANSACTION PAGE
# --------------------------------------------------

elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        key="amount_input"
    )

    description = st.text_input(
        "Description",
        key="description_input"
    )

    if st.button(
        "Add Transaction",
        key="add_transaction_button"
    ):

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

# --------------------------------------------------
# TRANSACTIONS PAGE
# --------------------------------------------------

elif page == "Transactions":

    st.title("📋 Transaction History")

    transactions_df = pd.DataFrame(
        transactions_data
    )

    st.dataframe(
        transactions_df,
        width="stretch"
    )

    csv = transactions_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Transactions CSV",
        data=csv,
        file_name="transactions.csv",
        mime="text/csv"
    )