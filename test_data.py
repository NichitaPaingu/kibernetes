#!/usr/bin/env python3
"""
Скрипт для добавления тестовых данных в API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    """Тестирование API с добавлением тестовых данных"""
    
    print("🧪 Тестирование School Management API")
    print("=" * 40)
    
    # Проверка health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check прошел успешно")
        else:
            print("❌ Health check не прошел")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен.")
        return
    
    # Создание школ
    schools_data = [
        {
            "name": "Школа №1 имени Пушкина",
            "address": "ул. Пушкина, 10, Москва",
            "phone": "+7-495-123-4567"
        },
        {
            "name": "Гимназия №2",
            "address": "пр. Мира, 25, Санкт-Петербург",
            "phone": "+7-812-987-6543"
        },
        {
            "name": "Лицей №3",
            "address": "ул. Ленина, 15, Казань",
            "phone": "+7-843-555-1234"
        }
    ]
    
    created_schools = []
    print("\n🏫 Создание школ...")
    
    for i, school_data in enumerate(schools_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/schools",
                json=school_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 201:
                school = response.json()
                created_schools.append(school)
                print(f"✅ Школа {i} создана: {school['name']} (ID: {school['id']})")
            else:
                print(f"❌ Ошибка создания школы {i}: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка при создании школы {i}: {e}")
    
    if not created_schools:
        print("❌ Не удалось создать школы. Прерывание теста.")
        return
    
    # Создание студентов
    students_data = [
        {
            "first_name": "Иван",
            "last_name": "Иванов",
            "age": 15,
            "school_id": created_schools[0]['id'],
            "grade": "9А"
        },
        {
            "first_name": "Мария",
            "last_name": "Петрова",
            "age": 16,
            "school_id": created_schools[0]['id'],
            "grade": "10Б"
        },
        {
            "first_name": "Алексей",
            "last_name": "Сидоров",
            "age": 14,
            "school_id": created_schools[1]['id'],
            "grade": "8В"
        },
        {
            "first_name": "Анна",
            "last_name": "Козлова",
            "age": 17,
            "school_id": created_schools[1]['id'],
            "grade": "11А"
        },
        {
            "first_name": "Дмитрий",
            "last_name": "Смирнов",
            "age": 13,
            "school_id": created_schools[2]['id'],
            "grade": "7Б"
        }
    ]
    
    created_students = []
    print("\n👨‍🎓 Создание студентов...")
    
    for i, student_data in enumerate(students_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/students",
                json=student_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 201:
                student = response.json()
                created_students.append(student)
                print(f"✅ Студент {i} создан: {student['first_name']} {student['last_name']} (ID: {student['id']})")
            else:
                print(f"❌ Ошибка создания студента {i}: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка при создании студента {i}: {e}")
    
    # Тестирование получения данных
    print("\n📊 Тестирование получения данных...")
    
    # Получение всех школ
    try:
        response = requests.get(f"{BASE_URL}/schools")
        if response.status_code == 200:
            schools = response.json()
            print(f"✅ Получено школ: {len(schools)}")
        else:
            print(f"❌ Ошибка получения школ: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при получении школ: {e}")
    
    # Получение всех студентов
    try:
        response = requests.get(f"{BASE_URL}/students")
        if response.status_code == 200:
            students = response.json()
            print(f"✅ Получено студентов: {len(students)}")
        else:
            print(f"❌ Ошибка получения студентов: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при получении студентов: {e}")
    
    # Получение студентов первой школы
    if created_schools:
        try:
            response = requests.get(f"{BASE_URL}/schools/{created_schools[0]['id']}/students")
            if response.status_code == 200:
                school_students = response.json()
                print(f"✅ Студентов в школе '{created_schools[0]['name']}': {len(school_students)}")
            else:
                print(f"❌ Ошибка получения студентов школы: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка при получении студентов школы: {e}")
    
    print("\n🎉 Тестирование завершено!")
    print(f"🌐 API доступен по адресу: {BASE_URL}")
    print(f"📚 Документация: {BASE_URL}/docs")
    print(f"💚 Health check: {BASE_URL}/health")

if __name__ == "__main__":
    test_api() 