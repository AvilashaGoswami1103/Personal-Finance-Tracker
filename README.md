# Personal-Finance-Tracker
💡 Core Idea
A system that:
Connects to user financial data
Tracks transactions automatically
Categorizes spending (AI-based)
Predicts future expenses
And with this, we get out intelligent finance assistant.

🔗 APIs I'll Use
Stripe API for payments and Plaid API for banking data. 

🚀 Feature Breakdown
1. 🔄 Automatic Transaction Sync
Fetch transactions via Plaid
Store:
amount
merchant
timestamp
2. 🧠 AI-Based Categorization (THIS is your strength)
Instead of rule-based:
👉 Use ML:
Input: “Swiggy ₹450”
Output: “Food”
Approaches:
Basic → keyword matching
Better → ML classifier (Logistic Regression / small NN)
Advanced → fine-tuned NLP model
3. 📊 Monthly Analytics Dashboard
Total spending
Category-wise breakdown
Graphs:
Pie chart
Time series
4. 🔮 Spending Prediction
Use:
Moving average OR
Time-series model (ARIMA / LSTM)
👉 Output:
“You will spend ₹12,500 this month”
“Food spending likely to increase”
5. 🚨 Smart Alerts (Likely)
“You crossed budget for shopping”
“Unusual transaction detected”

🏗️ ARCHITECTURE
1. Backend(FastAPI): Python, Async support, Easy ML integration
2. Frontend: React OR Streamlit
3. API Gateway Layer(API orchestration Layer): My backend will act as aggregator and controller.

🤖 AI COMPONENT
Models to be included:
1. Categorization Model
Input: transaction description
Output: category
2. Prediction Model
Time-series forecasting
3. Anomaly Detection (bonus)
Detect fraud-like behavior


Implemented an NLP-inspired transaction categorization engine integrated into a FastAPI backend.
Transaction Data
        ↓
AI Categorization
        ↓
Analytics Engine
        ↓
Insights

How the main.py code works:
Client/User
     ↓
FastAPI Routes (main.py)
     ↓
Services Layer
     ↓
AI + Analytics Logic
     ↓
Response Returned

##Current Architecture:
Client/User
     ↓
FastAPI Routes
     ↓
Pydantic Validation
     ↓
AI Categorization Service
     ↓
Analytics Service
     ↓
SQLAlchemy ORM
     ↓
SQLite Database

Next phase implemented:
Real NLP pipeline integrated directly into backend APIs: 
models/train_model.py: Built an NLP-based transaction categorization engine using TF-IDF and Logistic Regression integrated into a FastAPI backend.

Spending Prediction Engine 
Method used: Moving Average forecasting (Time-series prediction)
🎯 GOAL
Predict:
future monthly spending
category-wise future trends
estimated next expenses

Forecasting pipeline:
Historical Transactions
        ↓
Feature Aggregation
        ↓
Prediction Model
        ↓
Forecast Output

Next phase: Full interactive finance dashboard, using streamlit frontend
| Feature            | UI Component      |
| ------------------ | ----------------- |
| Add transactions   | Form              |
| View transactions  | Table             |
| Category analytics | Pie chart         |
| Spending forecast  | Cards/graphs      |
| ML predictions     | Real-time display |

Libraries used: 
| Library    | Purpose            |
| ---------- | ------------------ |
| streamlit  | Frontend dashboard |
| requests   | Call FastAPI APIs  |
| pandas     | Data handling      |
| matplotlib | Charts             |

| Component             | Visualization |
| --------------------- | ------------- |
| Total spending        | KPI metric    |
| Predicted spending    | KPI metric    |
| Category breakdown    | Pie chart     |
| Transactions          | Table         |
| Spending per category | Bar chart     |





