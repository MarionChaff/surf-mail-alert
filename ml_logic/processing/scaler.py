import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# for NN only

class Scaler:

    def __init__(self, features):
        self.preprocessor = ColumnTransformer(transformers=[
            ('minmax', MinMaxScaler(), ['wind_speed', 'wind_dir', 'swell_dir']),
            ('standard', StandardScaler(), ['swell_height', 'swell_period'])
        ], remainder='passthrough')
        self.features = features

    def fit(self, X):
        X = X[self.features]
        self.preprocessor.fit(X)
        return self

    def transform(self, X):
        X = X[self.features]
        X_scaled = pd.DataFrame(self.preprocessor.transform(X),columns=X.columns)
        print("✅ Features scaled")
        return X_scaled

