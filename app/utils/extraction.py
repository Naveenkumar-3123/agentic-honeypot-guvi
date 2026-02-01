import re

# Extraction Regex Patterns
UPI_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+", re.IGNORECASE)
BANK_ACCOUNT_REGEX = re.compile(r"\b\d{9,18}\b") # Basic 9-18 digit capture
URL_REGEX = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")

def extract_intelligence(text: str) -> dict:
    """
    Extracts structured entities from the text using Regex.
    """
    return {
        "upi_ids": list(set(UPI_REGEX.findall(text))),
        "bank_accounts": list(set(BANK_ACCOUNT_REGEX.findall(text))),
        "phishing_urls": list(set(URL_REGEX.findall(text)))
    }
