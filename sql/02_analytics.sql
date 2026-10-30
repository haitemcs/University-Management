-- Views, PL/pgSQL functions and audit triggers.
CREATE OR REPLACE VIEW student_average AS
SELECT s.id AS student_id, s.student_number, u.full_name,
       ROUND(SUM(g.score*g.coefficient)/NULLIF(SUM(g.coefficient),0),2) AS weighted_average,
       COUNT(DISTINCT e.course_id) AS courses_count
FROM students s JOIN users u ON u.id=s.user_id
LEFT JOIN enrollments e ON e.student_id=s.id
LEFT JOIN grades g ON g.enrollment_id=e.id
GROUP BY s.id,s.student_number,u.full_name;

CREATE OR REPLACE VIEW course_enrollment_summary AS
SELECT c.id AS course_id,c.code,c.title,d.name AS department_name,COUNT(e.id) AS enrollment_count
FROM courses c JOIN departments d ON d.id=c.department_id
LEFT JOIN enrollments e ON e.course_id=c.id
GROUP BY c.id,c.code,c.title,d.name;

CREATE OR REPLACE VIEW department_performance AS
SELECT d.id AS department_id,d.code,d.name,ROUND(AVG(g.score),2) AS average_score,
       COUNT(DISTINCT e.student_id) AS students_count,COUNT(g.id) AS grades_count
FROM departments d LEFT JOIN courses c ON c.department_id=d.id
LEFT JOIN enrollments e ON e.course_id=c.id LEFT JOIN grades g ON g.enrollment_id=e.id
GROUP BY d.id,d.code,d.name;

CREATE OR REPLACE FUNCTION audit_row_change() RETURNS TRIGGER AS $$
DECLARE target_id INTEGER;
BEGIN
  IF TG_OP='DELETE' THEN
    target_id:=OLD.id;
    INSERT INTO audit_logs(table_name,record_id,action,details) VALUES(TG_TABLE_NAME,target_id,TG_OP,row_to_json(OLD)::text);
    RETURN OLD;
  ELSE
    target_id:=NEW.id;
    INSERT INTO audit_logs(table_name,record_id,action,details) VALUES(TG_TABLE_NAME,target_id,TG_OP,row_to_json(NEW)::text);
    RETURN NEW;
  END IF;
END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_courses_changes ON courses;
CREATE TRIGGER audit_courses_changes AFTER INSERT OR UPDATE OR DELETE ON courses FOR EACH ROW EXECUTE FUNCTION audit_row_change();
DROP TRIGGER IF EXISTS audit_grades_changes ON grades;
CREATE TRIGGER audit_grades_changes AFTER INSERT OR UPDATE OR DELETE ON grades FOR EACH ROW EXECUTE FUNCTION audit_row_change();

CREATE OR REPLACE FUNCTION calculate_student_average(p_student_id INTEGER) RETURNS NUMERIC(5,2) AS $$
DECLARE result NUMERIC(5,2);
BEGIN
  SELECT ROUND(SUM(g.score*g.coefficient)/NULLIF(SUM(g.coefficient),0),2) INTO result
  FROM enrollments e JOIN grades g ON g.enrollment_id=e.id WHERE e.student_id=p_student_id;
  RETURN result;
END; $$ LANGUAGE plpgsql STABLE;
