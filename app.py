from flask import Flask, render_template, request
import joblib
from extractor import extract_features

app = Flask(__name__)

print("Loading AI model into memory...")
model = joblib.load('phishing_model.pkl')

@app.route('/', methods=['GET', 'POST'])
def home():
    # 1. Initialize variables as empty for the first page load!
    result = None
    phish_prob = None
    safe_prob = None
    url_input = ""
    
    if request.method == 'POST':
        url_input = request.form['url']
        features = extract_features(url_input)
        
        probabilities = model.predict_proba([features])[0]
        
        phish_prob = round(probabilities[0] * 100, 1)
        safe_prob = round(probabilities[1] * 100, 1)
        
        if phish_prob > 50:
            result = "🚨 DANGER: PHISHING DETECTED!"
        else:
            result = "✅ LIKELY SAFE"
            
    # 2. Now, whether it's the first load or a scan, these variables exist!
    return render_template(
        'index.html', 
        result=result, 
        phish_prob=phish_prob, 
        safe_prob=safe_prob, 
        url=url_input
    )

if __name__ == '__main__':
    app.run(debug=True)