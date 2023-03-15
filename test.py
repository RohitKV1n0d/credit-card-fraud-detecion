# Import required libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# Load the dataset
creditcard_df = pd.read_csv("creditcard.csv")

# Explore the data
print(creditcard_df.head())

# Check for missing values
print(creditcard_df.isnull().sum())

# Check the distribution of class variable
print(creditcard_df['Class'].value_counts())

# Visualize the distribution of class variable
sns.countplot(x='Class', data=creditcard_df)

# Split the data into train and test sets
X = creditcard_df.drop('Class', axis=1)
y = creditcard_df['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a logistic regression model
model = LogisticRegression(max_iter=1000)

# Train the model
model.fit(X_train, y_train)

# Predict on the test data
y_pred = model.predict(X_test)

# Evaluate the model
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
print("Accuracy score:", accuracy_score(y_test, y_pred))
print("Classification report:\n", classification_report(y_test, y_pred))
