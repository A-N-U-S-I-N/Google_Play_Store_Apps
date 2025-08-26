import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('cleaned_googleplaystore.csv') 

features = ['Reviews', 'Size_in_bytes', 'Installs', 'Price']
target = 'Rating'

df = df.dropna(subset=features + [target])

if 'Category' in df.columns:
    le = LabelEncoder()
    df['Category_enc'] = le.fit_transform(df['Category'])
    features.append('Category_enc')

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f'RMSE on test set: {rmse:.4f}')

import joblib
joblib.dump(model, 'rf_rating_predictor.pkl')
