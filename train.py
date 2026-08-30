import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from extractor import extract_features 

print("1. Loading dataset...")
df = pd.read_csv('dataset.csv')
df = df.sample(50000, random_state=42)

print("2. Extracting features from CSV... (This takes a few minutes!)")
features_list = df['url'].apply(extract_features).tolist()

# The updated 8 columns!
X = pd.DataFrame(features_list, columns=[
    'url_length', 'num_dots', 'has_at_symbol', 'has_ip', 'has_hyphen', 
    'has_suspicious_word', 'is_shortened', 'is_https'
])

y = df['status'] 

print("3. Training the Random Forest AI model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("4. Saving the model for the web interface...")
joblib.dump(model, 'phishing_model.pkl')
print("✅ Saved successfully as 'phishing_model.pkl'!")