from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
now = datetime.now()


app = Flask(__name__)

# Подключение к базе данных SQLite
conn = sqlite3.connect('attendance1.db', check_same_thread=False)
cur = conn.cursor()

# Создание таблицы в базе данных, если она еще не создана
cur.execute('''CREATE TABLE IF NOT EXISTS students
                (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, attended INTEGER)''')
conn.commit()
context= {}
@app.route('/')
def index():
    context['week'] = datetime.weekday(now)
    return render_template('index.html', context=context)

@app.route('/names', methods=['GET'])
def get_names():
    # cur.execute('''SELECT name, attended, group_ FROM students ''')
    if (datetime.weekday(now) % 2 == 0):
        cur.execute('''SELECT name, attended, group_ FROM students ORDER BY attended''')
    else:
        cur.execute('''SELECT name, attended, group1_ FROM students ORDER BY attended''')
    rows = cur.fetchall()
    names = [{'name': row[0], 'attended': bool(row[1]), 'group': row[2]} for row in rows]
    return jsonify(names)

@app.route('/attendance', methods=['POST'])
def update_attendance():
    data = request.get_json()
    selected_names = data.get('names', [])
    print(data, selected_names)
    for name in selected_names:
        attended = 1 if name.get('checked', False) else 0  # Если имя отмечено, то attended = 1, иначе attended = 0
        # Обновляем статус посещаемости в базе данных
        cur.execute('''UPDATE students SET attended = ? WHERE name = ?''', (attended, name['name']))
        conn.commit()
    return jsonify({'message': 'Attendance updated successfully'})



if __name__ == '__main__':
    app.run()

# from datetime import datetime
# now = datetime.now()


# from flask import Flask, render_template, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance1.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# # db.create_all()
# # Определение модели для таблицы students
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     attended = db.Column(db.Boolean, nullable=False, default=False)
#     group_ = db.Column(db.String(100))
#     group1_ = db.Column(db.String(100))

# # Создание всех таблиц в базе данных

# context = {

# }
# @app.route('/')
# def index():
#     context['week']=datetime.weekday(now)
#     return render_template('index.html', context=context)

# @app.route('/names', methods=['GET'])
# def get_names():
#     students = Student.query.order_by(Student.attended).all()

#     # names = [{'name': student.name, 'attended': student.attended, 'group': student.group1_} for student in students]
#     if (datetime.weekday(now)  % 2 == 0):
#         names = [{'name': student.name, 'attended': student.attended, 'group': student.group_} for student in students]
#     else:
#         names = [{'name': student.name, 'attended': student.attended, 'group': student.group1_} for student in students]
#     return jsonify(names)

# @app.route('/attendance', methods=['POST'])
# def update_attendance():
#     data = request.get_json()
#     selected_names = data.get('names', [])
#     print(data, selected_names)
#     for name in selected_names:
#         attended = name.get('checked', False)
#         # Обновляем статус посещаемости в базе данных
#         student = Student.query.filter_by(name=name['name']).first()
#         if student:
#             student.attended = attended
#             db.session.commit()
#     return jsonify({'message': 'Attendance updated successfully'})
# with app.app_context():

#         db.create_all()
# if __name__ == '__main__':
#     with app.app_context():

#         db.create_all()
#     app.run()
