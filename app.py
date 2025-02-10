import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import flask as fk

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql') as f:
    # with open('D:\\Prog1\\PredprofOL1\\Server\\schema.sql') as f:
        conn.executescript(f.read())#.encode("utf-8"))
    conn.commit()
    conn.close()
    print("db done")
def Set_admin(username):
    conn = get_db_connection()
    conn.execute("UPDATE userlist SET user_role = ? WHERE user_login = ?",
    ("admin", username,))
    conn.commit()
    print(f"{username} теперь админ")
# Set_admin("admin1")
# init_db()

# @app.before_request
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

        if(len(password) < 8) or (" " in password):
            return render_template('auth/register.html', error='Пароль невозможен')

        hashed_password = generate_password_hash(password)
        print(hashed_password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO userlist (user_login, user_password, user_role) VALUES (?, ?, ?)',
                        (username, hashed_password, "user"))
            conn.commit()
            session.clear()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('auth/register.html', error='Логин уже занят')
        conn.close()
        
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(" " in password):
            return render_template('auth/login.html', error = "Неверный пароль")


        conn = get_db_connection()
        user = conn.execute('SELECT * FROM userlist WHERE user_login = ?', (username,)).fetchone()
        conn.close()
        if user is None:
            return render_template('auth/login.html', error='Неверный логин')
        if (user and check_password_hash(user['user_password'], password)):
            session.clear()
            session['req_inv'] = user['user_request_inv']
            session['user_id'] = user['user_id']
            session['user_role'] = user['user_role']
            session['user_login'] = user['user_login']
            return redirect(url_for('blank'))
        return render_template('auth/login.html', error='Неверный пароль или логин')
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    # session.pop('username', None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/blank')
def blank():
    if 'user_login' in session:
        username = session['user_login']
        return render_template('Blank1.html', username=username, isadmin = IsAdmin1())
    return redirect(url_for('login'))

def RecordsInv():
    conn = get_db_connection()
    try:
        recs = conn.cursor().execute(
            "SELECT * FROM inventory;"
        ).fetchall()[0]
        print(recs, "recs")
        return recs
    except IndexError:
        print("Empty list")
    conn.close()
    

def IsAdmin1(session = session, 
            key = "user_role",
            value = "admin"):
    try:
        if(session[key] == value):
            isadmin = True
        else:
            isadmin = False
    except:
        return redirect(url_for("login"))
    return isadmin 

@app.route("/view", methods = ["GET"])
def view():
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows, "inv rows")
    """
    print(rows)
    if request.method == "POST":
        try:
            titles = []
            for i in range(1, rows + 1):
                c = conn.execute(
                "SELECT * FROM inventory WHERE item_id = ?;",
                    (i,)).fetchone()
                titles.append(c)
                    
            for t in titles:
                Cond = request.form[titles[t]]
                conn.execute(
                "INSERT INTO inventory (item_cond) VALUES (?);",
                (Cond,))
            conn.commit()
        except:
            pass
    """

    urows = conn.cursor().execute(  
        "SELECT COUNT(*) FROM userlist;"
    ).fetchone()[0]
    items = []
    # for i in range(1, rows):    
    record = conn.cursor().execute(
        "SELECT * FROM inventory ORDER BY item_title ASC;"
    ).fetchall()
    items = record
        # if record != None:
        #     items.append(record)
        # print(items)
    tobuy = conn.execute(
            "SELECT * FROM tobuylist ORDER BY buy_title ASC"
        ).fetchall()
    if (IsAdmin1()): # For ADMIN
        usersall = conn.execute(
            "SELECT * FROM userlist;",
        ).fetchall()
        users = []
        for u in usersall:
            if (u["user_request_inv"] != None):
                req = str.split(u["user_request_inv"], sep=" ")
                users.append([req[0], req[1],   u["user_login"], u['user_id'], req[2]])
                #            inv ID   status ID user_login       user_id       nnum
                # nnum (user request number of items)
                print(req, "rec")
        
    else: # For USER
        print(session['user_login'])
        req = conn.execute(
            "SELECT user_request_inv FROM userlist WHERE user_login = ?;",
            (session['user_login'],)
        ).fetchone()[0]
        if (req != None):
            print(req, "- - req")
            req = str.split(req, sep= " ")
            invid = int(req[0])
            # invid = 4
            statusid = {"1": "Отправлена",
                "2": "Одобрена",
                "3": "Отклонена",
                "4": "Недопустимое количество"}
            print(req, "- - req")
            status = statusid[req[1]]
            # status = statusid["4"]
            num = int(req[2])
            users = {"invid": invid, "status": status, "num": num}
        else:
            users = {"invid": None, "status": "неизвестно"}
        print(req, users, "- - req users")
    # items = []
    print(items, "items")
    conn.close()
    print(users, "users")
    RecordsInv()
    return render_template("view.html", isadmin = IsAdmin1(),
        items = items, users = users, tobuy = tobuy,
        session = session)

