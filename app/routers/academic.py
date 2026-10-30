from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_roles
from app.models import Course, Department, Enrollment, Grade, Role, Student, User
from app.schemas import CourseCreate, DepartmentCreate, EnrollmentCreate, GradeCreate, StudentCreate
from app.security import hash_password

router = APIRouter(tags=["Academic data"])

@router.post("/departments", status_code=201)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    row = Department(**data.model_dump())
    db.add(row); db.commit(); db.refresh(row)
    return {"id": row.id, "name": row.name, "code": row.code}

@router.get("/departments")
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).order_by(Department.name).all()

@router.post("/students", status_code=201)
def create_student(data: StudentCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    if db.query(User).filter_by(email=data.email).first(): raise HTTPException(409, "Email already registered")
    if db.query(Student).filter_by(student_number=data.student_number).first(): raise HTTPException(409, "Student number already exists")
    role = db.query(Role).filter_by(name="student").one()
    user = User(email=data.email, password_hash=hash_password(data.password), full_name=data.full_name, role=role)
    db.add(user); db.flush()
    student = Student(user_id=user.id, student_number=data.student_number, enrollment_year=data.enrollment_year, date_of_birth=data.date_of_birth)
    db.add(student); db.commit()
    return {"student_id": student.id, "user_id": user.id, "student_number": student.student_number}

@router.get("/students")
def list_students(db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "teacher"))):
    return db.execute(text("SELECT s.id, s.student_number, u.full_name, u.email, s.enrollment_year FROM students s JOIN users u ON u.id=s.user_id ORDER BY u.full_name")).mappings().all()

@router.post("/courses", status_code=201)
def create_course(data: CourseCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    if not db.get(Department, data.department_id): raise HTTPException(404, "Department not found")
    row = Course(**data.model_dump()); db.add(row); db.commit(); db.refresh(row)
    return row

@router.get("/courses")
def list_courses(department_id: int | None = None, semester: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Course)
    if department_id is not None: query = query.filter(Course.department_id == department_id)
    if semester: query = query.filter(Course.semester == semester)
    return query.order_by(Course.code).all()

@router.post("/enrollments", status_code=201)
def enroll(data: EnrollmentCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    if not db.get(Student, data.student_id) or not db.get(Course, data.course_id): raise HTTPException(404, "Student or course not found")
    row = Enrollment(**data.model_dump()); db.add(row)
    try: db.commit()
    except Exception:
        db.rollback(); raise HTTPException(409, "Duplicate enrollment or invalid data")
    db.refresh(row)
    return {"id": row.id, "student_id": row.student_id, "course_id": row.course_id, "status": row.status}

@router.post("/grades", status_code=201)
def add_grade(data: GradeCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "teacher"))):
    if not db.get(Enrollment, data.enrollment_id): raise HTTPException(404, "Enrollment not found")
    row = Grade(**data.model_dump()); db.add(row); db.commit(); db.refresh(row)
    return {"id": row.id, "enrollment_id": row.enrollment_id, "score": float(row.score)}
