from app import app
import psycopg2
import psycopg2.extras

def get_db_connection():
    conn = psycopg2.connect(app.config['DATABASE_URI'], cursor_factory=psycopg2.extras.DictCursor)
    return conn

def get_students():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT s.*, c.course_name FROM students s JOIN courses c ON s.course_id = c.course_id')
    students = cur.fetchall()
    cur.close()
    conn.close()
    return students

def add_student(student_name, course_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO students (student_name, course_id) VALUES (%s, %s)', (student_name, course_id))
    conn.commit()
    cur.close()
    conn.close()

def get_student_by_id(student_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    return student

def update_student(student_id, student_name, course_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE students SET student_name = %s, course_id = %s WHERE student_id = %s', (student_name, course_id, student_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM students WHERE student_id = %s', (student_id,))
    conn.commit()
    cur.close()
    conn.close()
    
def search_students(search_by, search_term):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ""
    if search_by == "id":
        query = """
        SELECT students.*, courses.course_name 
        FROM students 
        JOIN courses ON students.course_id = courses.course_id 
        WHERE students.student_id = %s;
        """
    elif search_by == "student_name":
        query = """
        SELECT students.*, courses.course_name 
        FROM students 
        JOIN courses ON students.course_id = courses.course_id 
        WHERE lower(students.student_name) LIKE lower(%s);
        """
        search_term = f"%{search_term}%"
    elif search_by == "course_code":
        query = """
        SELECT students.*, courses.course_name 
        FROM students 
        JOIN courses ON students.course_id = courses.course_id 
        WHERE lower(courses.course_name) LIKE lower(%s);
        """
    cursor.execute(query, (search_term,))
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return students