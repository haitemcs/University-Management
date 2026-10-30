-- Relational schema: keys, constraints and indexes.
CREATE TABLE IF NOT EXISTS roles (id SERIAL PRIMARY KEY, name VARCHAR(30) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, full_name VARCHAR(150) NOT NULL, role_id INTEGER NOT NULL REFERENCES roles(id), is_active BOOLEAN NOT NULL DEFAULT TRUE, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW());
CREATE TABLE IF NOT EXISTS departments (id SERIAL PRIMARY KEY, name VARCHAR(120) NOT NULL UNIQUE, code VARCHAR(12) NOT NULL UNIQUE, description TEXT);
CREATE TABLE IF NOT EXISTS students (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE, student_number VARCHAR(30) NOT NULL UNIQUE, date_of_birth DATE, enrollment_year INTEGER NOT NULL CHECK (enrollment_year BETWEEN 2000 AND 2100));
CREATE TABLE IF NOT EXISTS teachers (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE, department_id INTEGER NOT NULL REFERENCES departments(id), employee_number VARCHAR(30) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS courses (id SERIAL PRIMARY KEY, code VARCHAR(20) NOT NULL UNIQUE, title VARCHAR(180) NOT NULL, credits INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 12), department_id INTEGER NOT NULL REFERENCES departments(id), teacher_id INTEGER REFERENCES teachers(id), semester VARCHAR(20) NOT NULL);
CREATE TABLE IF NOT EXISTS enrollments (id SERIAL PRIMARY KEY, student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE, course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE, academic_year VARCHAR(9) NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'enrolled', enrolled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), CONSTRAINT uq_student_course_year UNIQUE(student_id, course_id, academic_year));
CREATE TABLE IF NOT EXISTS grades (id SERIAL PRIMARY KEY, enrollment_id INTEGER NOT NULL REFERENCES enrollments(id) ON DELETE CASCADE, assessment_name VARCHAR(100) NOT NULL, score NUMERIC(5,2) NOT NULL CHECK (score BETWEEN 0 AND 20), coefficient NUMERIC(5,2) NOT NULL DEFAULT 1 CHECK (coefficient > 0), recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW());
CREATE TABLE IF NOT EXISTS audit_logs (id SERIAL PRIMARY KEY, table_name VARCHAR(80) NOT NULL, record_id INTEGER NOT NULL, action VARCHAR(10) NOT NULL, changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), details TEXT);
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);
CREATE INDEX IF NOT EXISTS idx_courses_department_id ON courses(department_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_student_id ON enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course_id ON enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_grades_enrollment_id ON grades(enrollment_id);
