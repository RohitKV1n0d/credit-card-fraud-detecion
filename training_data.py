import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Load the dataset
data = pd.read_csv('sample_transactions.csv')

# Preprocess the data
encoder_location = LabelEncoder()
encoder_transaction = LabelEncoder()
data['Location'] = encoder_location.fit_transform(data['Location'])
data['Transaction'] = encoder_transaction.fit_transform(data['Transaction'])

# Separate features and target
X = data.drop('Fraudulent', axis=1)
y = data['Fraudulent']

# Scale the numerical features
scaler = StandardScaler()
X[['Amount', 'Time of Day']] = scaler.fit_transform(X[['Amount', 'Time of Day']])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Accuracy Score:\n", accuracy_score(y_test, y_pred))

# Save the trained model, encoders, and scaler
joblib.dump(clf, 'fraud_detection_model.pkl')
joblib.dump(encoder_location, 'encoder_location.pkl')
joblib.dump(encoder_transaction, 'encoder_transaction.pkl')
joblib.dump(scaler, 'standard_scaler.pkl')
