"""
Configuration settings for Spotify application
"""
import os
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent

# Database
DATABASE_URL = "sqlite:///./spotify.db"
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() == "true"

# CSV file path
CSV_FILE_PATH = os.path.join(BASE_DIR, "spotify_data.csv")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# API
API_TITLE = "Spotify Platform API"
API_VERSION = "2.0.0"
API_DESCRIPTION = "3-tier architecture implementation with FastAPI and SQLAlchemy"

# Subscription types
SUBSCRIPTION_TYPES = {
    "FREE": "FreeSubscription",
    "PREMIUM": "PremiumSubscription",
    "STUDENT": "StudentSubscription",
}

# Subscription pricing
SUBSCRIPTION_PRICING = {
    "FreeSubscription": 0.00,
    "PremiumSubscription": 9.99,
    "StudentSubscription": 4.99,
}
