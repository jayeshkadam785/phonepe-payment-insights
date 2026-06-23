import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# Config
N = 300000
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# Indian Names
# Hindu first names (male + female)
first_names = [
    # Male
    "Aarav", "Arjun", "Vivaan", "Aditya", "Krishna", "Ishaan", "Shiva", "Ganesh",
    "Vishnu", "Rama", "Lakshman", "Bharat", "Hanuman", "Kartik", "Dhruv", "Yash",
    "Rudra", "Pranav", "Vedant", "Shreyas", "Tejas", "Omkar", "Atharva", "Parth",
    "Rohan", "Varun", "Nikhil", "Siddharth", "Harsh", "Kunal", "Ankit", "Rahul",
    "Amit", "Suresh", "Ramesh", "Vijay", "Manoj", "Rajesh", "Sandeep", "Vikram",
    "Akash", "Ravi", "Mohit", "Harish", "Sanjay", "Deepak", "Ajay", "Rakesh",
    # Female
    "Priya", "Ananya", "Pooja", "Sneha", "Neha", "Divya", "Riya", "Kavya",
    "Anjali", "Shreya", "Meera", "Radha", "Sita", "Durga", "Lakshmi", "Parvati",
    "Saraswati", "Gayatri", "Tulsi", "Vrinda", "Ganga", "Yamuna", "Sunita",
    "Rekha", "Geeta", "Sonal", "Deepa", "Swati", "Pallavi", "Komal", "Rupali",
    "Manasi", "Shweta", "Varsha", "Madhuri", "Bharti", "Savita", "Nirmala", "Usha"
]
# Hindu surnames
last_names = [
    "Sharma", "Verma", "Gupta", "Joshi", "Mehta", "Shukla", "Trivedi", "Dwivedi",
    "Pandey", "Mishra", "Tiwari", "Chaudhary", "Agarwal", "Saxena", "Srivastava",
    "Singh", "Kumar", "Yadav", "Chauhan", "Rajput", "Thakur", "Patel", "Desai",
    "Shah", "Patil", "Kadam", "More", "Jadhav", "Shinde", "Pawar", "Kulkarni",
    "Joshi", "Bhatt", "Dixit", "Bajpai", "Malhotra", "Kapoor", "Chopra", "Khanna"
]
names = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(300)]

# Users
user_ids = [f"USR{str(i).zfill(6)}" for i in range(1, 108001)]
user_names = random.choices(names, k=108000)

# Age segments
age_segments = np.random.choice(
    ["Gen X", "Millennial", "Gen Z", "Boomer"],
    size=108000,
    p=[0.374, 0.373, 0.155, 0.098]
)

users_df = pd.DataFrame({
    "user_id": user_ids,
    "name": user_names[:108000],
    "age_segment": age_segments
})

# Generate random dates (weekday-biased: 71.6% weekday)
def random_date():
    d = start_date + timedelta(days=random.randint(0, 364))
    if random.random() < 0.716 and d.weekday() >= 5:
        d -= timedelta(days=random.randint(1, 2))
    return d

dates = [random_date() for _ in range(N)]

# Service types
service_types = np.random.choice(
    ["To Self Account", "To QR Code", "To UPI ID", "To Mobile Number", "Bike"],
    size=N,
    p=[0.22, 0.20, 0.22, 0.21, 0.15]
)

# Payment status (96% success)
statuses = np.random.choice(
    ["Successful", "Failed", "Pending"],
    size=N,
    p=[0.96, 0.025, 0.015]
)

# Transaction values
def get_amount(service):
    if service == "To Self Account":
        return round(np.random.lognormal(9, 1.2), 2)
    elif service == "To QR Code":
        return round(np.random.lognormal(7, 1.0), 2)
    elif service == "To UPI ID":
        return round(np.random.lognormal(8, 1.1), 2)
    elif service == "To Mobile Number":
        return round(np.random.lognormal(7.5, 1.0), 2)
    else:
        return round(np.random.lognormal(10, 0.8), 2)

amounts = [get_amount(s) for s in service_types]

# Assign users
transaction_users = np.random.choice(user_ids, size=N)
user_lookup = dict(zip(users_df.user_id, users_df.name))
age_lookup = dict(zip(users_df.user_id, users_df.age_segment))

txn_names = [user_lookup.get(uid, "Unknown") for uid in transaction_users]
txn_age = [age_lookup.get(uid, "Millennial") for uid in transaction_users]

# Build main dataframe
df = pd.DataFrame({
    "transaction_id": [f"TXN{str(i).zfill(8)}" for i in range(1, N+1)],
    "user_id": transaction_users,
    "user_name": txn_names,
    "date": dates,
    "month": [d.strftime("%B") for d in dates],
    "month_num": [d.month for d in dates],
    "day_type": ["Weekday" if d.weekday() < 5 else "Weekend" for d in dates],
    "service_type": service_types,
    "amount": amounts,
    "age_segment": txn_age
})

# Scale to match ₹3.47bn total
current_total = df[df.status == "Successful"]["amount"].sum()
target_total = 3_470_000_000
scale_factor = target_total / current_total
df["amount"] = (df["amount"] * scale_factor).round(2)

import os
os.makedirs("data", exist_ok=True)
df.to_csv("data/phonepe_transactions.csv", index=False)
print(f"✅ Generated {len(df)} transactions")
print(f"Total Value: ₹{df[df.status=='Successful']['amount'].sum()/1e9:.2f}bn")
print(f"Total Users: {df['user_id'].nunique()}")
print(f"Success Rate: {(df.status=='Successful').sum()/len(df)*100:.2f}%")
