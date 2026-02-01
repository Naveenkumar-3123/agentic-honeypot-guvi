import re

# Payment Keywords
PAYMENT_PATTERNS = re.compile(r"(upi|bank|pay|transfer|paytm|gpay|phonepe|wallet|credit card|debit card)", re.IGNORECASE)

# Urgency Indicators
URGENCY_PATTERNS = re.compile(r"(blocked|urgent|immediately|suspend|verify|kyc|24 hours|last chance|expired|action required)", re.IGNORECASE)

# URL Pattern (Simple)
# Specific UPI Scam Phrases
UPI_SCAM_PATTERNS = re.compile(r"(enter upi pin|receive money|scan qt|scan qr|refund.*upi|upi.*refund|upi id.*verify)", re.IGNORECASE)

URL_PATTERN = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")

def check_rule_based_signals(message: str) -> dict:
    """
    Checks for presence of scam keywords and URLs.
    """
    signals = {
        "payment_keywords": bool(PAYMENT_PATTERNS.search(message)),
        "urgency_keywords": bool(URGENCY_PATTERNS.search(message)),
        "contains_url": bool(URL_PATTERN.search(message)),
        "upi_scam_specific": bool(UPI_SCAM_PATTERNS.search(message))
    }
    
    # Boost payment signal if specific UPI scam pattern is found
    if signals["upi_scam_specific"]:
        signals["payment_keywords"] = True
        
    return signals
