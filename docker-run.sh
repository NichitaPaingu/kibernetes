#!/bin/bash

echo "🐳 School Management API - Docker Quick Start"
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker не запущен. Пожалуйста, запустите Docker"
    exit 1
fi

echo "🔨 Сборка Docker образа..."
docker build -t school-api:latest .

if [ $? -eq 0 ]; then
    echo "✅ Образ собран успешно"
else
    echo "❌ Ошибка при сборке образа"
    exit 1
fi

echo "🚀 Запуск контейнера..."
echo "🌐 API будет доступен по адресу: http://localhost:8000"
echo "📚 Документация: http://localhost:8000/docs"
echo "💚 Health check: http://localhost:8000/health"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

docker run -p 8000:8000 school-api:latest 