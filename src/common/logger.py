# src/common/logger.py

"""Logger configuration with Strategy pattern"""

import logging
from config import LOG_LEVEL, OUTPUT_TYPE, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from src.common.output_strategy import OutputStrategyFactory

# Global strategy instance (lazy initialization)
_output_strategy = None


def _get_output_strategy():
    """Get or create output strategy instance"""
    global _output_strategy
    
    if _output_strategy is None:
        try:
            if OUTPUT_TYPE.lower() == "kafka":
                _output_strategy = OutputStrategyFactory.create_strategy(
                    "kafka",
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                    topic=KAFKA_TOPIC,
                )
            else:
                _output_strategy = OutputStrategyFactory.create_strategy("console")
        except Exception as e:
            # Fallback to console if strategy creation fails
            print(f"Warning: Failed to initialize {OUTPUT_TYPE} strategy, falling back to console: {e}")
            _output_strategy = OutputStrategyFactory.create_strategy("console")
    
    return _output_strategy


def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger instance with strategy-based output
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Create a custom handler that uses the output strategy
        class StrategyHandler(logging.Handler):
            """Custom handler that uses output strategy"""
            
            def emit(self, record):
                try:
                    msg = self.format(record)
                    strategy = _get_output_strategy()
                    strategy.write(record.levelname, msg)
                except Exception:
                    self.handleError(record)
        
        handler = StrategyHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)

    return logger


def flush_output():
    """Flush output strategy"""
    strategy = _get_output_strategy()
    strategy.flush()


def close_output():
    """Close output strategy (e.g., for Kafka)"""
    global _output_strategy
    if _output_strategy:
        if hasattr(_output_strategy, 'close'):
            _output_strategy.close()
        _output_strategy = None
