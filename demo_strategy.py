#!/usr/bin/env python3
"""
Minimal Demo script for Lab 4: Strategy Pattern Implementation
Demonstrates switching between Console and Kafka output strategies.
"""
import sys
import os
import time

# Add src directory to Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.common.output_strategy import OutputStrategyFactory, ConsoleOutputStrategy
from src.common.logger import get_logger, close_output

def run_minimal_demo():
    print("\n--- DEMO 1: Direct Console Strategy ---")
    # Explicitly instantiate and use the Console Strategy
    console_strategy = ConsoleOutputStrategy()
    console_strategy.write("INFO", "This message is handled directly by ConsoleOutputStrategy.")
    console_strategy.flush()
    time.sleep(0.5)

    print("\n--- DEMO 2: Direct Kafka Strategy ---")
    try:
        # Use the Factory to instantiate the Kafka Strategy
        kafka_strategy = OutputStrategyFactory.create_strategy(
            "kafka",
            bootstrap_servers="localhost:9092",
            topic="spotify_data_topic"
        )
        kafka_strategy.write("INFO", "This message is handled directly by KafkaOutputStrategy.")
        kafka_strategy.flush()
        
        # FIX: Explicitly close the Kafka connection to prevent KafkaTimeoutError
        if hasattr(kafka_strategy, 'close'):
            kafka_strategy.close()
            
        print("✅ Success: Message silently sent to Kafka broker (topic: spotify_data_topic).")
    except Exception as e:
        print(f"⚠️ Fallback: Kafka is unavailable ({str(e)}). Ensure Docker container is running.")

    time.sleep(0.5)

    print("\n--- DEMO 3: Application Logger Integration ---")
    # The application logger automatically determines which strategy to use 
    # based on the OUTPUT_TYPE variable in the .env file or config.py
    current_strategy = os.getenv("OUTPUT_TYPE", "CONSOLE").upper()
    print(f"Current .env configuration: OUTPUT_TYPE = {current_strategy}")
    
    logger = get_logger(__name__)
    logger.info("This log entry was processed by the global strategy logger.")
    
    print("\n✅ Minimal Demo Completed.\n")
    
    # FIX: Explicitly close the global logger's Kafka connection before exiting
    close_output()

if __name__ == "__main__":
    try:
        run_minimal_demo()
    except KeyboardInterrupt:
        print("\nDemo interrupted.")
        sys.exit(0)