@app.route("/view/new", methods = ["GET", "POST"])
def viewnew():
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows)
    
    if request.method == "POST" and (session["user_role"] == "admin"):
        try:
            title = request.form['title']
            Number = request.form['Number']
            conn.execute(
        "INSERT INTO inventory (item_title, item_number, item_cond, item_req) VALUES (?, ?, ?, ?)",
            (title, Number, "новый", "---",)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.execute(
            "UPDATE inventory SET item_number = ?, item_cond = ?, item_req = ? WHERE item_title = ?",
            (Number, "новый", "---", title,)
            )
            conn.commit()
    conn.close()
    RecordsInv()
    return redirect(url_for('view'))

@app.route("/view/cond/<id>", methods = ["GET", "POST"])
def viewcond(id):
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows)
    
    if request.method == "POST" and (session["user_role"] == "admin"):
        try:
            title = conn.cursor().execute(
            "SELECT item_title FROM inventory WHERE item_id = ?;",
            (id,)).fetchone()[0]
            # print(title)
            cond = request.form[title]
            conn.execute(
            "UPDATE inventory SET item_cond = ? WHERE item_id = ?",
            (cond, id,)
            )
            conn.commit()
        except:
            print("cond error")
    conn.close()
    RecordsInv()
    return redirect(url_for('view',isadmin = IsAdmin1()))

@app.route("/view/item/<id>",methods = ["GET", "POST"])
def viewitem(id):
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows)
    
    if request.method == "POST" and (session["user_role"] == "admin"):
        # try:
            title = conn.cursor().execute(
            "SELECT item_title FROM inventory WHERE item_id = ?;",
            (id,)).fetchone()[0]
            # print(title)
            newtitle = request.form[title]
            Number = request.form[f"num{id}"]
            conn.execute(
            "UPDATE inventory SET item_title = ?, item_number = ? WHERE item_id = ?",
            (newtitle, Number, id,)
            )
            conn.commit()
        # except:
            # print("item update error")
    conn.close()
    RecordsInv()
    return redirect(url_for('view',isadmin = IsAdmin1()))

@app.route("/view/use/<id>",methods = ["GET", "POST"])
def viewuse(id):
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows)
    
    if request.method == "POST" and (session["user_role"] == "admin"):
        try:
            newuser = request.form[f"use{id}"]
            conn.execute(
            "UPDATE inventory SET item_req = ? WHERE item_id = ?" ,
            (newuser, id,)
            )
            conn.commit()
        except:
            print("item user error")
    conn.close()
    RecordsInv()
    return redirect(url_for('view',isadmin = IsAdmin1()))

@app.route("/view/del/",methods = ["GET", "POST"])
def viewdelete():
    conn = get_db_connection()
    if request.method == "POST" and (session["user_role"] == "admin"):
        # for i in range(10):
            conn.execute(
                "DELETE FROM inventory",
            # (i,)
            )
            conn.commit()
    conn.close()
    RecordsInv()
    return redirect(url_for('view'))

@app.route("/view/del/<id>",methods = ["GET", "POST"])
def viewdel(id):
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows)
    

    if request.method == "POST" and (session["user_role"] == "admin"):
        try:
            user = conn.cursor().execute(
            "SELECT item_req FROM inventory WHERE item_id = ?",
            (id,)
            ).fetchone()[0]
            print(user)
            if(user == "---" or user == None):
                conn.execute(
                    "DELETE FROM inventory WHERE item_id = ?",
                    (id,)
                )
                conn.commit()
            elif(user != None):
                conn.execute(
                    "UPDATE inventory SET item_req = ? WHERE item_id = ?",
                    ("---", id,)
                )
                conn.commit()
        except:
            print("item delete error")
    conn.close()
    RecordsInv()
    return redirect(url_for('view',isadmin = IsAdmin1()))

@app.route("/view/reqnew/<id>", methods = ["GET", "POST"])
def viewuseritemreq(id):
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows)
    if request.method == "POST":
        # try:
            user = session['user_login']
            nnum = int(request.form[f'nnum{id}'])
            print(nnum)
            print(user)
            invnum = int(conn.cursor().execute(
                "SELECT item_number FROM inventory WHERE item_id = ?",
                (id,)
            ).fetchone()[0])
            print(invnum, "NUM on SKLAD")
            if(nnum > invnum or nnum <= 0):
                error = "Недопустимое количество"
                reqinvOld = conn.execute(
                    "SELECT user_request_inv FROM userlist WHERE user_login = ?",
                    (user,)
                ).fetchone()[0]
                if(reqinvOld != None):
                    reqinvOld = str.split(reqinvOld, sep=" ")
                    reqinvOld[1] = "4"
                    newInvReq = ""
                    for i in reqinvOld:
                        newInvReq += i + " "
                    conn.execute(
                        "UPDATE userlist SET user_request_inv = ?",
                        (newInvReq,))
                    conn.commit()
                else:
                    conn.execute(
                    "UPDATE userlist SET user_request_inv = ? WHERE user_login = ?",
                    (f"{id} 4 {nnum}", user,)
                    ).connection.commit()
                return redirect(url_for("view"))
                # return None
            elif(nnum <= invnum):
                conn.execute(
                    "UPDATE userlist SET user_request_inv = ? WHERE user_login = ?",
                    (f"{id} 1 {nnum}", user,)
                )
            conn.commit()
        # except:
        #     print("item user request error")
    conn.close()
    RecordsInv()
    return redirect(url_for('view',isadmin = IsAdmin1()))

