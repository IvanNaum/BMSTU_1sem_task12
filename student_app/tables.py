from . import db


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

