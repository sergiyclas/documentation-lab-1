# 👨‍💻 Python Development Guide

## Налаштування розробки

### Вимоги
- Python 3.8+
- pip
- Git

### Встановлення розробницького середовища

```bash
# Клонуйте репозиторій
git clone <repo-url>
cd <repo-directory>

# Створіть віртуальне середовище
python -m venv venv

# Активуйте його
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Встановіть залежності
pip install -r requirements.txt

# (Опціонально) Встановіть dev залежності для тестування
pip install pytest pytest-asyncio black flake8
```

## Структура проекту

```
src/
├── common/              # Спільні утиліти
│   ├── __init__.py
│   ├── constants.ts      # Константи
│   └── logger.py         # Логер
├── pl/                  # Presentation Layer
│   ├── __init__.py
│   ├── routes.py        # FastAPI маршрути
│   └── schemas.py       # Pydantic моделі
├── bll/                 # Business Logic Layer
│   ├── __init__.py
│   └── services.py      # Сервіси (SpotifyService, StatisticsService)
├── dal/                 # Data Access Layer
│   ├── __init__.py
│   ├── database.py      # Налаштування БД
│   ├── models.py        # SQLAlchemy моделі
│   └── repositories.py  # DataAccessService
├── generators/
│   ├── __init__.py
│   └── generate_csv.py  # Генератор CSV
└── main.py             # FastAPI додаток
```

## Розробницькі команди

```bash
# Запуск з hot-reload (nodemon еквівалент)
python main.py
# або
uvicorn src.main:app --reload

# Генерування тестових CSV даних
python -m src.generators.generate_csv

# Ініціалізація БД
python cli.py init-db

# Імпорт CSV
python cli.py import-csv --csv spotify_data.csv

# Показ статистики
python cli.py stats

# Очистка БД
python cli.py clean
```

## Code Style & Форматування

### Налаштування Formatter

```bash
# Встановіть Black
pip install black

# Форматуйте код
black src/
```

### Налаштування Linter

```bash
# Встановіть Flake8
pip install flake8

# Перевірте код
flake8 src/
```

### Python Style Guide

- Використовуйте **snake_case** для змінних та функцій
- Використовуйте **PascalCase** для класів
- Додавайте type hints для все функцій:
  ```python
  def get_user_by_email(self, email: str) -> Optional[User]:
      pass
  ```
- Додавайте docstrings для модулів, класів та функцій:
  ```python
  def create_user(self, email: str, username: str) -> User:
      """Create new user with the given email and username"""
      pass
  ```

## Як додати нову сутність

### 1. Створити SQLAlchemy Model

Файл: `src/dal/models.py`

```python
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.dal.database import Base

class Post(Base):
    """Post entity"""
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post id={self.id} title='{self.title}'>"
```

### 2. Додати Repository Methods

Файл: `src/dal/repositories.py`

```python
class DataAccessService(IDataAccessLayer):
    
    async def create_post(self, title: str, content: str, author_id: int) -> Post:
        """Create new post"""
        post = Post(title=title, content=content, author_id=author_id)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        logger.info(f"Post created: {title}")
        return post
    
    async def get_post_by_id(self, post_id: int) -> Optional[Post]:
        """Get post by ID"""
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    async def get_all_posts(self) -> List[Post]:
        """Get all posts"""
        return self.db.query(Post).all()
```

### 3. Додати Pydantic Schema

Файл: `src/pl/schemas.py`

```python
class PostCreate(BaseModel):
    title: str
    content: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    author_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### 4. Додати Routes

Файл: `src/pl/routes.py`

```python
@router.post("/posts")
async def create_post(
    post_data: PostCreate,
    service: SpotifyService = Depends(get_spotify_service)
):
    """Create new post"""
    try:
        post = await service.create_post(
            post_data.title,
            post_data.content,
            post_data.author_id
        )
        return {"status": "success", "data": post}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/posts/{post_id}")
async def get_post(
    post_id: int,
    service: SpotifyService = Depends(get_spotify_service)
):
    """Get post by ID"""
    post = await service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"status": "success", "data": post}
```

### 5. Оновити Залежності в requirements.txt

(Якщо потрібні нові пакети)

```bash
pip freeze > requirements.txt
```

## Типові помилки та розв'язання

### Помилка: "Relations not loaded"

Переконайтесь, що робите explicit load:

```python
# ❌ Неправильно
user = db.query(User).filter(User.id == 1).first()
print(user.playlists)  # Може бути пусто

# ✅ Правильно
user = db.query(User).filter(User.id == 1).first()
_ = user.playlists  # Explicilty load
print(user.playlists)
```

### Помилка: "Duplicate key value"

CSV може мати дублюючі записи. Репозиторій автоматично проводить перевірку:

```python
# Автоматично перевіряє дублікати
async def create_user(...):
    existing_user = await self.get_user_by_email(email)
    if existing_user:
        return existing_user  # Повертає існуючого
```

### Помилка: "Database is locked"

Видаліть БД файл:

```bash
python cli.py clean
```

### Помилка: "Async not working"

Переконайтесь, використовуєте `async/await` правильно:

```python
# ❌ Неправильно
def get_data():
    result = service.get_users()  # Забув await

# ✅ Правильно
async def get_data():
    result = await service.get_users()
```

## Debugging

### Увімкнути SQL Logging

**config.py:**
```python
DATABASE_ECHO = True
```

Потім усі SQL запити будуть видимі в логах.

### Використання Python Debugger

```python
import pdb

def some_function():
    pdb.set_trace()  # Точка зупинки
    # Код виконується до цієї точки
```

### Логування

```python
from src.common.logger import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Тестування

### Налаштування pytest

```bash
pip install pytest pytest-asyncio
```

### Приклад тесту

Файл: `tests/test_services.py`

```python
import pytest
from src.bll import SpotifyService
from src.dal import DataAccessService

@pytest.mark.asyncio
async def test_import_csv():
    """Test CSV import"""
    dal = DataAccessService(db)
    service = SpotifyService(dal)
    
    stats = await service.import_csv("spotify_data.csv")
    
    assert stats['total_rows'] > 0
    assert stats['songs_created'] > 0
```

## Code Review Checklist

Перед push до git:

- [ ] Код відформатований (`black src/`)
- [ ] Немає помилок linter'а (`flake8 src/`)
- [ ] Всі функції мають type hints
- [ ] Всі публічні функції мають docstrings
- [ ] БД міграції проведені (якщо потрібні)
- [ ] Нові залежності додані у requirements.txt
- [ ] Тести проходять (якщо налаштовані)

## Deployment Considerations

### Production Checklist

- [ ] `DATABASE_ECHO = False` в config.py
- [ ] `LOG_LEVEL = "INFO"` або `"WARNING"`
- [ ] Використовуйте production ASGI сервер (Gunicorn)
- [ ] Налаштуйте CORS для production домену
- [ ] Включіть аутентифікацію (JWT)
- [ ] Налаштуйте rate limiting
- [ ] Додайте database pooling

### Запуск з Gunicorn

```bash
pip install gunicorn

# Запуск
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## Корисні ресурси

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM Guide](https://docs.sqlalchemy.org/en/20/orm/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Python AsyncIO](https://docs.python.org/3/library/asyncio.html)

---

**Happy Coding! 🎉**
