import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is not set in environment variables")
        return True
