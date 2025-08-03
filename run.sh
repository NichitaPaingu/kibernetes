#!/bin/bash

echo "🚀 School Management API - Quick Start"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен. Пожалуйста, установите Python 3.8+"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip не установлен. Пожалуйста, установите pip"
    exit 1
fi

echo "📦 Установка зависимостей..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Зависимости установлены успешно"
else
    echo "❌ Ошибка при установке зависимостей"
    exit 1
fi

echo "🔧 Запуск приложения..."
echo "🌐 API будет доступен по адресу: http://localhost:8000"
echo "📚 Документация: http://localhost:8000/docs"
echo "💚 Health check: http://localhost:8000/health"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 