import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
df = pd.read_csv("sample_transactions.csv")

# Display first few rows of the dataset
print(df.head())

# Visualize the distribution of the 'Fraudulent' column
sns.countplot(data=df, x="Fraudulent")
plt.title("Fraud vs Non-Fraud Transactions")
plt.show()

# Visualize the relationship between 'Amount' and 'Fraudulent'
sns.boxplot(data=df, x="Fraudulent", y="Amount")
plt.title("Transaction Amount vs Fraud")
plt.show()

# Visualize the relationship between 'Time of Day' and 'Fraudulent'
sns.boxplot(data=df, x="Fraudulent", y="Time of Day")
plt.title("Transaction Time vs Fraud")
plt.show()

# Visualize the relationship between 'Location' and 'Fraudulent'
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="Location", hue="Fraudulent")
plt.title("Transaction Location vs Fraud")
plt.show()