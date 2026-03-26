# 🎵 Spotify Documentation Lab

**Варіант: 12** | **Техстек:** TypeScript, NestJS, TypeORM, SQLite3, Dependency Injection

## 📋 Опис проекту

Це документаційна лабораторна робота, присвячена моделюванню системи управління музичною платформою **Spotify**. Проект реалізує **трирівневу архітектуру** (Presentation Layer, Business Logic Layer, Data Access Layer) і демонструє:

- ✅ Принципи SOLID (DIP, SRP)
- ✅ Design Patterns (Factory, Repository, Dependency Injection)
- ✅ ORM moделювання (TypeORM)
- ✅ CSV імпорт з обробкою дублікатів
- ✅ Логування та обробка помилок

## 🎯 Завдання

1. ✅ Use-case діаграма реєстрації користувача та створення плейліста
2. ✅ Діаграма класів для об'єктів плейліста, програвання та статистики
3. ✅ Діаграма активності зняття оплати залежно від типу підписки
4. ✅ Sequence діаграма читання плейліста та запису статистики

## 🏗️ Архітектура проекту

Проект дотримується **трирівневої архітектури**:

```
┌─────────────────────────────────────────────────────┐
│          Presentation Layer (PL)                    │
│         Інтерфейси для користувача                 │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│      Business Logic Layer (BLL)                     │
│  SpotifyService, StatisticsService                 │
│  (Processor CSV, управління даними)               │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│      Data Access Layer (DAL)                        │
│  Repository Pattern + TypeORM                      │
│  (User, Song, Playlist, Subscription)             │
└─────────────────────────────────────────────────────┘
```

### Файлова структура

```
src/
├── common/                      # Спільні утиліти
│   ├── constants.ts             # Конфігураційні константи
│   └── logger.ts                # Logger сервіс
│
├── pl/                          # Presentation Layer
│   └── interfaces/
│       └── (Інтерфейси для UI)
│
├── bll/                         # Business Logic Layer
│   ├── interfaces/
│   │   └── view.interface.ts    # Контракти для представлення
│   └── services/
│       └── spotify.service.ts   # Основний сервіс імпорту даних
│
├── dal/                         # Data Access Layer
│   ├── entities/                # ORM сутності
│   │   ├── user.entity.ts
│   │   ├── song.entity.ts
│   │   ├── playlist.entity.ts
│   │   └── subscription.entity.ts
│   ├── interfaces/
│   │   └── data-access.interface.ts (Dependency Inversion)
│   └── repositories/
│       └── data-access.service.ts   (Repository Pattern)
│
├── generators/
│   └── generate-csv.ts          # Генератор тестових даних
├── app.module.ts                # Модуль додатку
└── main.ts                      # Entry point
```

## 📚 Сутності базі даних

### User (Користувач)
```typescript
- id: number (PK)
- email: string (UNIQUE)
- username: string
- subscription: Subscription (OneToOne)
- playlists: Playlist[] (OneToMany)
- registrationDate: Date
- isActive: boolean
```

### Song (Пісня/Трек)
```typescript
- id: number (PK)
- title: string
- artist: string
- duration: number (ms)
- genre: string
- createdAt: Date
```

### Playlist (Плейліст)
```typescript
- id: number (PK)
- name: string
- description: string
- owner: User (ManyToOne)
- songs: Song[] (ManyToMany)
- createdAt: Date
- updatedAt: Date
```

### Subscription (Підписка - Abstract Class)
```typescript
- id: number (PK)
- type: string (FreeSubscription|PremiumSubscription|StudentSubscription)
- autoRenew: boolean
- startDate: Date
- endDate: Date | null
- user: User (OneToOne)

Типи:
├─ FreeSubscription (0.00$)
├─ PremiumSubscription (9.99$/міс) + offline download + high quality
└─ StudentSubscription (4.99$/міс) + university verification
```

## 🚀 Установка та запуск

### Вимоги
- Node.js >= 16.x
- npm або yarn

### Установка залежностей
```bash
npm install
```

### Копіювання конфігурації
```bash
cp .env.example .env
```

### Команди

| Команда | Опис |
|---------|------|
| `npm run dev` | Розробка з hot-reload (nodemon) |
| `npm run build` | Компіляція TypeScript в JavaScript |
| `npm start` | Запуск скомпільованого коду в production |
| `npm run generate-csv` | Генерування тестових даних (1000 рядків) |

## 📊 Імпорт даних

### Процес імпорту

1. **Читання CSV файлу** (`spotify_data.csv`)
2. **Парсинг рядків** - розподіл на колони: email, subType, playlistName, songTitle, artist, duration, genre
3. **Перевірка дублікатів**:
   - Пісня: глобально (по title + artist)
   - Користувач: по email
   - Плейліст: в межах користувача
