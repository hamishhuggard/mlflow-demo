import random
import os
from datetime import datetime, timedelta

output_dir = "spark_output"
os.makedirs(output_dir, exist_ok=True)
sales_data_file = os.path.join(output_dir, "sales_transactions.csv")

num_transactions = 1000
product_names = ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam", "Headphones", "SSD", "RAM", "CPU", "GPU"]

print(f"Generating {num_transactions} synthetic sales transactions to {sales_data_file}...")

with open(sales_data_file, "w") as f:
    # Write header
    f.write("TransactionID,ProductID,ProductName,Quantity,Price,TransactionDate\n")
    for i in range(1, num_transactions + 1):
        transaction_id = f"TRN{i:05d}"
        product_id = f"PROD{random.randint(1, 10):02d}"
        product_name = random.choice(product_names)
        quantity = random.randint(1, 5)
        price = round(random.uniform(10.0, 1000.0), 2)
        
        # Introduce some invalid data for cleaning demonstration
        if random.random() < 0.02: # 2% chance of invalid quantity
            quantity = "invalid" 
        if random.random() < 0.01: # 1% chance of invalid price
            price = "error"
        if random.random() < 0.005: # 0.5% chance of missing product name
            product_name = ""

        # Generate a date within the last 30 days
        transaction_date = (datetime.now() - timedelta(days=random.randint(0, 30),
                                                        hours=random.randint(0, 23),
                                                        minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S")
        
        f.write(f"{transaction_id},{product_id},{product_name},{quantity},{price},{transaction_date}\n")

print("Synthetic sales data generated.")
