# 🚀 Spotify Python Implementation - Quick Start Guide

## Встановлення за 3 кроки

### 1️⃣ Встановіть залежності

```bash
# Windows
run.bat install

# Linux/Mac
./run.sh install
```

**або вручну з uv:**
```bash
uv sync
```

### 2️⃣ Ініціалізуйте базу даних

```bash
# Windows
run.bat init

# Linux/Mac
./run.sh init
```

### 3️⃣ Запустіть сервер

```bash
# Windows
run.bat dev

# Linux/Mac  
./run.sh dev
```

**API доступна на:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs

---

## 📋 Типові сценарії використання

### Сценарій 1: Імпорт CSV даних

```bash
# Windows
run.bat import spotify_data.csv

# Linux/Mac
./run.sh import spotify_data.csv

# Або з явною вказівкою:
python cli.py import-csv --csv spotify_data.csv
```

**Результат:** Користувачі, пісні та плейлисти імпортовані в БД

### Сценарій 2: Перегляд статистики

```bash
# Windows
run.bat stats

# Linux/Mac
./run.sh stats
```

**Результат:**
```
==================================================
Database Statistics
==================================================
Total Users: 50
Total Songs: 139
Total Playlists: 100+

Subscription Breakdown:
  FreeSubscription: 20
  PremiumSubscription: 18
  StudentSubscription: 12
==================================================
```

### Сценарій 3: Отримання даних через API

#### GET усі користувачів
```bash
curl http://localhost:8000/api/users
```

**Результат:**
```json
{
  "status": "success",
  "count": 50,
  "data": [
    {
      "id": 1,
      "email": "user0@example.com",
      "username": "user0",
      "subscription_type": "FreeSubscription",
      "registration_date": "2026-03-26T..."
    }
  ]
}
```

#### GET деталі користувача з плейлистами
```bash
curl http://localhost:8000/api/users/1
```

**Результат:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user0@example.com",
    "username": "user0",
    "subscription_type": "FreeSubscription",
    "playlists": [
      {
        "id": 5,
        "name": "Playlist_0",
        "song_count": 3,
        "created_at": "2026-03-26T..."
      }
    ]
  }
}
```

#### GET деталі плейліста з піснями
```bash
curl http://localhost:8000/api/playlists/1
```

**Результат:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Playlist_0",
    "owner_id": 5,
    "song_count": 3,
    "songs": [
      {
        "id": 1,
        "title": "Song Title 0",
        "artist": "Artist 18",
        "duration": 136,
        "genre": "Rock"
      }
    ]
  }
}
```

#### GET статистика платформи
```bash
curl http://localhost:8000/api/statistics
```

**Результат:**
```json
{
  "status": "success",
  "data": {
    "total_users": 50,
    "total_songs": 139,
    "total_playlists": 100,
    "total_playlist_songs": 342,
    "subscriptions": {
      "FreeSubscription": 20,
      "PremiumSubscription": 18,
      "StudentSubscription": 12
    },
    "average_playlist_size": 3.42
  }
}
```

---

## 🧪 Testing API з Swagger UI

1. Перейдіть на **http://localhost:8000/docs**
2. Натисніть на потрібний endpoint
3. Натисніть **"Try it out"**
4. Натисніть **"Execute"**

---

## 🗑️ Очистка і переініціалізація

```bash
# Видаліть БД і створіть нову
python cli.py clean

# Або вручну
rm spotify.db  # Linux/Mac
del spotify.db # Windows PowerShell
```

---

## 📊 Структура проекту

```
.
├── src/
│   ├── common/           # Утиліти (логер, константи)
│   ├── pl/              # Presentation Layer - API маршрути
│   ├── bll/             # Business Logic Layer - сервіси
│   ├── dal/             # Data Access Layer - моделі і репозиторії
│   ├── generators/      # CSV генератори
│   └── main.py          # FastAPI додаток
├── main.py              # Entry point
├── cli.py               # CLI утиліти
├── config.py            # Конфігурація
├── requirements.txt     # Залежності
├── run.bat             # Батник для Windows
├── run.sh              # Шелл-скрипт для Linux/Mac
└── spotify_data.csv    # Тестові дані
```

---

## 🔧 Як розширити проект

### Додавання нового API endpoint

1. Відкрийте `src/pl/routes.py`
2. Додайте новий маршрут:

```python
@router.post("/api/users")
async def create_user(
    email: str,
    username: str,
    sub_type: str = "FREE",
    service: SpotifyService = Depends(get_spotify_service)
):
    """Create new user"""
    try:
        db = SessionLocal()
        dal = DataAccessService(db)
        user = await dal.create_user(email, username, sub_type)
        db.close()
        return {"status": "success", "data": {"id": user.id, "email": user.email}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

3. Перезапустіть сервер
4. Новий endpoint буде доступний на http://localhost:8000/api/users

### Додавання новой сутності

1. Додайте модель в `src/dal/models.py`
2. Додайте методи в `src/dal/repositories.py`
3. Додайте сервіс методи в `src/bll/services.py`
4. Додайте маршрути в `src/pl/routes.py`

---

## 📝 Режим Debug

Для детальних логів включіть SQL logging:

**config.py:**
```python
DATABASE_ECHO = True  # Замість False
LOG_LEVEL = "DEBUG"   # Замість "INFO"
```

Потім переконайтесь БД синхронізується:
```bash
python cli.py clean
python cli.py init-db
```

---

## ✅ Перевірка списку

- [ ] Python встановлено (3.8+)
- [ ] Залежності встановлені (`pip install -r requirements.txt`)
- [ ] БД ініціалізована (`python cli.py init-db`)
- [ ] Сервер працює (`python main.py`)
- [ ] API доступна на http://localhost:8000
- [ ] CSV імпортовані (`python cli.py import-csv --csv spotify_data.csv`)
- [ ] Статистика показується (`python cli.py stats`)

---

## 🆘 Troubleshooting

**Q: "ModuleNotFoundError: No module named 'fastapi'"**  
A: Встановіть залежності: `pip install -r requirements.txt`

**Q: "sqlite3.OperationalError: database is locked"**  
A: Запустіть: `python cli.py clean`

**Q: API не доступна**  
A: Переконайтесь сервер працює і запущен на port 8000

**Q: Дані не імпортуються**  
A: Перевірте шлях до CSV файла і його формат

---

**Більше інформації:** [README_PYTHON.md](README_PYTHON.md)
