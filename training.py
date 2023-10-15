import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# Assuming df is your DataFrame
sampled_df = df.sample(n=10000, random_state=1)


# 1. Feature Engineering: (Generic since data is not provided)
# Extracting hour from a hypothetical 'time' column as an example
sampled_df['HOUR'] = pd.to_datetime(sampled_df['CRASH TIME']).dt.hour

# Extract relevant information from 'CRASH DATE' column
sampled_df['CRASH DATE'] = pd.to_datetime(sampled_df['CRASH DATE'])
sampled_df['Year'] = sampled_df['CRASH DATE'].dt.year
sampled_df['Month'] = sampled_df['CRASH DATE'].dt.month
sampled_df['Day'] = sampled_df['CRASH DATE'].dt.day

# Drop the original 'CRASH DATE' column
sampled_df.drop(['CRASH DATE'], axis=1, inplace=True)

# Drop columns that are unlikely to be relevant or have too many missing values
sampled_df.drop(['CRASH TIME', 'LOCATION', 'OFF STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME',
           'CONTRIBUTING FACTOR VEHICLE 3', 'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5'],
          axis=1, inplace=True)

# Separate the target variable
y = sampled_df['NUMBER OF MOTORIST KILLED']
sampled_df.drop(['NUMBER OF MOTORIST KILLED'], axis=1, inplace=True)

# Handle missing values (replace NaN with the median for numeric columns)
numeric_cols = sampled_df.select_dtypes(include='number').columns
imputer = SimpleImputer(strategy='median')
sampled_df[numeric_cols] = imputer.fit_transform(sampled_df[numeric_cols])

# Encode categorical variables (assuming 'BOROUGH' is categorical)
label_encoder = LabelEncoder()
sampled_df['BOROUGH'] = label_encoder.fit_transform(sampled_df['BOROUGH'])

# One-hot encode categorical columns
categorical_cols = ['ON STREET NAME', 'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2', 'VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2']
sampled_df = pd.get_dummies(sampled_df, columns=categorical_cols)

# Convert ZIP CODE to numeric (assuming it's a feature)
sampled_df['ZIP CODE'] = pd.to_numeric(sampled_df['ZIP CODE'], errors='coerce')

# 3. Data Split:
# Assume 'target' is the variable you want to predict
X = sampled_df  # No need to drop the target variable here
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# 4. Model Setup:
xgb_regressor = xgb.XGBRegressor(objective='reg:squarederror', seed=42)

# 5. Hyperparameter Tuning: Grid Search
# Define the best parameters obtained from Grid Search
best_params = {
    'max_depth': 3,
    'learning_rate': 0.01,
    'n_estimators': 100
}


# Fitting model
grid_search.fit(X_train, y_train)

# Best parameters and model
print(f'Best parameters: {grid_search.best_params_}')
best_model = grid_search.best_estimator_

# 6. Model Evaluation:
y_pred = best_model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f'RMSE: {rmse}')
