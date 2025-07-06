"""
Utility functions for the Daily Motivation Bot.
"""

from datetime import datetime
from typing import Tuple


def get_french_date_info() -> Tuple[str, int]:
    """
    Get current date information in French format.
    
    Returns:
        Tuple[str, int]: (formatted_date_string, day_of_year)
    """
    today = datetime.now()
    date_str = today.strftime("%d %B %Y")
    day_of_year = today.timetuple().tm_yday
    return date_str, day_of_year


def sanitize_quote(quote: str) -> str:
    """
    Clean and sanitize a quote by removing surrounding quotes.
    
    Args:
        quote: Raw quote string that may have surrounding quotes
        
    Returns:
        str: Cleaned quote without surrounding quotes
    """
    quote = quote.strip()
    
    # Remove surrounding quotes if present
    if quote.startswith('"') and quote.endswith('"'):
        quote = quote[1:-1]
    if quote.startswith("'") and quote.endswith("'"):
        quote = quote[1:-1]
    
    return quote.strip()

