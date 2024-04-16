from app import app
import psycopg2
import psycopg2.extras

def get_db_connection():
    conn = psycopg2.connect(app.config['DATABASE_URI'], cursor_factory=psycopg2.extras.DictCursor)
    return conn

def get_courses():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM courses')
    courses = cur.fetchall()
    cur.close()
    conn.close()
    return courses

def add_course(course_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO courses (course_name) VALUES (%s)', (course_name,))
    conn.commit()
    cur.close()
    conn.close()

def get_course_by_id(course_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM courses WHERE course_id = %s', (course_id,))
    course = cur.fetchone()
    cur.close()
    conn.close()
    return course

def update_course(course_id, course_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE courses SET course_name = %s WHERE course_id = %s', (course_name, course_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_course(course_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM courses WHERE course_id = %s', (course_id,))
    conn.commit()
    cur.close()
    conn.close()

def search_courses(search_by, search_term):
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_by == "code":
        query = "SELECT * FROM courses WHERE course_id = %s;"
    else:  # Assumes search_by == "name"
        query = "SELECT * FROM courses WHERE lower(course_name) LIKE lower(%s);"
        search_term = f"%{search_term}%"
    cursor.execute(query, (search_term,))
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses
