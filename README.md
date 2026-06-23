📊 PhonePe Payment Insights Dashboard
A Streamlit dashboard replicating a PhonePe Payment Insights Power BI project — built with Python, Plotly, and synthetic data.
�
�
�
�
Load image
Load image
Load image
🚀 Dashboard Highlights
Metric
Value
💳 Total Transactions
300K (+8.97% MoM)
💰 Total Transaction Value
₹3.47 Billion (+8.98% MoM)
👥 Total Users
108K
✅ Success Rate
96%
📌 Key Insights
📈 Transaction volume and value show positive growth throughout the year
💰 Loans contribute the highest transaction value (₹2.5 Billion)
📅 Weekday transactions (71.6%) significantly higher than weekends (28.4%)
👥 Gen X (37.4%) and Millennials (37.3%) are the largest contributors
🏆 Top user generated ₹1.82M+ in transaction value
✅ 96% success rate reflects a highly reliable payment system
🛠️ Tools Used
Python — Data generation & processing
Streamlit — Web dashboard framework
Plotly — Interactive charts
Pandas / NumPy — Data manipulation
📂 Project Structure
phonepe-dashboard/
│
├── app.py                  # Main Streamlit dashboard
├── generate_data.py        # Synthetic data generator
├── requirements.txt        # Python dependencies
├── data/
│   └── phonepe_transactions.csv   # Generated dataset (300K rows)
└── README.md
Code
▶️ How to Run Locally
Bash
# 1. Clone the repo
git clone https://github.com/jayeshkadam785/phonepe-payment-insights.git
cd phonepe-payment-insights

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset
python generate_data.py

# 4. Run the dashboard
streamlit run app.py
Open your browser at http://localhost:8501
🌐 Deploy on Streamlit Cloud (Free)
Push this repo to GitHub
Go to share.streamlit.io
Connect your GitHub repo
Set Main file path → app.py
Click Deploy ✅
📊 Dashboard Features
Sidebar filters — Filter by Month & Payment Status
KPI Cards — Total transactions, value, users, success rate
Transaction Over Time — Line chart with dual axis
Age Segment Contribution — Donut chart (Gen X, Millennial, Gen Z, Boomer)
Service Transaction Value — Horizontal bar chart
Top 5 Users — Bar chart by transaction value
Weekday vs Weekend — Donut chart
Insights Panel — Key business findings
👨‍💻 Author
Jayesh Kadam
B.Tech AI & Data Science | KBP College of Engineering, Satara
