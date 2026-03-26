# 🎵 Spotify Platform - Python/FastAPI Implementation

**Варіант:** 12 | **Техстек:** Python, FastAPI, SQLAlchemy, SQLite3

## 📋 Опис проекту

Це переписана реалізація документаційної лабораторної роботи на **Python стеку с FastAPI** замість TypeScript/NestJS. Проект реалізує ту ж **трирівневу архітектуру** (Presentation Layer, Business Logic Layer, Data Access Layer) з дотриманням SOLID принципів.

## 🏗️ Архітектура проекту

```
┌─────────────────────────────────────────────────────┐
│          Presentation Layer (PL)                    │
│         FastAPI Routes & HTTP Handlers              │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│      Business Logic Layer (BLL)                     │
│  SpotifyService, StatisticsService                 │
│  (CSV Import, управління даними)                  │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│      Data Access Layer (DAL)                        │
│  Repository Pattern + SQLAlchemy                   │
│  (User, Song, Playlist, Subscription)             │
└─────────────────────────────────────────────────────┘
```

### Файлова структура

```
src/
├── common/                      # Спільні утиліти
│   ├── __init__.py
│   ├── logger.py                # Логування
│   └── constants.py             # Константи
│
├── pl/                          # Presentation Layer
│   ├── __init__.py
│   └── routes.py                # FastAPI маршрути
│
├── bll/                         # Business Logic Layer
│   ├── __init__.py
│   └── services.py              # SpotifyService, StatisticsService
│
├── dal/                         # Data Access Layer
│   ├── __init__.py
│   ├── database.py              # Налаштування БД та сесій
│   ├── models.py                # SQLAlchemy моделі
│   └── repositories.py          # DataAccessService
│
├── generators/                  # Генератори
│   ├── __init__.py
│   └── generate_csv.py          # Генератор тестових CSV даних
│
├── __init__.py
└── main.py                      # FastAPI додаток
│
config.py                        # Конфігурація
main.py                         # Entry point
cli.py                          # Утиліти CLI
requirements.txt                # Python залежності
.env.example                    # Приклад конфігурації
```

## 📚 Сутності базі даних

### User (Користувач)
```python
- id: int (Primary Key)
- email: str (UNIQUE)
- username: str
- subscription_id: int (Foreign Key)
- registration_date: DateTime
- is_active: bool
- Relations:
  - subscription: OneToOne → Subscription
  - playlists: OneToMany → Playlist[]
```

### Song (Пісня/Трек)
```python
- id: int (Primary Key)
- title: str (INDEX)
- artist: str (INDEX)
- duration: int (в мс)
- genre: str
- created_at: DateTime
- Relations:
  - playlists: ManyToMany → Playlist[]
```

### Playlist (Плейліст)
```python
- id: int (Primary Key)
- name: str
- description: str
- owner_id: int (Foreign Key)
- created_at: DateTime
- updated_at: DateTime
- Relations:
  - owner: ManyToOne → User
  - songs: ManyToMany → Song[]
```

### Subscription (Підписка - Base Class)
```python
- id: int (Primary Key)
- type: str (Discriminator: FreeSubscription|PremiumSubscription|StudentSubscription)
- auto_renew: bool
- start_date: DateTime
- end_date: DateTime (nullable)
- Relations:
  - user: OneToOne → User

Subclasses:
├─ FreeSubscription ($0.00)
├─ PremiumSubscription ($9.99/month) - offline download, high quality
└─ StudentSubscription ($4.99/month) - university verification
```

## 🚀 Встановлення та запуск

### Вимоги
- Python 3.8+
- pip
- SQLite3 (включено у Python)

### Крок 1: Встановлення залежностей

```bash
# Встановіть залежності
pip install -r requirements.txt

# Або в віртуальному середовищі (рекомендується)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### Крок 2: Налаштування конфігурації

```bash
# Скопіюйте .env.example в .env
cp .env.example .env

# (Опціонально) Відредагуйте .env файл за потреби
```

### Крок 3: Запуск додатку

```bash
# Запуск FastAPI додатку
python main.py

# Або через uvicorn безпосередньо
uvicorn src.main:app --reload
```

API буде доступно на: **http://localhost:8000**
Swagger документація: **http://localhost:8000/docs**
ReDoc документація: **http://localhost:8000/redoc**

## 📋 Команди CLI

### Ініціалізація БД
```bash
python cli.py init-db
```

### Імпорт CSV даних
```bash
python cli.py import-csv --csv spotify_data.csv
```

### Показ статистики
```bash
python cli.py stats
```

### Очистка БД
```bash
python cli.py clean
```

## 🔌 API Endpoints

### Імпорт
- **POST** `/api/import/csv` - Завантажити та імпортувати CSV файл

### Користувачі
- **GET** `/api/users` - Отримати всіх користувачів
- **GET** `/api/users/{user_id}` - Отримати користувача з плейлистами

### Пісні
- **GET** `/api/songs` - Отримати всі пісні

### Плейлисти
- **GET** `/api/playlists` - Отримати всі плейлисти
- **GET** `/api/playlists/{playlist_id}` - Отримати плейліст з піснями

### Статистика
- **GET** `/api/statistics` - Отримати статистику платформи

### Здоров'я
- **GET** `/api/health` - Перевірка здоров'я API

## 📊 Процес імпорту CSV

1. **Читання CSV файлу** (`spotify_data.csv`)
2. **Парсинг рядків** - розподіл на колони: email, subType, playlistName, songTitle, artist, duration, genre
3. **Перевірка дублікатів**:
   - Пісня: глобально (по title + artist)
   - Користувач: по email
   - Плейліст: в межах користувача
4. **Factory Pattern**: створення правильного типу підписки
5. **SQLAlchemy Relations**: встановлення відносин
6. **Atomic Save**: збереження всіх даних в транзакції

### CSV формат

```csv
email,subType,playlistName,songTitle,artist,duration,genre
user27@example.com,PREMIUM,Playlist_1,Song Title 0,Artist 18,136,Rock
user13@example.com,PREMIUM,Playlist_3,Song Title 1,Artist 11,261,Pop
...
```

## 🏛️ Design Patterns & Принципи

### 1. Dependency Inversion (DIP)
```python
# BLL залежить від інтерфейсу, не від реалізації
class SpotifyService:
    def __init__(self, dal: IDataAccessLayer):
        self.dal = dal  # Залежність ін'єктується

