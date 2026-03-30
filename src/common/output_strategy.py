# src/common/output_strategy.py

"""Output Strategy pattern implementation for flexible logging"""

from abc import ABC, abstractmethod
from typing import Optional
import logging


class OutputStrategy(ABC):
    """Abstract base class for output strategies"""

    @abstractmethod
    def write(self, level: str, message: str) -> None:
        """
        Write log message
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Message to write
        """
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush any buffered data"""
        pass


class ConsoleOutputStrategy(OutputStrategy):
    """Console output strategy - writes to stdout/stderr using logging"""

    def __init__(self):
        """Initialize console strategy"""
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.handler.setFormatter(self.formatter)

    def write(self, level: str, message: str) -> None:
        """Write message to console"""
        logger = logging.getLogger()
        
        # Map string level to logging level
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        
        log_level = level_map.get(level.upper(), logging.INFO)
        logger.log(log_level, message)

    def flush(self) -> None:
        """Flush console handler"""
        if hasattr(self.handler, "flush"):
            self.handler.flush()


class KafkaOutputStrategy(OutputStrategy):
    """Kafka output strategy - writes to Kafka topic"""

    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        topic: str = "application-logs",
    ):
        """
        Initialize Kafka strategy
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Kafka topic name
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer: Optional[object] = None
        self._initialize_producer()

    def _initialize_producer(self) -> None:
        """Initialize Kafka producer"""
        try:
            from kafka import KafkaProducer
            import json

            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        except ImportError:
            raise ImportError(
                'kafka-python is required for KafkaOutputStrategy. Install with: pip install kafka-python'
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Kafka producer: {str(e)}")

    def write(self, level: str, message: str) -> None:
        """Send message to Kafka"""
        if not self.producer:
            raise RuntimeError("Kafka producer not initialized")

        try:
            log_record = {
                "level": level.upper(),
                "message": message,
                "timestamp": str(__import__("datetime").datetime.now()),
            }
            self.producer.send(self.topic, value=log_record)
        except Exception as e:
            # Fallback to console if Kafka fails
            console_strategy = ConsoleOutputStrategy()
            console_strategy.write(
                "ERROR", f"Failed to send to Kafka: {str(e)}. Message: {message}"
            )

    def flush(self) -> None:
        """Flush Kafka producer"""
        if self.producer:
            self.producer.flush()

    def close(self) -> None:
        """Close Kafka producer"""
        if self.producer:
            self.producer.close()


class OutputStrategyFactory:
    """Factory for creating output strategies"""

    _strategies = {
        "console": ConsoleOutputStrategy,
        "kafka": KafkaOutputStrategy,
    }

    @classmethod
    def create_strategy(
        cls, strategy_type: str, **kwargs
    ) -> OutputStrategy:
        """
        Create output strategy instance
        
        Args:
            strategy_type: Type of strategy ('console' or 'kafka')
            **kwargs: Strategy-specific arguments
            
        Returns:
            OutputStrategy instance
            
        Raises:
            ValueError: If strategy type is unknown
        """
        strategy_class = cls._strategies.get(strategy_type.lower())
        if not strategy_class:
            raise ValueError(
                f"Unknown strategy type: {strategy_type}. "
                f"Available strategies: {', '.join(cls._strategies.keys())}"
            )
        return strategy_class(**kwargs)

    @classmethod
    def register_strategy(cls, name: str, strategy_class: type) -> None:
        """
        Register custom strategy
        
        Args:
            name: Name for the strategy
            strategy_class: Strategy class to register
        """
        cls._strategies[name.lower()] = strategy_class
