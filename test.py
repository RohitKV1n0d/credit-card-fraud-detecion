# # Import required libraries
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# # Load the dataset
# creditcard_df = pd.read_csv("creditcard.csv")

# # Explore the data
# print(creditcard_df.head())

# # Check for missing values
# print(creditcard_df.isnull().sum())

# # Check the distribution of class variable
# print(creditcard_df['Class'].value_counts())

# # Visualize the distribution of class variable
# sns.countplot(x='Class', data=creditcard_df)

# # Split the data into train and test sets
# X = creditcard_df.drop('Class', axis=1)
# y = creditcard_df['Class']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# # Scale the data
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# # Create a logistic regression model
# model = LogisticRegression(max_iter=1000)

# # Train the model
# model.fit(X_train, y_train)

# # Predict on the test data
# y_pred = model.predict(X_test)

# # Evaluate the model
# print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
# print("Accuracy score:", accuracy_score(y_test, y_pred))
# print("Classification report:\n", classification_report(y_test, y_pred))




# import csv

# txt_file = "data_preview.txt"
# csv_file = "output.csv"

# with open(txt_file, "r") as infile, open(csv_file, "w", newline='') as outfile:
#     writer = csv.writer(outfile)
#     for line in infile:
#         row = line.strip().split(",")  # Assumes data is separated by commas
#         writer.writerow(row)

import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
random.seed(42)

# Define sample sizes
total_samples = 1000
fraud_samples = total_samples // 2
non_fraud_samples = total_samples - fraud_samples

# Define locations
locations_india = ['Thrissur', 'Coimbatore', 'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore']
non_fraud_locations = ['Thrissur', 'Coimbatore']
locations_fraud = [loc for loc in locations_india if loc not in non_fraud_locations]

# Generate random data for non-fraudulent transactions
non_fraud_data = {
    'Transaction': [random.choice(['Withdrawal', 'Purchase', 'Transfer']) for _ in range(non_fraud_samples)],
    'Amount': [random.randint(1, 5000) for _ in range(non_fraud_samples)],
    'Time of Day': [random.randint(0, 23) for _ in range(non_fraud_samples)],
    'Location': [random.choice(non_fraud_locations) for _ in range(non_fraud_samples)],
    'Fraudulent': [0] * non_fraud_samples
}

# Generate random data for fraudulent transactions
fraud_data = {
    'Transaction': [random.choice(['Withdrawal', 'Purchase', 'Transfer']) for _ in range(fraud_samples)],
    'Amount': [random.randint(20000, 50000) for _ in range(fraud_samples)],
    'Time of Day': [random.choice(list(range(23, 24)) + list(range(0, 6))) for _ in range(fraud_samples)],
    'Location': [random.choice(locations_fraud) for _ in range(fraud_samples)],
    'Fraudulent': [1] * fraud_samples
}

# Combine non-fraudulent and fraudulent data
combined_data = {key: non_fraud_data[key] + fraud_data[key] for key in non_fraud_data}

# Create a DataFrame and shuffle the rows
data = pd.DataFrame(combined_data)
data = data.sample(frac=1).reset_index(drop=True)

# Save the dataset to a CSV file
data.to_csv('sample_transactions.csv', index=False)
