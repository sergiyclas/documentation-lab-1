# 🎵 Spotify Platform - Web Interface (MVC Implementation)

## Лабораторна 3: Реалізація Web-додатку на основі шаблону MVC

Цей документ описує реалізацію Web-інтерфейсу для Spotify Platform з дотриманням MVC архітектури.

## 📋 Що було реалізовано

### 1. **Model та Business Logic Layer**
- ✅ SQLAlchemy ORM моделі (User, Song, Playlist, Subscription)
- ✅ Business Logic Services (SpotifyService, StatisticsService)
- ✅ Repository Pattern для DAL (Data Access Layer)
- ✅ CRUD операції для Song та Playlist

### 2. **View Layer (HTML Шаблони)**
Створено 8 HTML шаблонів використовуючи Jinja2:

#### **Основні сторінки:**
- `base.html` - базовий шаблон з навігацією та footer
- `index.html` - домашня сторінка зі статистикою
- `statistics.html` - сторінка зі статистикою платформи

#### **Пісні (Songs):**
- `songs.html` - список всіх пісень з CRUD кнопками
- `song_form.html` - форма для додавання/редагування пісні

#### **Плейлисти (Playlists):**
- `playlists.html` - список плейлистів у формі карток
- `playlist_detail.html` - деталі плейлісту з піснями
- `playlist_form.html` - форма для створення/редагування плейлісту

### 3. **Controller (FastAPI Routes)**

#### **HTML Endpoints (View Layer):**
```
GET  /                           - Домашня сторінка
GET  /songs                      - Список пісень
GET  /songs/create               - Форма створення пісні
POST /songs/create               - Обробка створення пісні
GET  /songs/{id}/edit            - Форма редагування пісні
POST /songs/{id}/edit            - Обробка редагування пісні
POST /songs/{id}/delete          - Видалення пісні
GET  /playlists                  - Список плейлистів
GET  /playlists/create           - Форма створення плейлісту
POST /playlists/create           - Обробка створення плейлісту
GET  /playlists/{id}             - Деталі плейлісту
GET  /playlists/{id}/edit        - Форма редагування плейлісту
POST /playlists/{id}/edit        - Обробка редагування плейлісту
POST /playlists/{id}/delete      - Видалення плейлісту
POST /playlists/{id}/add-song    - Додавання пісні до плейлісту
POST /playlists/{id}/songs/{sid}/remove - Видалення пісні з плейлісту
GET  /statistics                 - Статистика платформи
```

#### **API Endpoints (JSON):**
```
POST /api/import/csv             - Імпорт даних з CSV
GET  /api/users                  - Отримати всіх користувачів
GET  /api/users/{id}             - Отримати користувача з плейлистами
GET  /api/songs                  - Отримати всі пісні
GET  /api/playlists              - Отримати всі плейлисти
GET  /api/playlists/{id}         - Отримати плейліст з піснями
GET  /api/statistics             - Отримати статистику
GET  /api/health                 - Health check
```

### 4. **Стилізація (CSS)**
- `static/style.css` - комплексні CSS стилі з:
  - Responsive дизайном (мобільні, планшети, десктоп)
  - Градієнтними кнопками і картками
  - Таблицями з гарним форматуванням
  - Формами з валідацією
  - Анімаціями та переходами

## 🏗️ Архітектура MVC

```
┌─────────────────────────────────────────────┐
│         VIEW LAYER (Presentation)           │
│  HTML Template + CSS + Forms                │
│  - base.html, songs.html, playlist*.html    │
│  - style.css (responsive design)            │
└─────────────────┬───────────────────────────┘
                  │ (Користувач взаємодіє)
┌─────────────────▼───────────────────────────┐
│      CONTROLLER (FastAPI Routes)            │
│  - HTML endpoints (/songs, /playlists)      │
│  - API endpoints (/api/songs, /api/users)   │
│  - Form processing (POST/PUT/DELETE)        │
└─────────────────┬───────────────────────────┘
                  │ (Бізнес-логіка)
┌─────────────────▼───────────────────────────┐
│     MODEL LAYER (Business Logic)            │
│  - SpotifyService (управління даними)       │
│  - StatisticsService (аналітика)            │
│  - DataAccessService (репозиторії)          │
└─────────────────┬───────────────────────────┘
                  │ (БД операції)
┌─────────────────▼───────────────────────────┐
│        DATA ACCESS LAYER (DAL)              │
│  - SQLAlchemy ORM моделі                    │
│  - Repository Pattern                       │
│  - CRUD операції                            │
│  - SQLite база даних                        │
└─────────────────────────────────────────────┘
```

## 🚀 CRUD Операції

### Songs (Пісні)
```
CREATE: POST /songs/create          (Форма: song_form.html)
READ:   GET  /songs                 (Список: songs.html)
UPDATE: POST /songs/{id}/edit       (Форма: song_form.html)
DELETE: POST /songs/{id}/delete     (Кнопка с підтвердженням)
```

### Playlists (Плейлисти)
```
CREATE: POST /playlists/create      (Форма: playlist_form.html)
READ:   GET  /playlists             (Карти: playlists.html)
        GET  /playlists/{id}        (Деталі: playlist_detail.html)
UPDATE: POST /playlists/{id}/edit   (Форма: playlist_form.html)
DELETE: POST /playlists/{id}/delete (Кнопка с підтвердженням)
ADD:    POST /playlists/{id}/add-song (Dropdown в деталях)
REMOVE: POST /playlists/{id}/songs/{sid}/remove
```

