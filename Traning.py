import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint

# Load the dataset
data = pd.read_csv('creditcard.csv')

# Split the data into X and y
X = data.drop('Class', axis=1)
y = data['Class']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the mean and standard deviation for future use
np.save('X_mean.npy', scaler.mean_)
np.save('X_std.npy', scaler.scale_)

# Apply PCA transformation
pca = PCA(n_components=23, svd_solver='full')
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

# Save the PCA matrix for future use
np.save('pca_matrix.npy', pca.components_)

# Define the model
model = Sequential([
    Dense(units=32, activation='relu', input_dim=23),
    Dropout(0.2),
    Dense(units=16, activation='relu'),
    Dropout(0.2),
    Dense(units=1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Define a checkpoint callback to save the best model
checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True, monitor='val_loss', mode='min', verbose=1)

# Train the model
history = model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test), callbacks=[checkpoint])

# Load the best model
model.load_weights('best_model.h5')

# Make a prediction on new data
amount = 100.0
time = 86400
input_data = np.array([[amount, time]])
input_data = (input_data - scaler.mean_) / scaler.scale_
input_data = pca.transform(input_data)
prediction = model.predict(input_data)
print(prediction)
