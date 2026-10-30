from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_roles
from app.models import User

router = APIRouter(prefix="/reports", tags=["SQL reports"])

@router.get("/student-gpa")
def student_gpa(student_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "teacher"))):
    return db.execute(text("""SELECT s.id AS student_id, s.student_number, u.full_name, ROUND(SUM(g.score*g.coefficient)/NULLIF(SUM(g.coefficient),0),2) AS weighted_average, COUNT(DISTINCT e.course_id) AS courses_count FROM students s JOIN users u ON u.id=s.user_id LEFT JOIN enrollments e ON e.student_id=s.id LEFT JOIN grades g ON g.enrollment_id=e.id WHERE s.id=:student_id GROUP BY s.id,s.student_number,u.full_name"""), {"student_id": student_id}).mappings().first()

@router.get("/department-performance")
def department_performance(db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "teacher"))):
    return db.execute(text("SELECT * FROM department_performance ORDER BY average_score DESC NULLS LAST")).mappings().all()

@router.get("/course-enrollment")
def course_enrollment(db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "teacher"))):
    return db.execute(text("SELECT * FROM course_enrollment_summary ORDER BY enrollment_count DESC")).mappings().all()

@router.get("/top-students")
def top_students(limit: int = 10, db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "teacher"))):
    limit = max(1, min(limit, 100))
    return db.execute(text("SELECT * FROM student_average WHERE weighted_average IS NOT NULL ORDER BY weighted_average DESC LIMIT :limit"), {"limit": limit}).mappings().all()
