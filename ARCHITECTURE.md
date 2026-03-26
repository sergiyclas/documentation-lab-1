# Архітектура Проекту

## Трирівнева архітектура (3-Tier Architecture)

### 1. **PL (Presentation Layer)** - Рівень представлення
📁 `/src/pl/interfaces/`

- Визначає контракти для взаємодії з користувачем
- Інтерфейси для UI компонентів
- Зараз: Базові інтерфейси для меню та статусу

### 2. **BLL (Business Logic Layer)** - Рівень бізнес-логіки
📁 `/src/bll/`

#### Сервіси (`/services/`)
- **SpotifyService** - основний сервіс для імпорту та управління даними
  - Читання CSV файлів
  - Створення/оновлення сутностей
  - Управління плейлистами та піснями

#### Інтерфейси (`/interfaces/`)
- **ISpotifyView** - контракт для представлення
- **IStatisticsView** - контракт для статистики

### 3. **DAL (Data Access Layer)** - Рівень доступу до даних
📁 `/src/dal/`

#### Сутності (`/entities/`)
Моделі даних з TypeORM:
- **User** - Користувач платформи
- **Song** - Пісня в базі
- **Playlist** - Плейліст користувача
- **Subscription** - Базовий клас для підписок
  - FreeSubscription
  - PremiumSubscription
  - StudentSubscription (наслідування)

#### Репозиторії (`/repositories/`)
- **DataAccessService** - реалізація IDataAccessLayer
  - CRUD операції для всіх сутностей
  - Запити та фільтрація

#### Інтерфейси (`/interfaces/`)
- **IDataAccessLayer** - контракт для репозиторіїв (Dependency Inversion)

## Основні концепції

### Dependency Inversion Principle (DIP)
```
BLL → IDataAccessLayer (interface)
               ↓
          DataAccessService (implementation)
```
Це дозволяє легко змінювати реалізацію без змін в BLL.

### Factory Pattern
Використовується при створенні підписок:
```typescript
switch(subType.toUpperCase()) {
  case 'PREMIUM': user.subscription = new PremiumSubscription();
  case 'STUDENT': user.subscription = new StudentSubscription();
  default: user.subscription = new FreeSubscription();
}
```

### ORM Relations
- **OneToOne**: User ↔ Subscription
- **OneToMany**: User → Playlist[]
- **ManyToMany**: Playlist ↔ Song[]

## Database Schema

```
┌──────────────────────────────────────┐
│           User                       │
├──────────────────────────────────────┤
│ id (PK)                              │
│ email (UNIQUE)                       │
│ username                             │
│ registrationDate                     │
│ subscriptionId (FK)                  │
└──────────────────────────────────────┘
         ↓ 1:1         ↑ 1:∞
    ┌─────────────┐   ┌──────────────┐
    │Subscription │   │  Playlist    │
    │  (abstract) │   ├──────────────┤
    ├─────────────┤   │ id (PK)      │
    │ id (PK)     │   │ name         │
    │ type        │   │ ownerId (FK) │
    │ startDate   │   └──────────────┘
    │ endDate     │          ↑ ∞:∞
    └─────────────┘          │
         ↑                    │
    ┌────┴────────────┐       │
    │    │            │       │
    │ Free Premium Student    │
    │                    ┌────┴──────────┐
    │                    │  Playlist_Song│
    │                    │  (JoinTable)  │
    │                    └────┬──────────┘
    │                         │
    │                    ┌────▼──────────┐
    │                    │   Song         │
    │                    ├────────────────┤
    │                    │ id (PK)        │
    │                    │ title          │
    │                    │ artist         │
    │                    │ duration       │
    │                    │ genre          │
    │                    └────────────────┘
```

## Процес імпорту даних

1. **Читання CSV** - пошук рядків файлу
2. **Парсинг** - розділення на колони
3. **Перевірка дублікатів**:
   - Пісня: глобально (по title + artist)
   - Користувач: по email
   - Плейліст: у користувача (по name)
4. **Створення сутностей** - Factory pattern для підписок
5. **Встановлення зв'язків** - ORM відносини
6. **Каскадне збереження** - TypeORM синхронізує все

## Технологічний стек

- **Runtime**: Node.js + TypeScript
- **Framework**: NestJS
- **ORM**: TypeORM 0.3.16
- **Database**: SQLite3
- **Build**: tsc (TypeScript Compiler)
