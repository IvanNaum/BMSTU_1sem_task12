import os

import sqlalchemy
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/db/student.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    student_id = db.Column(db.String, unique=True, nullable=False)
    surname = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String)
    age = db.Column(db.Integer, nullable=False)
    faculty = db.Column(db.String, nullable=False)
    course = db.Column(db.Integer, nullable=False)

    @staticmethod
    def add(student_id, surname, name, patronymic, age, faculty, course):
        student = {
            "student_id": student_id,
            "surname": surname,
            "name": name,
            "patronymic": patronymic,
            "age": age,
            "faculty": faculty,
            "course": course
        }
        db.session.add(Student(**student))
        db.session.commit()


@app.route('/')
def index():
    content = list()
    students = db.engine.execute('SELECT * FROM student')
    for i in students:
        content.append({
            "student_id": i[1],
            "surname": i[2],
            "name": i[3],
            "patronymic": i[4],
            "age": i[5],
            "faculty": i[6],
            "course": i[7]
        })
    return render_template("students.html", students=content)


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
    sql_req = ''
    students = []

    if request.method == "POST":
        sql_req = request.form.get('sql')
        students = db.engine.execute(sql_req)
        print(students)

    return render_template("injection.html", sql_req=sql_req, students=students)


if not os.path.isfile("db/student.sqlite"):
    '''Создание(Модификация) соответствующей базы данных и таблицы из   заготовленных шаблонов'''
    with app.app_context():
        db.create_all()

        for i in ({"student_id": "123321", "surname": "Иванов", "name": "Иван", "patronymic": "Иванович", "age": 18,
                   "faculty": "ИУ", "course": 1},
                  {"student_id": "123456", "surname": "Петров", "name": "Петр", "patronymic": "Петрович", "age": 20,
                   "faculty": "ИУ", "course": 2},
                  {"student_id": "121212", "surname": "Сидоров", "name": "Никита", "patronymic": "", "age": 19,
                   "faculty": "ИУ", "course": 3},
                  {"student_id": "321987", "surname": "Семенов", "name": "Константин", "patronymic": "Иванович",
                   "age": 23, "faculty": "РТ", "course": 6},
                  {"student_id": "123234", "surname": "Коприков", "name": "Сергей", "patronymic": "Иванович", "age": 21,
                   "faculty": "РТ", "course": 4},
                  {"student_id": "345567", "surname": "Цой", "name": "Александр", "patronymic": "Иванович", "age": 19,
                   "faculty": "РТ", "course": 1}):
            Student.add(**i)

        res = db.engine.execute('SELECT * FROM student')
        print(*res, sep="\n")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
