import re
import requests
import json

class WordConverter:
    @staticmethod
    def smart_case_conversion(text):
        """Convert text to smart case (proper case with intelligent capitalization)"""
        if not text:
            return text
            
        # Split text into words
        words = text.split()
        converted_words = []
        
        for word in words:
            # Skip if word is all caps (acronyms)
            if word.isupper() and len(word) > 1:
                converted_words.append(word)
                continue
                
            # Convert to smart case
            # Handle words with apostrophes
            if "'" in word:
                parts = word.split("'")
                if len(parts) == 2:
                    word = parts[0].capitalize() + "'" + parts[1].capitalize()
                else:
                    word = word.capitalize()
            # Handle hyphenated words
            elif "-" in word:
                parts = word.split("-")
                word = "-".join(part.capitalize() for part in parts)
            # Handle numbers with letters
            elif any(c.isdigit() for c in word) and any(c.isalpha() for c in word):
                # Keep numbers as is, capitalize letters
                word = ''.join(c.upper() if c.isalpha() else c for c in word)
            else:
                word = word.capitalize()
                
            converted_words.append(word)
            
        return ' '.join(converted_words)
    
    @staticmethod
    def extract_urls(text):
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+'
        return re.findall(url_pattern, text)
    
    @staticmethod
    def detect_language(text):
        """Detect language using a free API"""
        try:
            # Using a free language detection API
            response = requests.get(
                f"https://api.mymemory.translated.net/get?q={text[:50]}",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('responseData'):
                    return data['responseData'].get('language', 'en')
        except:
            pass
        return 'en'  # Default to English
    
    @staticmethod
    def smart_abbreviation_expander(text):
        """Expand common abbreviations"""
        abbreviations = {
            'ASAP': 'As Soon As Possible',
            'FYI': 'For Your Information',
            'IMO': 'In My Opinion',
            'LOL': 'Laugh Out Loud',
            'OMG': 'Oh My God',
            'BRB': 'Be Right Back',
            'BTW': 'By The Way',
            'IDK': 'I Don\'t Know',
            'JK': 'Just Kidding',
            'TTYL': 'Talk To You Later',
            'SMH': 'Shaking My Head',
            'TBH': 'To Be Honest',
            'IMHO': 'In My Humble Opinion',
            'ROFL': 'Rolling On Floor Laughing',
            'G2G': 'Got To Go',
            'ATM': 'At The Moment',
            'BFF': 'Best Friends Forever',
            'DIY': 'Do It Yourself',
            'ETA': 'Estimated Time of Arrival',
            'FAQ': 'Frequently Asked Questions',
            'AKA': 'Also Known As',
            'RSVP': 'Répondez S\'il Vous Plaît'
        }
        
        words = text.split()
        expanded_words = []
        
        for word in words:
            # Remove punctuation for checking
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word.upper() in abbreviations:
                expanded_words.append(abbreviations[clean_word.upper()])
            else:
                expanded_words.append(word)
                
        return ' '.join(expanded_words)
    
    @staticmethod
    def format_numbers(text):
        """Format numbers in text for better readability"""
        def format_match(match):
            num_str = match.group(0)
            try:
                if '.' in num_str:
                    # Decimal number
                    num = float(num_str)
                    # Format with commas for large numbers
                    if num >= 1000:
                        return f"{num:,.2f}"
                    else:
                        return num_str
                else:
                    # Integer
                    num = int(num_str)
                    if num >= 1000:
                        return f"{num:,}"
                    else:
                        return num_str
            except:
                return num_str
        
        # Find and format numbers
        pattern = r'\d+(?:\.\d+)?'
        return re.sub(pattern, format_match, text)
    
    @staticmethod
    def smart_converter(text):
        """Apply all conversions"""
        # Expand abbreviations
        text = WordConverter.smart_abbreviation_expander(text)
        
        # Apply smart case conversion
        text = WordConverter.smart_case_conversion(text)
        
        # Format numbers
        text = WordConverter.format_numbers(text)
        
        return text
