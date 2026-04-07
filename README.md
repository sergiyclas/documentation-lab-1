# 🎵 Spotify Platform - Complete Implementation

# Лабораторна 4: GoF Паттерн Стратегія 🎯

## Опис реалізації

Реалізовано паттерн **Strategy** для відділення логіки виводу даних від основного коду. Дозволяє динамічно переключатися між консольним та Kafka розповсюджувачем **без змін кода**.

## ✅ Що було реалізовано

### 1. **Strategy Pattern**
- ✅ Абстрактний клас `OutputStrategy` з методами `write()` та `flush()`
- ✅ Конкретні реалізації: `ConsoleOutputStrategy` та `KafkaOutputStrategy`
- ✅ Factory Pattern для створення стратегій (`OutputStrategyFactory`)
- ✅ Можливість реєстрації власних стратегій в runtime

### 2. **Kafka Integration**
- ✅ Kafka producer для відправки логів до topic
- ✅ JSON серіалізація повідомлень
- ✅ Graceful fallback на консоль при помилці Kafka
- ✅ Автоматичне закриття producer

### 3. **Configuration-based Switching**
- ✅ Переключення через змінні середовища (env vars)
- ✅ Мінімальні зміни в коді (тільки конфіг)
- ✅ Підтримка різних параметрів для кожної стратегії

### 4. **Logger Integration**
- ✅ Custom handler для інтеграції logging з strategies
- ✅ Глобальна стратегія для всіх logger'ів
- ✅ Ліниве ініціалізування (lazy initialization)

## 🏗️ Архітектура Strategy Pattern

```
┌─────────────────────────────────────┐
│        OutputStrategy (ABC)         │  ← Абстрактна стратегія
│    - write(level, message)          │
│    - flush()                        │
└────────┬───────────────────┬────────┘
         │                   │
┌────────▼───────┐    ┌──────▼──────────┐
│  ConsoleOutput │    │  KafkaOutput    │
│    Strategy    │    │   Strategy      │
│  (файл/stdout) │    │  (message queue)│
└────────┬───────┘    └──────┬──────────┘
         │                   │
         └───────┬───────────┘
                 │
         ┌───────▼──────────┐
         │OutputStrategy   │
         │  Factory        │  ← Factory для створення
         │ create_strategy │
         └───────┬──────────┘
                 │
         ┌───────▼──────────┐
         │  get_logger()    │  ← Интеграция с logger'ом
         │ (StrategyHandler)│
         └──────────────────┘
```

## 🔧 Конфігурація

### Console Output (За замовчуванням)
```bash
# config.py
OUTPUT_TYPE = "console"

# Або через env vars
$env:OUTPUT_TYPE = "console"
python main.py
```

### Kafka Output
```bash
# 1. Запустити Kafka локально (Docker)
docker run -d --name kafka -p 9092:9092 confluentinc/cp-kafka:latest

# 2. Встановити OUTPUT_TYPE
$env:OUTPUT_TYPE = "kafka"
$env:KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# 3. Запустити demo
uv run .\demo_strategy.py

# config.py
OUTPUT_TYPE = "kafka"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "application-logs"

# Або через env vars
$env:OUTPUT_TYPE = "kafka"
$env:KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
$env:KAFKA_TOPIC = "application-logs"
python main.py
```

## 📝 Передача даних

### Console Strategy
```
[2026-03-29 14:30:45,123] - root - INFO - User created: user@example.com
[2026-03-29 14:30:46,456] - root - INFO - Playlist created: My Favorite Songs
```

### Kafka Strategy
```json
{
  "level": "INFO",
  "message": "User created: user@example.com",
  "timestamp": "2026-03-29 14:30:45.123456"
}
```

## 📦 Залежності

### Основні (для Console)
```
Вже включені в основні залежності (FastAPI, logging, etc.)
```

### Kafka (опціональне)
```bash
pip install -e ".[kafka]"
# або
pip install kafka-python>=2.0.0
```

## 🚀 Демонстрація

### Запуск demo скрипту
```bash
python demo_strategy.py
```

Скрипт демонструє:
1. Console Output Strategy
2. Kafka Output Strategy (with fallback)
3. Logger integration with Strategy
4. Dynamic strategy switching

## 📂 Файли реалізації

| Файл | Функція |
|------|---------|
| `src/common/output_strategy.py` | Реалізація стратегій і factory |
| `src/common/logger.py` | Integration з logging module |
| `config.py` | Конфігурація стратегій |
| `demo_strategy.py` | Demo скрипт для демонстрації |
| `pyproject.toml` | Зависимости (kafka опціональна) |

## ✨ Особливості Реалізації

### ✅ SOLID Принципи
- **SRP** - Кожна стратегія має одну відповідальність
- **OCP** - Легко додати нові стратегії без змін існуючих
- **LSP** - Всі стратегії дотримуються контракту OutputStrategy
- **ISP** - Мінімальні методи (write, flush)
- **DIP** - Залежність на OutputStrategy, не на конкретних реалізаціях

### ✅ Design Patterns
- **Strategy** - Кілька алгоритмів в одному інтерфейсі
- **Factory** - OutputStrategyFactory для створення стратегій
- **Dependency Injection** - Через конфіг параметри
- **Null Object** - Graceful fallback на консоль

### ✅ Good Practices
- Type hints для всіх методів
- Docstrings для документації
- Error handling з informative повідомленнями
- Ліниве ініціалізування ресурсів
- Resource cleanup (close методи)

## 🧪 Тестування

### Тест Console Strategy
```python
from src.common.output_strategy import ConsoleOutputStrategy

strategy = ConsoleOutputStrategy()
strategy.write("INFO", "Test message")
strategy.flush()
```

### Тест Kafka Strategy
```python
from src.common.output_strategy import OutputStrategyFactory

strategy = OutputStrategyFactory.create_strategy(
    "kafka",
    bootstrap_servers="localhost:9092",
    topic="test-logs"
)
strategy.write("INFO", "Test message")
strategy.flush()
```

### Тест Logger Integration
```python
from src.common.logger import get_logger

logger = get_logger(__name__)
logger.info("Application started")
logger.warning("Low disk space")
logger.error("Connection failed")
```

## 🔄 Реалізація Custom Strategy

Щоб додати власну стратегію:

```python
from src.common.output_strategy import OutputStrategy, OutputStrategyFactory

class FileOutputStrategy(OutputStrategy):
    def __init__(self, filename="logs.txt"):
        self.filename = filename
    
    def write(self, level: str, message: str) -> None:
        with open(self.filename, "a") as f:
            f.write(f"[{level}] {message}\n")
    
    def flush(self) -> None:
        pass

# Реєстрація стратегії
OutputStrategyFactory.register_strategy("file", FileOutputStrategy)

# Використання
strategy = OutputStrategyFactory.create_strategy("file", filename="app.log")
strategy.write("INFO", "Message to file")
```