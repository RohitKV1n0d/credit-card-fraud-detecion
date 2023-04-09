import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import BinaryCrossentropy
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

# Load the dataset (replace 'data.csv' with the path to your dataset)
data = pd.read_csv('sample_transactions.csv')

# Preprocess the data
# Convert Time of Day to seconds
data['Time of Day'] = pd.to_datetime(data['Time of Day']).dt.hour * 3600 + pd.to_datetime(data['Time of Day']).dt.minute * 60 + pd.to_datetime(data['Time of Day']).dt.second

# Scale the features using MinMaxScaler or StandardScaler
scaler = MinMaxScaler()
data[['Transaction Amount', 'Time of Day', 'Location']] = scaler.fit_transform(data[['Transaction Amount', 'Time of Day', 'Location']])

# Split the data into training and testing sets
X = data[['Transaction Amount', 'Time of Day', 'Location']]
y = data['Fraudulent']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the ANN model
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,)),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss=BinaryCrossentropy(), metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)

# Evaluate the model on the testing set
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')