-- 1. Multi-table JOIN: students, courses and departments.
SELECT s.student_number,u.full_name,c.code,c.title,d.name AS department
FROM students s JOIN users u ON u.id=s.user_id
JOIN enrollments e ON e.student_id=s.id JOIN courses c ON c.id=e.course_id
JOIN departments d ON d.id=c.department_id ORDER BY u.full_name,c.code;

-- 2. NOT EXISTS: students without an enrollment.
SELECT s.id,s.student_number FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id=s.id);

-- 3. Subquery: courses above the average enrollment count.
SELECT course_id,code,title,enrollment_count FROM course_enrollment_summary
WHERE enrollment_count>(SELECT AVG(enrollment_count) FROM course_enrollment_summary);

-- 4. Window function: rank students by average inside each department.
SELECT department_name,student_number,full_name,weighted_average,
DENSE_RANK() OVER(PARTITION BY department_name ORDER BY weighted_average DESC) AS department_rank
FROM (SELECT d.name AS department_name,s.student_number,u.full_name,calculate_student_average(s.id) AS weighted_average
      FROM students s JOIN users u ON u.id=s.user_id JOIN enrollments e ON e.student_id=s.id
      JOIN courses c ON c.id=e.course_id JOIN departments d ON d.id=c.department_id
      GROUP BY d.name,s.id,s.student_number,u.full_name) ranked
ORDER BY department_name,department_rank;

-- 5. CASE and GROUP BY: grade distribution.
SELECT CASE WHEN score>=16 THEN 'Excellent' WHEN score>=14 THEN 'Good'
            WHEN score>=10 THEN 'Pass' ELSE 'Fail' END AS grade_category,COUNT(*) AS total
FROM grades GROUP BY grade_category ORDER BY total DESC;
