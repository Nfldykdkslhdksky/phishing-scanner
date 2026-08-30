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
        
        # --- THE NEW WHITELIST ---
        trusted_domains = ['instagram.com', 'google.com', 'youtube.com', 'github.com', 'wikipedia.org',# --- THE EXPANDED WHITELIST ---
        
            # Search & Tech Giants
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com', 'yahoo.com',
            
            # Social Media & Communications
            'instagram.com', 'facebook.com', 'x.com', 'twitter.com', 'linkedin.com', 
            'reddit.com', 'discord.com', 'whatsapp.com',
            
            # Media & Entertainment
            'youtube.com', 'netflix.com', 'spotify.com', 'twitch.tv',
            
            # Developer & Data Tools
            'github.com', 'stackoverflow.com', 'kaggle.com', 'wikipedia.org',
            
            # Gaming Networks
            'hoyoverse.com', 'hoyolab.com', 'rockstargames.com', 'krafton.com'
        ]
        
        # Check if any trusted domain is inside the URL
        if any(domain in url_input.lower() for domain in trusted_domains):
            result = "✅ LIKELY SAFE (Verified Trusted Domain)"
            phish_prob = 0.0
            safe_prob = 100.0
            
        else:
            # If it's not a famous domain, let the AI decide!
            features = extract_features(url_input)
            probabilities = model.predict_proba([features])[0]
            
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