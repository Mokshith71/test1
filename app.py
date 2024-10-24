import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load the dataset
df = pd.read_csv('BoneTumorDataset.csv')

# Preprocessing: Convert categorical columns to numeric using one-hot encoding
df_encoded = pd.get_dummies(df.drop(columns=['Patient ID']), drop_first=True)

# Define the target variable (y) and features (X)
# Handle the patient status labels for NED, AWD, D
y = df_encoded[['Status (NED, AWD, D)_D', 'Status (NED, AWD, D)_NED']].idxmax(axis=1).apply(lambda x: x.split('_')[-1])
y = y.replace({'NED': 'NED', 'D': 'D'}).fillna('AWD')  # Replace missing values with 'AWD'

# Drop the status columns from the feature set
X = df_encoded.drop(columns=['Status (NED, AWD, D)_D', 'Status (NED, AWD, D)_NED'])

# Train-test split (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Evaluate the model
report = classification_report(y_test, y_pred)
print(report)