# Це дозволяє легко замінити реалізацію
```

### 2. Factory Pattern
```python
# Створення правильного типу підписки
def _create_subscription(self, subscription_type: str) -> Subscription:
    if subscription_type.upper() == 'PREMIUM':
        return PremiumSubscription(type='PremiumSubscription')
    elif subscription_type.upper() == 'STUDENT':
        return StudentSubscription(type='StudentSubscription')
    else:
        return FreeSubscription(type='FreeSubscription')
```

### 3. Repository Pattern
```python
# DataAccessService інкапсулює всі DB операції
class DataAccessService(IDataAccessLayer):
    async def get_user_by_email(self, email: str) -> Optional[User]:
        # DB operation implementation
```

### 4. Single Responsibility (SRP)
- **SpotifyService** - імпорт CSV, управління даними
- **StatisticsService** - аналітика
- **DataAccessService** - робота з БД
- **Models** - представлення сутностей

### 5. FastAPI Dependency Injection
```python
# FastAPI вбудована DI система
def get_spotify_service(db: Session = Depends(get_db)) -> SpotifyService:
    dal = DataAccessService(db)
    return SpotifyService(dal)

@router.get("/data")
async def get_data(service: SpotifyService = Depends(get_spotify_service)):
    # Сервіс автоматично ін'єктується
```

## 🗂️ База даних

- **Тип**: SQLite3
- **Локація**: `spotify.db` (автоматично створюється)
- **Автоматична синхронізація**: SQLAlchemy автоматично створює таблиці на старт

### Переглід БД

#### VS Code
1. Встановіть розширення: **SQLite Viewer** або **SQLite3 Editor**
2. Клікніть на `spotify.db` файл
3. Переглядайте таблиці та дані

#### Командна лінія (Windows PowerShell для SQLite)
```bash
# Встановіть sqlite3 (якщо не встановлено)
# Або використовуйте Python:
python -c "import sqlite3; conn = sqlite3.connect('spotify.db'); print([row for row in conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')])"
```

## 📝 Порівняння TypeScript vs Python реалізацій

| Аспект | TypeScript/NestJS | Python/FastAPI |
|--------|-------------------|----------------|
| **ORM** | TypeORM | SQLAlchemy |
| **Framework** | NestJS | FastAPI |
| **Dependency Injection** | NestJS DI | FastAPI Depends |
| **Async** | RxJS / async/await | async/await |
| **Validation** | class-validators | Pydantic |
| **Database** | TypeORM (SQL Builder) | SQLAlchemy ORM |
| **API Docs** | Swagger (auto) | Swagger (auto) |

## 🔧 Залежності Python

| Пакет | Версія | Призначення |
|-------|--------|------------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| sqlalchemy | 2.0.23 | ORM |
| pydantic | 2.5.0 | Data validation |
| python-multipart | 0.0.6 | Form data parsing |

## 📚 Примітки та переваги Python реалізації

✅ **Простота**: Python синтаксис зрозумів та лаконічний  
✅ **FastAPI**: Найшвидший Python framework, автоматична документація  
✅ **SQLAlchemy**: Потужний ORM з гнучкістю  
✅ **Type Hints**: Python 3.8+ підтримує type hints як TypeScript  
✅ **Productivity**: Менше boilerplate коду ніж TypeScript  
✅ **Community**: Величезна спільнота, багато бібліотек  

## 🐛 Типові помилки та розв'язання

### Помилка: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Встановіть залежності заново
pip install -r requirements.txt
```

### Помилка: "sqlite3.OperationalError: database is locked"
```bash
# Видаліть spotify.db і переiniziалізуйте
python cli.py clean
```

### Помилка: "Relations not loaded"
SQLAlchemy автоматично завантажує relations з ForeignKey. Якщо виникають проблеми:
```python
# Явно завантажіть relations
user = db.query(User).filter(User.id == 1).first()
_ = user.subscription  # Força載入
_ = user.playlists    # Força載入
```

## 🚀 Розширення

- [ ] REST API endpoints (готово ✓)
- [ ] JWT аутентифікація
- [ ] Статистика слухання пісень
- [ ] Рекомендаційна система
- [ ] Unit тести (pytest)
- [ ] Integration тести
- [ ] Docker контейнеризація
- [ ] GraphQL API
- [ ] WebSocket для real-time оновлень
- [ ] Caching (Redis)
- [ ] Rate limiting
- [ ] Database migrations (Alembic)

## 📖 Додаткова інформація

- Оригінальна документація: [ARCHITECTURE.md](ARCHITECTURE.md)
- Гайд розробки: [CONTRIBUTING.md](CONTRIBUTING.md)
- README TypeScript версії: [README.md](README.md)

---

**Дата:** Март 2026  
**Версія Python:** 3.0.0  
**Версія API:** 2.0.0
