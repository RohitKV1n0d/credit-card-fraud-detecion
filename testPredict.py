import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Prediction phase

# Load the saved model, encoders, and scaler
loaded_model = joblib.load('fraud_detection_model.pkl')
encoder_location = joblib.load('encoder_location.pkl')
encoder_transaction = joblib.load('encoder_transaction.pkl')
scaler = joblib.load('standard_scaler.pkl')



def predict(transaction,amount,time,location):
    # Prepare the input data for prediction 
    input_data = {
    'Transaction': transaction,
    'Amount': amount,
    'Time of Day': time,
    'Location': location
    }

    # Preprocess the input data
    input_df = pd.DataFrame([input_data])
    input_df['Transaction'] = encoder_transaction.transform(input_df['Transaction'])
    input_df['Location'] = encoder_location.transform(input_df['Location'])
    input_df[['Amount', 'Time of Day']] = scaler.transform(input_df[['Amount', 'Time of Day']])

    # Make a prediction using the loaded model
    prediction = loaded_model.predict(input_df)

    # Print the prediction result (0 for non-fraud, 1 for fraud)
    return prediction[0]

# Run the prediction
# print(predict('Purchase', 100, 12, 'Coimbatore'))
