from flask import render_template, request, redirect, url_for, flash
from app import app
from app.models.course import get_courses, add_course, get_course_by_id, update_course, delete_course, search_courses
from app.models.student import get_students, add_student, get_student_by_id, update_student, delete_student, search_students

@app.route('/')
def index():
    return render_template('index.html', courses=get_courses(), students=get_students())

@app.route('/courses')
def courses():
    courses = get_courses()
    return render_template('course.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course_route():
    if request.method == 'POST':
        course_name = request.form['name']
        add_course(course_name)
        flash('Course successfully added!', 'success')
        return redirect('/courses')
    return render_template('add_course.html')

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if request.method == 'POST':
        course_name = request.form['name']
        update_course(course_id, course_name)
        flash('Course information successfully updated!', 'success')
        return redirect('/courses')
    course = get_course_by_id(course_id)
    return render_template('edit_course.html', course=course)

@app.route('/delete_course/<int:course_id>')
def delete_course_route(course_id):
    delete_course(course_id)
    flash('Course successfully deleted!', 'success')
    return redirect('/courses')

@app.route('/students')
def students():
    students = get_students()
    return render_template('student.html', students=students, courses=get_courses())

@app.route('/add_student', methods=['GET', 'POST'])
def add_student_route():
    if request.method == 'POST':
        student_name = request.form['student_name']
        course_id = request.form['course_id']
        add_student(student_name, course_id)
        flash('Student successfully added!', 'success')
        return redirect('/students')
    return render_template('add_student.html', courses=get_courses())

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        student_name = request.form['student_name']
        course_id = request.form['course_id']
        update_student(student_id, student_name, course_id)
        flash('Student information successfully updated!', 'success')
        return redirect('/students')
    student = get_student_by_id(student_id)
    courses = get_courses()
    return render_template('edit_student.html', student=student, courses=courses)

@app.route('/delete_student/<int:student_id>')
def delete_student_route(student_id):
    delete_student(student_id)
    flash('Student successfully deleted!', 'success')
    return redirect('/students')

@app.route('/search_student', methods=['POST'])
def search_student():
    search_by = request.form['search_by']
    search_term = request.form['search_term']
    students = search_students(search_by, search_term)
    if not students:
        flash('No results found', 'info')
    return render_template('student.html', students=students)

@app.route('/search_course', methods=['POST'])
def search_course():
    search_by = request.form['search_by']
    search_term = request.form['search_term']
    courses = search_courses(search_by, search_term)
    if not courses:
        flash('No results found', 'info')
    return render_template('course.html', courses=courses)