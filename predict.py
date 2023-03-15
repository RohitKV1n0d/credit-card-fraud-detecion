import numpy as np
import tensorflow as tf

# Load the saved model and preprocessed data
model = tf.keras.models.load_model('best_model.h5')
X_mean = np.load('X_mean.npy')
X_std = np.load('X_std.npy')
pca_matrix = np.load('pca_matrix.npy')

# Prepare input data
amount = 100.0  # replace with user input
time = 172792.0  # replace with user input
input_data = np.array([[amount, time]])

# Standardize the input data
input_data = (input_data - X_mean) / X_std

# Apply PCA transformation to input data
input_data_pca = np.dot(input_data, pca_matrix.T)

# Make a prediction using the loaded model
y_pred = model.predict(input_data_pca)

# Convert the prediction to a binary label
y_pred_label = np.argmax(y_pred, axis=1)

print(y_pred_label)
