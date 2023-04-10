import pandas as pd
import numpy as np
import tensorflow as tf 
from keras.models import Sequential
from keras.layers import Dense
from keras.losses import BinaryCrossentropy
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

# Load the dataset (replace 'data.csv' with the path to your dataset)
data = pd.read_csv('sample_Datasets.csv')

# Preprocess the data
# Convert Time of Day to seconds
data['Time of Day'] = pd.to_datetime(data['Time of Day']).dt.hour * 3600 + pd.to_datetime(data['Time of Day']).dt.minute * 60 + pd.to_datetime(data['Time of Day']).dt.second

# One-hot encode the 'Location' and 'Purchase' columns
data = pd.get_dummies(data, columns=['Location', 'Transaction'])

# Scale the features using MinMaxScaler
scaler = MinMaxScaler()
data[['Amount', 'Time of Day']] = scaler.fit_transform(data[['Amount', 'Time of Day']])

# Split the data into training and testing sets
X = data.drop(columns=['Fraudulent'])
y = data['Fraudulent']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# Build the ANN model
input_shape = X_train.shape[1]

model = Sequential([
    Dense(64, activation='relu', input_shape=(input_shape,)),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
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


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Predict on the test set
y_pred = (model.predict(X_test) > 0.5).astype("int32")

# Calculate performance metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_mat = confusion_matrix(y_test, y_pred)
print('======================================== Performance Metrics ======================================== ')

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1-score: {f1}')
print(f'Confusion Matrix:\n {conf_mat}')

