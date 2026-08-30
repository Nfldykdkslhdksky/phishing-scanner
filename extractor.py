import re
from urllib.parse import urlparse

def extract_features(url):
    """
    Converts a raw URL string into a list of numerical features 
    that a machine learning model can understand.
    """
    # 1. URL Length (Phishing URLs are often very long to hide the real domain)
    url_length = len(url)
    
    # 2. Number of dots (More dots usually means suspicious subdomains)
    num_dots = url.count('.')
    
    # 3. Presence of '@' symbol (Used by attackers to mask the real destination)
    # We assign 1 for True (exists), 0 for False
    has_at_symbol = 1 if '@' in url else 0
    
    # 4. Check if an IP address is used instead of a normal domain name
    try:
        # urlparse separates the domain from the rest of the link
        domain = urlparse(url).netloc
        # Regular expression to check if the domain looks like an IPv4 address
        has_ip = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain) else 0
    except:
        domain = ""
        has_ip = 0
        
    # 5. Presence of a hyphen in the domain (Often used in fakes like paypal-update.com)
    has_hyphen = 1 if '-' in domain else 0

    # 6. Suspicious word check
    suspicious_words = ['login', 'update', 'secure', 'verify', 'account', 'banking', 'confirm']
    has_suspicious_word = 1 if any(word in url.lower() for word in suspicious_words) else 0
    
    # 7. URL shortener check
    shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'ow.ly']
    is_shortened = 1 if any(shortener in url.lower() for shortener in shorteners) else 0
    
    # 8. HTTPS check (Notice we are checking if it is secure. 1 = Yes, 0 = No)
    is_https = 1 if url.startswith("https://") else 0

    # Return the exact features as a structured list of numbers
    return [url_length, num_dots, has_at_symbol, has_ip, has_hyphen, has_suspicious_word, is_shortened, is_https]
# Let's test the script!
if __name__ == "__main__":
    test_safe_url = "https://www.google.com"
    test_phish_url = "http://192.168.1.1/paypal-update-login@scam.com"
    
    print(f"Safe URL Math: {extract_features(test_safe_url)}")
    print(f"Phishing URL Math: {extract_features(test_phish_url)}")

