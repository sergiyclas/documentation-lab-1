#!/usr/bin/env python3
"""
Demo script for Lab 4: Strategy Pattern Implementation
Shows how to switch between Console and Kafka output strategies without code changes
"""
import sys
import os
import time
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.common.output_strategy import OutputStrategyFactory, ConsoleOutputStrategy
from src.common.logger import get_logger


def demo_console_strategy():
    """Demonstrate console output strategy"""
    print("\n" + "="*70)
    print("🎯 DEMO 1: Console Output Strategy")
    print("="*70)
    
    # Using console strategy directly
    console_strategy = ConsoleOutputStrategy()
    
    messages = [
        ("INFO", "Application started successfully"),
        ("DEBUG", "Reading configuration file"),
        ("INFO", "Connecting to database"),
        ("WARNING", "Database connection slow (500ms)"),
        ("INFO", "Importing CSV data"),
        ("INFO", "Processing 1000 records..."),
        ("INFO", "✅ Data imported successfully: 950 records"),
        ("INFO", "Creating playlists..."),
        ("INFO", "✅ 150 playlists created"),
    ]
    
    for level, msg in messages:
        console_strategy.write(level, msg)
        time.sleep(0.3)
    
    console_strategy.flush()
    print("\nConsole Output Strategy Demo Completed ✓\n")


def demo_kafka_strategy_simulation():
    """Demonstrate Kafka strategy (simulated)"""
    print("\n" + "="*70)
    print("🎯 DEMO 2: Kafka Output Strategy (Simulated)")
    print("="*70)
    
    try:
        kafka_strategy = OutputStrategyFactory.create_strategy(
            "kafka",
            bootstrap_servers="localhost:9092",
            topic="application-logs"
        )
        
        messages = [
            ("INFO", "Kafka strategy initialized"),
            ("INFO", "Sending logs to Kafka topic: application-logs"),
            ("INFO", "Event 1: User registered"),
            ("INFO", "Event 2: Playlist created"),
            ("INFO", "Event 3: Song added to playlist"),
        ]
        
        for level, msg in messages:
            kafka_strategy.write(level, msg)
            time.sleep(0.2)
        
        kafka_strategy.flush()
        print("Kafka Output Strategy Demo Completed ✓\n")
        
    except Exception as e:
        print(f"\n⚠️  Kafka not available: {str(e)}")
        print("To use Kafka strategy, install: pip install -e '.[kafka]'")
        print("and ensure Kafka is running on localhost:9092\n")


def demo_logger_with_strategy():
    """Demonstrate logger integration with strategy pattern"""
    print("\n" + "="*70)
    print("🎯 DEMO 3: Logger with Strategy Pattern Integration")
    print("="*70)
    
    logger = get_logger(__name__)
    
    logger.info("Starting data import process...")
    logger.debug("Reading CSV configuration")
    logger.info("Processing 5000 records from spotify_data.csv")
    
    for i in [1000, 2000, 3000, 4000, 5000]:
        logger.info(f"Processed {i} records")
        time.sleep(0.2)
    
    logger.info("✅ Import completed successfully")
    logger.debug("Total time: 2.5 seconds")
    
    print("\nLogger Integration Demo Completed ✓\n")


def demo_strategy_switching():
    """Demonstrate how to switch strategies at runtime"""
    print("\n" + "="*70)
    print("🎯 DEMO 4: Dynamic Strategy Switching")
    print("="*70)
    print("""
To switch output strategies, use environment variables:

1️⃣  Console Output (Default):
   $env:OUTPUT_TYPE = "console"
   python main.py

2️⃣  Kafka Output:
   $env:OUTPUT_TYPE = "kafka"
   $env:KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
   $env:KAFKA_TOPIC = "application-logs"
   python main.py

3️⃣  Or modify config.py:
   OUTPUT_TYPE = "console"  # or "kafka"
   KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
   KAFKA_TOPIC = "application-logs"

Key Benefit: ✅ No code changes required, only configuration!
    """)


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "Lab 4: Strategy Pattern Implementation" + " "*15 + "║")
    print("║" + " "*68 + "║")
    print("║" + " "*(68 - len("Spotify Platform")) + "Spotify Platform" + " "*20 + "║")
    print("╚" + "="*68 + "╝\n")
    
    try:
        # Run all demos
        demo_console_strategy()
        demo_kafka_strategy_simulation()
        demo_logger_with_strategy()
        demo_strategy_switching()
        
        print("\n" + "="*70)
        print("✅ All Demos Completed Successfully!")
        print("="*70)
        print("""
📚 Lab 4 Implementation Summary:

✓ Strategy Pattern: Abstract base class with multiple implementations
✓ Factory Pattern: OutputStrategyFactory for creating strategies
✓ Configuration-based: Change behavior via environment variables
✓ No Code Changes: All switching happens through config files
✓ Kafka Support: Optional kafka-python for message queue integration
✓ Graceful Fallback: Falls back to console if Kafka unavailable
✓ Logger Integration: All logging uses strategy pattern

📖 Key Files:
- src/common/output_strategy.py  - Strategy implementations
- src/common/logger.py           - Logger with strategy integration
- config.py                      - Configuration management
        """)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
