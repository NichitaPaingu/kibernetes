# School Management API

Простое API для управления школами и студентами с использованием словарей для хранения данных.

## Структура проекта

```
.
├── app/
│   ├── main.py          # FastAPI приложение
│   └── models.py        # Модели данных и репозитории
├── k8s/
│   ├── deployment.yaml  # Kubernetes deployment
│   └── service.yaml     # Kubernetes service
├── Dockerfile           # Docker конфигурация
├── requirements.txt     # Python зависимости
└── README.md           # Документация
```

## Возможности API

### Школы

- `POST /schools` - Создать школу
- `GET /schools` - Получить все школы
- `GET /schools/{id}` - Получить школу по ID
- `PUT /schools/{id}` - Обновить школу
- `DELETE /schools/{id}` - Удалить школу

### Студенты

- `POST /students` - Создать студента
- `GET /students` - Получить всех студентов
- `GET /students/{id}` - Получить студента по ID
- `PUT /students/{id}` - Обновить студента
- `DELETE /students/{id}` - Удалить студента
- `GET /schools/{id}/students` - Получить студентов школы

## Локальный запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск приложения

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Доступ к API

- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Docker запуск

### 1. Сборка образа

```bash
docker build -t school-api:latest .
```

### 2. Запуск контейнера

```bash
docker run -p 8000:8000 school-api:latest
```

## Kubernetes развертывание

### 1. Сборка и загрузка образа

```bash
# Для Minikube
eval $(minikube docker-env)
docker build -t school-api:latest .

# Для Docker Desktop
docker build -t school-api:latest .
```

### 2. Применение конфигураций

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 3. Проверка статуса

```bash
kubectl get pods
kubectl get services
```

### 4. Доступ к сервису

```bash
# Для Minikube
minikube service school-api-service

# Для Docker Desktop
kubectl port-forward service/school-api-service 8080:80
```

## Примеры использования

### Создание школы

```bash
curl -X POST "http://localhost:8000/schools" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Школа №1",
    "address": "ул. Пушкина, 10",
    "phone": "+7-123-456-7890"
  }'
```

### Создание студента

```bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Иван",
    "last_name": "Иванов",
    "age": 15,
    "school_id": "SCHOOL_ID_HERE",
    "grade": "9А"
  }'
```

### Получение всех школ

```bash
curl -X GET "http://localhost:8000/schools"
```

### Получение студентов школы

```bash
curl -X GET "http://localhost:8000/schools/SCHOOL_ID_HERE/students"
```

## Особенности

- **In-memory хранение**: Данные хранятся в памяти с использованием словарей
- **Валидация**: Все входные данные валидируются с помощью Pydantic
- **Обработка ошибок**: Полная обработка ошибок с логированием
- **Health checks**: Проверка состояния приложения
- **CORS**: Поддержка кросс-доменных запросов
- **Логирование**: Подробное логирование всех операций
- **Масштабируемость**: Готовность к развертыванию в Kubernetes

## Мониторинг

- Health check endpoint: `/health`
- Автоматическая документация: `/docs`
- Альтернативная документация: `/redoc`
