import sqlalchemy
from flask import render_template, request

from . import app
from . import db
from . import Student


@app.route('/')
def index():
    content = list()
    students = db.engine.execute('SELECT student_id, surname, name, patronymic, age, faculty, course FROM student')
    col_names = list(students.keys())
    for i in students:
        content.append({
            "student_id": i[0],
            "surname": i[1],
            "name": i[2],
            "patronymic": i[3],
            "age": i[4],
            "faculty": i[5],
            "course": i[6]
        })
    return render_template("students.html", col_names=col_names, students=content)


@app.route("/add", methods=["post", "get"])
def add():
    messages = []
    student = {}

    if request.method == "POST":
        for name_col in ("student_id", "surname", "name", "patronymic", "faculty", "age", "course"):
            student[name_col] = data if (data := request.form.get(name_col)) else None
        try:
            student["age"] = int(student['age'])
        except (ValueError, TypeError):
            messages.append('Возраст введен некорректно')

        try:
            student["course"] = int(student['course'])
        except (ValueError, TypeError):
            messages.append('Курс введен некорректно')

        if not messages:
            try:
                Student.add(**student)
                student = {}
            except sqlalchemy.exc.IntegrityError:
                messages = ['Введите все необходимые поля корректно']

    return render_template("add.html", messages=messages, form_data=student)


@app.route("/injection", methods=["post", "get"])
def injection():
    message = ''
    sql_req = ''
    students = []

    if request.method == "POST":
        sql_req = request.form.get('sql')
        try:
            result = db.engine.execute(sql_req)
            if result.returns_rows:
                students = result
        except:
            message = 'Что-то пошло не так'
    return render_template("injection.html", sql_req=sql_req, students=students, message=message)
