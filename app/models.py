from typing import Dict, List, Optional
from datetime import datetime
import uuid

class School:
    def __init__(self, name: str, address: str, phone: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.phone = phone
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'School':
        school = cls(data['name'], data['address'], data['phone'])
        school.id = data['id']
        school.created_at = data['created_at']
        school.updated_at = data['updated_at']
        return school

class Student:
    def __init__(self, first_name: str, last_name: str, age: int, school_id: str, grade: str):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.school_id = school_id
        self.grade = grade
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'school_id': self.school_id,
            'grade': self.grade,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        student = cls(data['first_name'], data['last_name'], data['age'], data['school_id'], data['grade'])
        student.id = data['id']
        student.created_at = data['created_at']
        student.updated_at = data['updated_at']
        return student

# In-memory storage using dictionaries
schools_db: Dict[str, School] = {}
students_db: Dict[str, Student] = {}

class SchoolRepository:
    @staticmethod
    def create_school(name: str, address: str, phone: str) -> School:
        school = School(name, address, phone)
        schools_db[school.id] = school
        return school
    
    @staticmethod
    def get_school(school_id: str) -> Optional[School]:
        return schools_db.get(school_id)
    
    @staticmethod
    def get_all_schools() -> List[School]:
        return list(schools_db.values())
    
    @staticmethod
    def update_school(school_id: str, name: str = None, address: str = None, phone: str = None) -> Optional[School]:
        school = schools_db.get(school_id)
        if school:
            if name:
                school.name = name
            if address:
                school.address = address
            if phone:
                school.phone = phone
            school.updated_at = datetime.now().isoformat()
        return school
    
    @staticmethod
    def delete_school(school_id: str) -> bool:
        if school_id in schools_db:
            del schools_db[school_id]
            return True
        return False

class StudentRepository:
    @staticmethod
    def create_student(first_name: str, last_name: str, age: int, school_id: str, grade: str) -> Student:
        student = Student(first_name, last_name, age, school_id, grade)
        students_db[student.id] = student
        return student
    
    @staticmethod
    def get_student(student_id: str) -> Optional[Student]:
        return students_db.get(student_id)
    
    @staticmethod
    def get_all_students() -> List[Student]:
        return list(students_db.values())
    
    @staticmethod
    def get_students_by_school(school_id: str) -> List[Student]:
        return [student for student in students_db.values() if student.school_id == school_id]
    
    @staticmethod
    def update_student(student_id: str, first_name: str = None, last_name: str = None, 
                      age: int = None, school_id: str = None, grade: str = None) -> Optional[Student]:
        student = students_db.get(student_id)
        if student:
            if first_name:
                student.first_name = first_name
            if last_name:
                student.last_name = last_name
            if age is not None:
                student.age = age
            if school_id:
                student.school_id = school_id
            if grade:
                student.grade = grade
            student.updated_at = datetime.now().isoformat()
        return student
    
    @staticmethod
    def delete_student(student_id: str) -> bool:
        if student_id in students_db:
            del students_db[student_id]
            return True
        return False 