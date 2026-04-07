# config.py
"""
Configuration settings for Spotify application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Database
DATABASE_URL = "sqlite:///./spotify.db"
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() == "true"

# CSV file path
CSV_FILE_PATH = os.path.join(BASE_DIR, "spotify_data.csv")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Output Strategy Configuration
OUTPUT_TYPE = os.getenv("OUTPUT_TYPE", "console")  # 'console' or 'kafka'

# Kafka Configuration (used when OUTPUT_TYPE='kafka')
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "application-logs")

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
