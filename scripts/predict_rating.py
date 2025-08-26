import pandas as pd
import joblib

model = joblib.load('rf_rating_predictor.pkl')

new_data = pd.DataFrame({
    'Reviews': [1200, 15000],
    'Size_in_bytes': [5*1024*1024, 25*1024*1024],
    'Installs': [10000, 500000],
    'Price': [0.0, 4.99],
    'Category_enc': [10, 25]  
})

predictions = model.predict(new_data)
new_data['Predicted_Rating'] = predictions
print(new_data)
