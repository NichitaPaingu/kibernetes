from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
import sys

from app.models import SchoolRepository, StudentRepository, School, Student

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="School Management API",
    description="API для управления школами и студентами",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class SchoolCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Название школы")
    address: str = Field(..., min_length=1, description="Адрес школы")
    phone: str = Field(..., min_length=1, description="Телефон школы")

class SchoolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Название школы")
    address: Optional[str] = Field(None, min_length=1, description="Адрес школы")
    phone: Optional[str] = Field(None, min_length=1, description="Телефон школы")

class SchoolResponse(BaseModel):
    id: str
    name: str
    address: str
    phone: str
    created_at: str
    updated_at: str

class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=1, description="Имя студента")
    last_name: str = Field(..., min_length=1, description="Фамилия студента")
    age: int = Field(..., ge=5, le=25, description="Возраст студента")
    school_id: str = Field(..., description="ID школы")
    grade: str = Field(..., min_length=1, description="Класс/курс")

class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, description="Имя студента")
    last_name: Optional[str] = Field(None, min_length=1, description="Фамилия студента")
    age: Optional[int] = Field(None, ge=5, le=25, description="Возраст студента")
    school_id: Optional[str] = Field(None, description="ID школы")
    grade: Optional[str] = Field(None, min_length=1, description="Класс/курс")

class StudentResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    age: int
    school_id: str
    grade: str
    created_at: str
    updated_at: str

# Error handling middleware
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return {"error": "Internal server error", "detail": str(exc)}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "School Management API is running"}

# School endpoints
@app.post("/schools", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def create_school(school_data: SchoolCreate):
    """Создать новую школу"""
    try:
        school = SchoolRepository.create_school(
            name=school_data.name,
            address=school_data.address,
            phone=school_data.phone
        )
        logger.info(f"Created school: {school.id}")
        return school.to_dict()
    except Exception as e:
        logger.error(f"Error creating school: {e}")
        raise HTTPException(status_code=500, detail="Failed to create school")

@app.get("/schools", response_model=List[SchoolResponse])
async def get_all_schools():
    """Получить все школы"""
    try:
        schools = SchoolRepository.get_all_schools()
        return [school.to_dict() for school in schools]
    except Exception as e:
        logger.error(f"Error getting schools: {e}")
        raise HTTPException(status_code=500, detail="Failed to get schools")

@app.get("/schools/{school_id}", response_model=SchoolResponse)
async def get_school(school_id: str):
    """Получить школу по ID"""
    try:
        school = SchoolRepository.get_school(school_id)
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        return school.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting school {school_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get school")

@app.put("/schools/{school_id}", response_model=SchoolResponse)
async def update_school(school_id: str, school_data: SchoolUpdate):
    """Обновить школу"""
    try:
        school = SchoolRepository.update_school(
            school_id=school_id,
            name=school_data.name,
            address=school_data.address,
            phone=school_data.phone
        )
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        logger.info(f"Updated school: {school_id}")
        return school.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating school {school_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update school")

@app.delete("/schools/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_school(school_id: str):
    """Удалить школу"""
    try:
        success = SchoolRepository.delete_school(school_id)
        if not success:
            raise HTTPException(status_code=404, detail="School not found")
        logger.info(f"Deleted school: {school_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting school {school_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete school")

# Student endpoints
@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentCreate):
    """Создать нового студента"""
    try:
        # Verify school exists
        school = SchoolRepository.get_school(student_data.school_id)
        if not school:
            raise HTTPException(status_code=400, detail="School not found")
        
        student = StudentRepository.create_student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            age=student_data.age,
            school_id=student_data.school_id,
            grade=student_data.grade
        )
        logger.info(f"Created student: {student.id}")
        return student.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating student: {e}")
        raise HTTPException(status_code=500, detail="Failed to create student")

@app.get("/students", response_model=List[StudentResponse])
async def get_all_students():
    """Получить всех студентов"""
    try:
        students = StudentRepository.get_all_students()
        return [student.to_dict() for student in students]
    except Exception as e:
        logger.error(f"Error getting students: {e}")
        raise HTTPException(status_code=500, detail="Failed to get students")

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    """Получить студента по ID"""
    try:
        student = StudentRepository.get_student(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting student {student_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get student")

@app.get("/schools/{school_id}/students", response_model=List[StudentResponse])
async def get_students_by_school(school_id: str):
    """Получить всех студентов школы"""
    try:
        # Verify school exists
        school = SchoolRepository.get_school(school_id)
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        students = StudentRepository.get_students_by_school(school_id)
        return [student.to_dict() for student in students]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting students for school {school_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get students")

@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student_data: StudentUpdate):
    """Обновить студента"""
    try:
        # Verify school exists if school_id is being updated
        if student_data.school_id:
            school = SchoolRepository.get_school(student_data.school_id)
            if not school:
                raise HTTPException(status_code=400, detail="School not found")
        
        student = StudentRepository.update_student(
            student_id=student_id,
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            age=student_data.age,
            school_id=student_data.school_id,
            grade=student_data.grade
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        logger.info(f"Updated student: {student_id}")
        return student.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student {student_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update student")

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    """Удалить студента"""
    try:
        success = StudentRepository.delete_student(student_id)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        logger.info(f"Deleted student: {student_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete student")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 