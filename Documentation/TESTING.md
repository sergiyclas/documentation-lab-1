# 🧪 Testing Guide for Python Implementation

## Automated Testing

### Setup

```bash
pip install pytest pytest-asyncio

pytest
```

## Manual Testing

### 1. CSV Import Testing

```bash
# Initialize database
python cli.py init-db

# Import data
python cli.py import-csv --csv spotify_data.csv

# Check statistics
python cli.py stats
```

**Expected Output:**
```
==================================================
Database Statistics
==================================================
Total Users: 50
Total Songs: 139
Total Playlists: 100+

Subscription Breakdown:
  FreeSubscription: 20+
  PremiumSubscription: 18+
  StudentSubscription: 12+
==================================================
```

### 2. Testing API with Curl

#### Health Check
```bash
curl -X GET "http://localhost:8000/api/health"
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### Get All Users
```bash
curl -X GET "http://localhost:8000/api/users"
```

**Response:**
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
      "registration_date": "2026-03-26T10:30:00"
    }
  ]
}
```

#### Get User by ID
```bash
curl -X GET "http://localhost:8000/api/users/1"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user0@example.com",
    "username": "user0",
    "subscription_type": "FreeSubscription",
    "registration_date": "2026-03-26T10:30:00",
    "playlists": [
      {
        "id": 1,
        "name": "Playlist_0",
        "song_count": 3,
        "created_at": "2026-03-26T10:30:00"
      }
    ]
  }
}
```

#### Get All Songs
```bash
curl -X GET "http://localhost:8000/api/songs"
```

**Response:**
```json
{
  "status": "success",
  "count": 139,
  "data": [
    {
      "id": 1,
      "title": "Song Title 0",
      "artist": "Artist 18",
      "duration": 136,
      "genre": "Rock",
      "created_at": "2026-03-26T10:30:00"
    }
  ]
}
```

#### Get All Playlists
```bash
curl -X GET "http://localhost:8000/api/playlists"
```

#### Get Playlist by ID
```bash
curl -X GET "http://localhost:8000/api/playlists/1"
```

**Response:**
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
    ],
    "created_at": "2026-03-26T10:30:00",
    "updated_at": "2026-03-26T10:30:00"
  }
}
```

#### Get Statistics
```bash
curl -X GET "http://localhost:8000/api/statistics"
```

**Response:**
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

### 3. Testing CSV Import via API

```bash
# Prepare CSV file
# Then upload it

curl -X POST "http://localhost:8000/api/import/csv" \
  -H "accept: application/json" \
  -F "file=@spotify_data.csv"
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully imported 139 rows",
  "statistics": {
    "users_created": 45,
    "users_existing": 5,
    "songs_created": 139,
    "playlists_created": 100,
    "associations_added": 342,
    "total_rows": 139
  }
}
```

### 4. Testing via Swagger UI

1. Start the API:
```bash
python main.py
```

2. Open in browser: http://localhost:8000/docs

3. Click on endpoint
4. Click "Try it out"
5. Click "Execute"

## Integration Tests

### Test 1: Full workflow cycle

```bash
# 1. Clean database
python cli.py clean

# 2. Start API in separate terminal
python main.py

# 3. In another terminal, import CSV via CLI
python cli.py import-csv --csv spotify_data.csv

# 4. Check statistics via API
curl -X GET "http://localhost:8000/api/statistics"

# 5. Get specific user
curl -X GET "http://localhost:8000/api/users/1"

# 6. Get their playlist
curl -X GET "http://localhost:8000/api/playlists/1"
```

### Test 2: Duplicate checking

```bash
# 1. Import CSV twice
python cli.py import-csv --csv spotify_data.csv
python cli.py import-csv --csv spotify_data.csv

# 2. Check that users are not duplicated
curl -X GET "http://localhost:8000/api/users" | grep count
# should be the same number as before

# 3. Check statistics
python cli.py stats
# Total Users should remain unchanged
```

## Performance Tests

### Load testing

```bash
# Install Apache Bench
# Windows: https://httpd.apache.org/download.cgi
# Linux: sudo apt-get install apache2-utils

# Test 1000 requests
ab -n 1000 -c 10 http://localhost:8000/api/users

# Test with logging
ab -n 100 -c 5 -g results.txt http://localhost:8000/api/statistics
```

## Debugging

### Enable SQL logging

In **config.py** set:
```python
DATABASE_ECHO = True
LOG_LEVEL = "DEBUG"
```

Run the application and see all SQL queries.

### Python Debugger

```python
import pdb

# Add at the desired location:
pdb.set_trace()

# An interactive debugger will appear in terminal
```

## Common Errors and Fixes

### Error: "sqlite3.OperationalError: database is locked"
```bash
python cli.py clean
```

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### API not accessible
- Check if application is running
- Check if server is listening on localhost:8000
- Check logs for error details

### CSV won't import
- Check CSV format (should be: email, subType, playlistName, songTitle, artist, duration, genre)
- Check encoding (UTF-8)
- Check file paths

## API Documentation

### OpenAPI (Swagger) - http://localhost:8000/docs
Interactive documentation with all endpoints

### ReDoc - http://localhost:8000/redoc
Alternative documentation

## Test Coverage

```bash
pip install pytest-cov

pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

---

**Готово до тестування! 🚀**

