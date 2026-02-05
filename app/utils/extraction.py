import re

# Extraction Regex Patterns
UPI_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+", re.IGNORECASE)
BANK_ACCOUNT_REGEX = re.compile(r"\b\d{11,18}\b") # More specific for bank accounts (usually 11+ digits)
URL_REGEX = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
PHONE_REGEX = re.compile(r"(?:\+91|91|0)?[6-9]\d{9}\b")
KEYWORDS = ["blocked", "urgent", "immediately", "suspend", "verify", "kyc", "pin", "otp", "login", "password"]

def extract_intelligence(text: str) -> dict:
    """
    Extracts structured entities from the text using Regex.
    """
    # Clean up UPI ids (remove trailing periods often found in sentences)
    upi_ids = [upi.rstrip('.') for upi in UPI_REGEX.findall(text)]
    
    # Strip trailing periods from URLs
    phishing_urls = [url.rstrip('.') for url in URL_REGEX.findall(text)]
    
    # Extract phone numbers first
    phone_numbers = list(set(PHONE_REGEX.findall(text)))
    
    # Extract bank accounts, ensuring they are not also captured as phone numbers
    all_digit_sequences = BANK_ACCOUNT_REGEX.findall(text)
    bank_accounts = [acc for acc in all_digit_sequences if acc not in phone_numbers]
    
    return {
        "upi_ids": list(set(upi_ids)),
        "bank_accounts": list(set(bank_accounts)),
        "phishing_urls": list(set(phishing_urls)),
        "phone_numbers": phone_numbers,
        "suspicious_keywords": [word for word in KEYWORDS if word.lower() in text.lower()]
    }
