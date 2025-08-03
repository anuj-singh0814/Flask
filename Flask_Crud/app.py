from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("students.db")

def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)

create_table()

@app.route('/')
def index():
    with connect_db() as conn:
        students = conn.execute("SELECT * FROM students").fetchall()
    return render_template("index.html", students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        with connect_db() as conn:
            conn.execute("INSERT INTO students (id, name, age) VALUES (?, ?, ?)", (id, name, age))
        return redirect(url_for('index'))
    return render_template("add.html")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        with connect_db() as conn:
            conn.execute("UPDATE students SET name = ?, age = ? WHERE id = ?", (name, age, id))
        return redirect(url_for('index'))
    else:
        with connect_db() as conn:
            student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
        return render_template("update.html", student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    with connect_db() as conn:
        conn.execute("DELETE FROM students WHERE id = ?", (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
