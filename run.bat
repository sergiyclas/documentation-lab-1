@echo off
REM Run Spotify API Builder (with uv)
REM Usage: run.bat [command]

setlocal enabledelayedexpansion

set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=dev

echo.
echo =====================================================
echo   Spotify Platform - Python/FastAPI (uv)
echo =====================================================
echo.

if /i "%COMMAND%"=="install" (
    echo Installing dependencies with uv...
    uv sync
    echo Dependencies installed!
) else if /i "%COMMAND%"=="dev" (
    echo Starting development server...
    uv run python main.py
) else if /i "%COMMAND%"=="build" (
    echo Building application...
    echo Note: No build step needed for Python
    echo Application is ready to run!
) else if /i "%COMMAND%"=="init" (
    echo Initializing database...
    uv run python cli.py init-db
    echo Database initialized!
) else if /i "%COMMAND%"=="import" (
    echo Importing CSV data...
    set CSV=%2
    if "!CSV!"=="" set CSV=spotify_data.csv
    uv run python cli.py import-csv --csv !CSV!
) else if /i "%COMMAND%"=="stats" (
    echo Showing database statistics...
    uv run python cli.py stats
) else if /i "%COMMAND%"=="clean" (
    echo Cleaning database...
    uv run python cli.py clean
) else if /i "%COMMAND%"=="help" (
    echo Available commands:
    echo.
    echo   run.bat install      - Install dependencies with uv
    echo   run.bat dev          - Start development server
    echo   run.bat init         - Initialize database
    echo   run.bat import       - Import CSV data
    echo   run.bat stats        - Show database statistics
    echo   run.bat clean        - Clean database
    echo   run.bat help         - Show this help message
) else (
    echo Unknown command: %COMMAND%
    echo Run "run.bat help" for available commands
)

echo.
