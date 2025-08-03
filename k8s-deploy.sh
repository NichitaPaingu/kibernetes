#!/bin/bash

echo "☸️ School Management API - Kubernetes Deployment"
echo "==============================================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl не установлен. Пожалуйста, установите kubectl"
    exit 1
fi

# Check if kubectl can connect to cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Не удается подключиться к Kubernetes кластеру"
    echo "Убедитесь, что кластер запущен (minikube start или docker-desktop)"
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

echo "📦 Применение Kubernetes конфигураций..."

echo "Deploying deployment..."
kubectl apply -f k8s/deployment.yaml

echo "Deploying service..."
kubectl apply -f k8s/service.yaml

echo "⏳ Ожидание запуска подов..."
kubectl wait --for=condition=ready pod -l app=school-api --timeout=300s

if [ $? -eq 0 ]; then
    echo "✅ Поды запущены успешно"
else
    echo "❌ Ошибка при запуске подов"
    exit 1
fi

echo ""
echo "📊 Статус развертывания:"
kubectl get pods -l app=school-api
kubectl get services -l app=school-api

echo ""
echo "🌐 Доступ к API:"

# Check if running in minikube
if kubectl config current-context | grep -q "minikube"; then
    echo "Для Minikube:"
    echo "minikube service school-api-service"
    echo ""
    echo "Или используйте port-forward:"
    echo "kubectl port-forward service/school-api-service 8080:80"
    echo "Затем откройте: http://localhost:8080"
else
    echo "Для Docker Desktop:"
    echo "kubectl port-forward service/school-api-service 8080:80"
    echo "Затем откройте: http://localhost:8080"
fi

echo ""
echo "📚 Документация будет доступна по адресу: /docs"
echo "💚 Health check: /health"

echo ""
echo "Для удаления развертывания выполните:"
echo "kubectl delete -f k8s/" 