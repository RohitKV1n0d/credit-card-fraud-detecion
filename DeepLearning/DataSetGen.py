import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
random.seed(42)

# Define sample sizes
total_samples = 100000
fraud_samples = total_samples // 10
non_fraud_samples = total_samples - fraud_samples

# Define locations
locations_india = ['Thrissur', 'Coimbatore', 'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore', 'Gujarat', 'Kashmir' ]
non_fraud_locations = ['Thrissur', 'Coimbatore']
locations_fraud = [loc for loc in locations_india if loc not in non_fraud_locations]

# Generate random data for non-fraudulent transactions
non_fraud_data = {
    'Transaction': [random.choice(['Withdrawal', 'Purchase', 'Transfer']) for _ in range(non_fraud_samples)],
    'Amount': [random.randint(1, 5000) for _ in range(non_fraud_samples)],
    'Time of Day': [random.randint(0, 23) for _ in range(non_fraud_samples)],
    'Location': [random.choice(locations_india) for _ in range(non_fraud_samples)],  # More random locations
    'Fraudulent': [0] * non_fraud_samples
}

# Generate random data for fraudulent transactions
fraud_data = {
    'Transaction': [random.choice(['Withdrawal', 'Purchase', 'Transfer']) for _ in range(fraud_samples)],
    'Amount': [random.randint(10000, 50000) if random.random() < 0.8 else random.randint(1, 9999) for _ in range(fraud_samples)],  # Introduce randomness in the amount
    'Time of Day': [random.choice(list(range(23, 24)) + list(range(0, 6))) if random.random() < 0.8 else random.randint(6, 22) for _ in range(fraud_samples)],  # Introduce randomness in the time of day
    'Location': [random.choice(locations_fraud) for _ in range(fraud_samples)],
    'Fraudulent': [1] * fraud_samples
}

# Combine non-fraudulent and fraudulent data
combined_data = {key: non_fraud_data[key] + fraud_data[key] for key in non_fraud_data}

# Create a DataFrame and shuffle the rows
data = pd.DataFrame(combined_data)
data = data.sample(frac=1).reset_index(drop=True)

# Save the dataset to a CSV file
data.to_csv('sample_Datasets.csv', index=False)
