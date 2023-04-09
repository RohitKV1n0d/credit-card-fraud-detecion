import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.losses import BinaryCrossentropy
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import tensorflow_federated as tff
import nest_asyncio

nest_asyncio.apply()

# Load the dataset (replace 'data.csv' with the path to your dataset)
data = pd.read_csv('data.csv')

# Preprocess the data
# Convert Time of Day to seconds
data['Time of Day'] = pd.to_datetime(data['Time of Day']).dt.hour * 3600 + pd.to_datetime(data['Time of Day']).dt.minute * 60 + pd.to_datetime(data['Time of Day']).dt.second

# Scale the features using MinMaxScaler or StandardScaler
scaler = MinMaxScaler()
data[['Transaction Amount', 'Time of Day', 'Location']] = scaler.fit_transform(data[['Transaction Amount', 'Time of Day', 'Location']])

# Reshape the data to be 3D for the LSTM layer input (samples, time steps, features)
data_reshaped = np.array(data[['Transaction Amount', 'Time of Day', 'Location']]).reshape(-1, 1, 3)
labels = np.array(data['Fraudulent'])

# Build the LSTM model
def build_lstm_model():
    model = Sequential([
        LSTM(64, activation='relu', input_shape=(1, 3)),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss=BinaryCrossentropy(), metrics=['accuracy'])
    return model

# Federated learning
# Define the TFF computation
@tff.tf_computation(tf.float32, tf.float32)
def create_data_for_federated_learning(X, y):
    return tf.data.Dataset.from_tensor_slices((X, y)).batch(32)

# Divide the dataset for federated learning (simulating multiple clients)
num_clients = 10
client_data = []
client_labels = []

samples_per_client = len(data_reshaped) // num_clients

for i in range(num_clients):
    start = i * samples_per_client
    end = (i + 1) * samples_per_client
    client_data.append(data_reshaped[start:end])
    client_labels.append(labels[start:end])

federated_data = [create_data_for_federated_learning(client_data[i], client_labels[i]) for i in range(num_clients)]

# Train the model using federated learning
trainer = tff.learning.from_keras_model(build_lstm_model, input_spec=federated_data[0].element_spec)
server_state = tff.learning.build_federated_averaging_process(trainer)
state = server_state.initialize()

for round_num in range(10):
    state, metrics = server_state.next(state, federated_data)
    print('round {:2d}, metrics={}'.format(round_num, metrics))

# Transfer learning
# Extract the pre-trained LSTM and dense layers
pretrained_layers = state.model.trainable_variables[:-2]

# Create a new model for transfer learning
transfer_model = Sequential([
    LSTM(64, activation='relu', input_shape=(1, 3)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Set the weights of the pre-trained layers in the new model
transfer_model.set_weights(pretrained_layers)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data_reshaped, labels, test_size=0.2, random_state=42)

# Train the new model with transfer learning
transfer_model.compile(optimizer='adam', loss=BinaryCrossentropy(), metrics=['accuracy'])
transfer_model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)

# Evaluate the new model on the testing set
loss, accuracy = transfer_model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
