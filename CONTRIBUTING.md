# Contributing & Development Guide

## Налаштування розробки

### Вимоги
- Node.js >= 16.x
- npm або yarn
- SQLite3 (входить в npm package)

### Установка

```bash
# Встановлення залежностей
npm install

# Копіювання .env файлу
cp .env.example .env
```

## Команди розробки

```bash
# Розробка з hot-reload
npm run dev

# Компіляція TypeScript
npm run build

# Запуск скомпільованого коду
npm start

# Генерування тестових CSV даних
npm run generate-csv
```

## Структура проекту

```
src/
├── common/              # Спільні утиліти
│   ├── constants.ts      # Константи
│   └── logger.ts         # Логер
├── pl/                  # Presentation Layer
│   └── interfaces/
├── bll/                 # Business Logic Layer
│   ├── interfaces/
│   └── services/
├── dal/                 # Data Access Layer
│   ├── entities/
│   ├── interfaces/
│   └── repositories/
├── generators/          # Генератори
├── app.module.ts        # Root модуль
└── main.ts             # Entry point
```

## Як додати нову сутність

1. **Створити Entity** в `/src/dal/entities/`:
```typescript
import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class NewEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;
}
```

2. **Добавити методи в DAL Interface** (`/src/dal/interfaces/data-access.interface.ts`)

3. **Реалізувати методи в DataAccessService** (`/src/dal/repositories/data-access.service.ts`)

4. **Зареєструвати в AppModule** (`/src/app.module.ts`):
   - В `TypeOrmModule.forRoot().entities`
   - В `TypeOrmModule.forFeature()`

## Типи помилок та розв'язання

### Помилка: "Cannot find module 'typeorm'"
```bash
npm install --save typeorm
```

### Помилка: "Relations not loaded"
Переконайтесь, що в `findOne()` передаються `relations`:
```typescript
const user = await this.userRepo.findOne({
  where: { id },
  relations: ['playlists', 'playlists.songs'] // ← Додайте цю лінію
});
```

### Помилка: "Duplicate entry"
CSV може мати дублюючі записи. Сервіс автоматично перевіряє дублікати.

### База даних не оновлюється
Переконайтесь:
1. `synchronize: true` в `TypeOrmModule.forRoot()`
2. Видаліть `spotify.db` перед тестуванням
3. Перекомпілюйте: `npm run build`

## Debugging

### Увімкнути SQL логування
В `app.module.ts` змініть:
```typescript
logging: true, // Замість false
```

### Переглянути базу даних
1. Встановіть VS Code розширення "SQLite Viewer"
2. Клікніть на `spotify.db` файл
3. Переглядайте таблиці та дані

## Код стилю

- Використовуйте TypeScript (не JavaScript)
- Додавайте коментарі для складної логіки
- Слідуйте NestJS конвенціям
- Формат: Prettier + ESLint

```bash
# Перевірити код
npm run lint

# Форматувати код
npm run format
```

## Тестування

Поточен не налаштовано, але можна додати:
```bash
npm install --save-dev jest @types/jest
```

## Що далі розвивати?

- [ ] Додати REST API endpoints
- [ ] Реалізувати аутентифікацію (JWT)
- [ ] Додати статистику слухання пісень
- [ ] Реалізувати рекомендацію пісень
- [ ] Додати unit та integration тести
- [ ] Налаштувати Docker контейнеризацію