4. **Factory Pattern**: створення правильного типу підписки
5. **ORM Relations**: встановлення відносин між сутностями
6. **Каскадне збереження**: TypeORM синхронізує всі зв'язки

### Приклад процесу

```
CSV Рядок: user1@example.com,PREMIUM,Workout,Song1,Artist1,180,Rock

1. Пошук/Створення Song: "Song1" by "Artist1" (180ms, Genre: Rock)
2. Пошук/Створення User: user1@example.com → Assign PremiumSubscription
3. Пошук/Створення Playlist: "Workout" пла user1
4. Додавання Song→Playlist, User→Subscription
5. Каскадне збереження всіх даних в БД
```

## 🗂️ База даних

- **Тип**: SQLite3
- **Локація**: `spotify.db`
- **Автоматична синхронізація**: TypeORM автоматично створює таблиці
- **Кількість сутностей**: User, Song, Playlist, Subscription (+ 3 підкласи)

### Переглік БД у VS Code

1. Встановіть розширення: **SQLite Viewer** (`RandomFractalsInc.vscode-sqlite3-editor`)
2. Клікніть на `spotify.db` файл
3. Переглядайте таблиці та дані

Альтернатива - CLI:
```bash
sqlite3 spotify.db ".tables"
sqlite3 spotify.db "SELECT COUNT(*) FROM user;"
```

## 🏛️ Design Patterns & Принципи

### 1. Dependency Inversion Principle (DIP)
```typescript
// BLL залежить від інтерфейсу, а не від реалізації
constructor(@Inject(DATA_ACCESS_LAYER) private readonly dal: IDataAccessLayer)

// Це дозволяє легко замінити реалізацію
// DIP → Loose coupling → Easier testing & maintenance
```

### 2. Factory Pattern
```typescript
// Створення правильного типу підписки
switch(subType.toUpperCase()) {
  case 'PREMIUM': 
    user.subscription = new PremiumSubscription();
    break;
  // ...
}
```

### 3. Repository Pattern
```typescript
// DataAccessService інкапсулює всі DB операції
// BLL використовує інтерфейс, не знаючи про внутрішню реалізацію
interface IDataAccessLayer {
  findUserByEmail(email: string): Promise<User | null>;
  saveUser(user: User): Promise<User>;
  // ...
}
```

### 4. Single Responsibility Principle (SRP)
- **SpotifyService** - імпорт CSV
- **DataAccessService** - робота з БД
- **User/Song/Playlist/Subscription** - модельовані сутності

## 📝 Примітки та переваги архітектури

✅ **Модульність**: Легко додавати нові層 та сервіси
✅ **Тестованість**: Залежності ін'єктуються, можна мокувати
✅ **Maintainability**: Чіткий поділ відповідальності
✅ **Масштабованість**: ORM дозволяє легко змінювати БД
✅ **Type Safety**: Full TypeScript з строгими типами
✅ **Logging**: Вбудований логер для debug

## 🔧 Залежності

| Пакет | Версія | Завдання |
|-------|--------|----------|
| @nestjs/common | ^10.0.0 | NestJS декоратори |
| @nestjs/core | ^10.0.0 | NestJS фреймворк |
| @nestjs/typeorm | ^10.0.0 | Інтеграція TypeORM |
| typeorm | ^0.3.16 | ORM для роботи з БД |
| sqlite3 | ^5.1.6 | SQLite драйвер |
| reflect-metadata | ^0.1.13 | Метаданни для декораторів |

## 📋 DevDependencies

| Пакет | Версія |
|-------|--------|
| typescript | ^5.0.0 |
| @types/node | ^20.0.0 |
| nodemon | ^3.0.0 |
| ts-node | ^10.9.0 |
| @typescript-eslint/eslint-plugin | Latest |
| eslint | Latest |
| prettier | Latest |

## 📚 Додаткова документація

- [ARCHITECTURE.md](ARCHITECTURE.md) - Детальна архітектура та схеми
- [CONTRIBUTING.md](CONTRIBUTING.md) - Гайд розробки та розширення

## ✨ Майбутні розширення

- [ ] REST API endpoints (Express/NestJS)
- [ ] JWT аутентифікація
- [ ] Статистика слухання пісень
- [ ] Рекомендаційна система
- [ ] Unit & Integration тести (Jest)
- [ ] Docker контейнеризація
- [ ] GraphQL API

---

**Автор:** Лабораторна робота № 1  
**Дата:** Март 2026  
**Версія:** 2.0.0