@app.route("/view/req/<iuid>", methods = ["GET", "POST"])
def viewreq(iuid):
    conn = get_db_connection()
    rows = conn.cursor().execute(
        "SELECT COUNT(*) FROM inventory;"
    ).fetchone()[0]
    # print(rows)
    if request.method == "POST" and (session['user_role'] == "admin"):
        # try:
            
            iuid = str(iuid).split(sep="u")
            itemid = iuid[0]
            userid = iuid[1]
            move = request.form[f'accept{itemid}']
            reqinv = conn.cursor().execute(
                "SELECT user_request_inv FROM userlist WHERE user_id = ?",
                (userid,)
            ).fetchone()[0]
            reqinv = str.split(reqinv, sep=" ")
            nnum = reqinv[2]
            username = conn.cursor().execute(
                "SELECT user_login FROM userlist WHERE user_id = ?;",
                (userid,)
            ).fetchone()[0]
            
            print(userid, move)
            
            if(move == "Одобрить"):
                item = conn.execute(
                "SELECT * FROM inventory WHERE item_id = ?",
                (int(itemid),)
                ).fetchone()
                itemNum = item['item_number']
                if(itemNum == int(nnum)):
                    conn.execute(
                            "UPDATE inventory SET item_req = ?",
                            (username,)
                        )
                    conn.commit()
                else:
                    newnum = itemNum - int(nnum)
                    conn.execute(
                        "UPDATE inventory SET item_number = ?",
                        (newnum,)
                    )
                    conn.execute(
                    "INSERT INTO inventory (item_title, item_number, item_cond, item_req) VALUES (?, ?, ?, ?)",
                    (item['item_title'], int(nnum), "новый", username,)
                    )
                    conn.commit()
                move = "2"
            elif(move == "Отклонить"):
                move = "3"
            else:
                pass
            conn.execute(
                "UPDATE userlist SET user_request_inv = ? WHERE user_id = ?",
                (f"{itemid} {move} {nnum}", userid,)
            )
            conn.commit()
            print("done")
        # except:
        #     print("item user request accepting error")
    conn.close()
    RecordsInv()
    return redirect(url_for('view',isadmin = IsAdmin1()))

@app.route("/view/tobuy/", methods = ["GET", "POST"])
def viewtobuynew():
    conn = get_db_connection()
    if request.method == "POST" and (session["user_role"] == "admin"):
        title = request.form['title']
        cost = request.form['cost']
        seller = request.form['from']
        try:
            conn.execute(
                "INSERT INTO tobuylist (buy_title, buy_cost, buy_from, buy_cond) VALUES (?, ?, ?, ?)",
                (title, cost, seller, "ожидание", )
            )
            conn.commit()
        except :
            conn.close()
            error = "Этот предмет уже есть в списке покупок"
            return render_template("Blank1.html", username=session['user_login'], error = error)

    conn.close()
    return redirect(url_for("view"))

@app.route("/view/buydel/<id>", methods = ["GET", "POST"])
def viewbuydel(id):
    conn = get_db_connection()
    if(request.method == "POST" and session['user_role'] == "admin"):
        value = request.form[f"bdel{id}"]
        if(value == "Удалить"):
            conn.execute(
                "DELETE FROM tobuylist WHERE buy_id = ?",
                (id,)
            ).connection.commit()
    conn.close()
    
    return redirect(url_for("view"))

@app.route("/blank/log", methods = ["GET"])
def blanklog():
    conn = get_db_connection()
    if (session['user_role'] == "admin"):
        items = conn.cursor().execute(
        "SELECT * FROM inventory ORDER BY item_title ASC;"
        ).fetchall()
        log = "Отчёт:\n"

        num = str(len(items))[-1]
        if(num in ["0", "5", "6", "7", "8","9"]):
            end = "предметов"
        elif(num in ["2", "3", "4"]):
            end = "предмета"
        elif(num == "1"):
            end = "предмет"
        
        log += f"На складе {len(items)} {end}.\n"
        for i in items:
            log += f"{i['item_id']}. {i['item_title']} в количестве {i['item_number']}"
            if(i['item_req'] != "---"):
                log += f", владелец: {i['item_req']}"
            else:
                log += f", владелец отсутствует"
            log += f", состояние: {i['item_cond']}.\n"
        log += "Конец отчёта."

    user = session['user_login']
    conn.close()
    return render_template("Blank1.html", username=user, log=log,
    isadmin=IsAdmin1())

# host='10.145.87.72'
# port = 3306
# flask --app app run --host="" --port=3306 --debug

if __name__ == '__main__':

    app.run(host = "", port = 3306, debug = True)




"""
try:
            title = request.form['title']
            Number = request.form['Number']
            conn.execute(
            "INSERT INTO inventory (item_title, item_number) VALUES (?, ?)",
            (title, Number,)
        )
        conn.commit()
        except:
            pass
"""

