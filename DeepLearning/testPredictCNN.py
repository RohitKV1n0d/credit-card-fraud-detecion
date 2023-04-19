import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder

# Load the trained model
model = load_model('cnn_ann_model.h5')

# Load the original dataset
data = pd.read_csv('sample_transactions.csv')
X = data.drop(['Fraudulent'], axis=1)

# Prepare the OneHotEncoder for categorical features
enc = OneHotEncoder(sparse=False)
enc.fit(X.select_dtypes(include=['object']))


def predict(transaction, amount, time_of_day, location):
    # Sample inputs
    sample_inputs = pd.DataFrame({
        'Transaction': [transaction],
        'Amount': [amount],
        'Time of Day': [time_of_day],
        'Location': [location]
    })

    # Preprocess the sample inputs
    sample_inputs_encoded = pd.DataFrame(enc.transform(sample_inputs.select_dtypes(include=['object'])))
    sample_inputs_encoded.columns = enc.get_feature_names_out(sample_inputs.select_dtypes(include=['object']).columns)
    sample_inputs = sample_inputs.drop(sample_inputs.select_dtypes(include=['object']).columns, axis=1)
    sample_inputs = pd.concat([sample_inputs, sample_inputs_encoded], axis=1)

    # Convert the sample inputs to float format
    sample_inputs = sample_inputs.astype('float32')

    # Reshape the sample inputs for the CNN-ANN model
    sample_inputs = np.expand_dims(sample_inputs.values, axis=-1)

    # Make predictions using the model
    predictions = model.predict(sample_inputs)
    predictions = np.round(predictions)

    # Print the predictions
    for i, prediction in enumerate(predictions):
        if prediction == 0:
            print(f'Sample {i + 1} is predicted to be Legitimate')
            return False
        else:
            print(f'Sample {i + 1} is predicted to be Fraudulent')
            return True
