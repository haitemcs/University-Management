from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=150)

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: str | None = None

class CourseCreate(BaseModel):
    code: str
    title: str
    credits: int = Field(ge=1, le=12)
    department_id: int
    teacher_id: int | None = None
    semester: str

class StudentCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    student_number: str
    enrollment_year: int = Field(ge=2000, le=2100)
    date_of_birth: date | None = None

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    academic_year: str

class GradeCreate(BaseModel):
    enrollment_id: int
    assessment_name: str
    score: float = Field(ge=0, le=20)
    coefficient: float = Field(default=1, gt=0, le=10)
