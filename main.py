import os

from student_app import app, db, Student

if not os.path.isfile("student_app/db/student.sqlite"):
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
