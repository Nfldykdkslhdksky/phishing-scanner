from flask import Flask, render_template, request
import joblib
from extractor import extract_features

app = Flask(__name__)

print("Loading AI model into memory...")
model = joblib.load('phishing_model.pkl')

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    phish_prob = None
    safe_prob = None
    url_input = ""
    
    if request.method == 'POST':
        url_input = request.form['url']
        features = extract_features(url_input)
        
        # predict_proba gives probabilities for [Class 0, Class 1]
        # Class 0 = Phishing, Class 1 = Safe
        probabilities = model.predict_proba([features])[0]
        
        # Convert to percentage and round to 1 decimal place
        phish_prob = round(probabilities[0] * 100, 1)
        safe_prob = round(probabilities[1] * 100, 1)
        
        if phish_prob > 50:
            result = "🚨 DANGER: PHISHING DETECTED!"
        else:
            result = "✅ LIKELY SAFE"
            
    return render_template(
        'index.html', 
        result=result, 
        phish_prob=phish_prob, 
        safe_prob=safe_prob, 
        url=url_input
    )

if __name__ == '__main__':
    app.run(debug=True)