## 🎨 Функціональні Можливості

### ✨ Користувацьський Інтерфейс
- **Навігація** - меню з посиланнями на основні сторінки
- **Формування** - інтуїтивні форми з валідацією
- **Таблиці** - сортування та перегляд даних у таблицях
- **Карти** - красивий перегляд плейлистів у форматі карток
- **Статистика** - графічне представлення даних з прогрес-барами

### 🔄 Взаємодія Даних
- Додавання пісень до плейлистів
- Видалення пісень з плейлистів
- Редагування імені та опису плейлістів
- Видалення всіх даних через простий інтерфейс

### 📊 Демонстрація Бізнес-Логіки
- Отримання даних з БД через BLL сервіси
- Управління відносинами (relationships) між сутностями
- Трансформація даних із моделей у представлення

## 📁 Структура Файлів

```
project/
├── templates/                      # HTML шаблони
│   ├── base.html                   # Базовий шаблон
│   ├── index.html                  # Домашня сторінка
│   ├── songs.html                  # Список пісень
│   ├── song_form.html              # Форма пісні
│   ├── playlists.html              # Список плейлистів
│   ├── playlist_detail.html        # Деталі плейлісту
│   ├── playlist_form.html          # Форма плейлісту
│   └── statistics.html             # Статистика
│
├── static/
│   └── style.css                   # CSS стилі
│
├── src/
│   ├── pl/
│   │   ├── routes.py               # FastAPI маршрути (HTML + API)
│   │   └── schemas.py              # Pydantic схеми
│   ├── bll/
│   │   └── services.py             # Business Logic Services
│   ├── dal/
│   │   ├── models.py               # SQLAlchemy моделі
│   │   ├── repositories.py         # CRUD операції
│   │   └── database.py             # DB конфіг
│   └── common/
│       ├── logger.py               # Логування
│       └── constants.py            # Константи
│
├── main.py                         # Entry point + FastAPI app
└── pyproject.toml                  # Зависимости
```

## 🔧 Технічний Стек

| Компонент | Технологія |
|-----------|-----------|
| **Web Framework** | FastAPI |
| **Template Engine** | Jinja2 |
| **ORM** | SQLAlchemy 2.0 |
| **Database** | SQLite3 |
| **Styling** | CSS3 (Responsive) |
| **Forms** | HTML5 + Method Override |
| **Async** | Python asyncio |
| **Server** | Uvicorn |

## 🎯 Принципи та Паттерни

### ✅ SOLID Принципи
- **SRP** - Кожна папка має одну відповідальність (PL, BLL, DAL)
- **OCP** - Розширення через новi сервіси без зміни існуючих
- **LSP** - DAL інтерфейс дотримується контракту
- **ISP** - Мінімальні залежності між шарами
- **DIP** - Залежність на абстракціях (сервісах), не реалізаціях

### 🏗️ Design Patterns
- **MVC** - Model-View-Controller архітектура
- **Repository** - DAL інкапсуляція
- **Factory** - Создание підписок
- **Dependency Injection** - FastAPI Depends
- **Template Method** - Базовий HTML шаблон

## 🚀 Запуск

### 1. Встановлення залежностей
```bash
pip install -e .  # Встановить проект з pyproject.toml
```

### 2. Ініціалізація БД та імпорт даних
```bash
python cli.py init-db
python cli.py import-csv --csv spotify_data.csv
```

### 3. Запуск сервера
```bash
# Option 1: Direct via Python
python main.py

# Option 2: Via uvicorn
uvicorn src.main:app --reload --port 8000
```

### 4. Доступ до web-додатку
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger)
- **API ReDoc**: http://localhost:8000/redoc

## ✨ Особливості Реалізації

### 🎨 Frontend
- **Responsive Design** - працює на всіх розмірах екранів
- **Form Validation** - валідація на HTML рівні
- **User Feedback** - повідомлення про дії
- **Easy Navigation** - інтуїтивна навігація

### 🔌 Backend
- **Async/Await** - асинхронна обробка запитів
- **Error Handling** - правильне обробка помилок
- **Logging** - детальне логування всіх операцій
- **DB Transactions** - атомарні операції в БД

### 📊 Business Logic
- **BLL Services** - вся бізнес-логіка в сервісах
- **DAL Abstraction** - НЕ залежність від БД реалізації
- **Type Hints** - повна типізація коду
- **Validation** - валідація на рівні сервісів

## 📈 Можливі Розширення

- [ ] JWT аутентифікація користувачів
- [ ] Пошук та фільтрацію даних
- [ ] Пагінацію списків
- [ ] WebSocket для real-time оновлень
- [ ] Caching (Redis)
- [ ] Rate limiting
- [ ] Database migrations (Alembic)
- [ ] Unit тести (pytest)
- [ ] Docker контейнеризація
- [ ] GraphQL API

## 📝 Висновок

Проект успішно реалізує MVC архітектуру з:
- ✅ Model Layer - SQLAlchemy + Repository Pattern
- ✅ View Layer - Jinja2 HTML шаблони + CSS
- ✅ Controller Layer - FastAPI маршрути
- ✅ Business Logic Layer - Сервіси для управління даними
- ✅ CRUD операції - Повна функціональність управління сутностями

Додаток демонструє правильну розділення відповідальності та дотримання SOLID принципів у веб-розробці.

---

**Версія**: 1.0.0  
**Last Updated**: 2026-03-26  
**Framework**: FastAPI + SQLAlchemy + Jinja2
