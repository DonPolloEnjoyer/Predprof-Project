import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())#.encode("utf-8"))
    conn.commit()
    conn.close()
    print("db done")

# init_db()
# @app.before_first_request
# def before_first_request_func():
#     init_db()

app = Flask(__name__)
app.secret_key = "test" #os.urandom(24)  # Секретный ключ для сессий

@app.route("/auth/index1")
def Tohome1():
    return redirect("/")
@app.route("/index1")
def Tohome2():
    return redirect("/")

@app.route("/")
def index1():
    return render_template("index1.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO userlist (user_login, user_password, user_role) VALUES (?, ?, ?)',
                        (username, hashed_password, "user"))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('auth/register.html', error='Логин уже занят')
        conn.close()
        return redirect(url_for('blank'))
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM userlist WHERE user_login = ?', (username,)).fetchone()
        conn.close()
        if user is None:
            return render_template('auth/login.html', error='Неверный логин')
        if (user and check_password_hash(user['user_password'], password)):
            session['user_login'] = user['user_login']
            return redirect(url_for('blank'))
        return render_template('auth/login.html', error='Неверный пароль или логин')
    return render_template('auth/login.html')


@app.route('/blank')
def blank():
    if 'user_login' in session:
        username = session['user_login']
        return render_template('Blank1.html', username=username)
    return redirect(url_for('login'))

@app.route("/view", methods = ["GET", "POST"])
def view():
    if request.method == "POST":
        title = request.form['title']
        Number = request.form['Number']
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO inventory (item_title, item_number) VALUES (?, ?)",
            (title, Number,)
        )
        conn.commit()
    
    
    conn = get_db_connection()
    items = []
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    for i in range(1, rows + 1):
        record = conn.execute(
        "SELECT * FROM inventory WHERE item_id = ?;",
        (i,)
        ).fetchone()
        items.append(record)
        print(items)
    # records = conn.execute(
    #     "SELECT * FROM inventory"
    # ).fetchone()
    # for record in records:
    #     items.append(record)
    conn.close()
    if 'user_role' in session:
        if (session["user_role"] == "admin"):
            isadmin = True
        else:
            isadmin = False
    
    
    
    return render_template("view.html",isadmin = True, items = items)

@app.route('/logout')
def logout():
    # session.pop('username', None)
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='',port='',debug=True)

# flask --app app run

