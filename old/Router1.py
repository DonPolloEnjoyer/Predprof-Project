
"Server router, uses settings from Conf1.py "

from flask  import Flask

import flask_sqlalchemy as fSQL
import flask_migrate as fMig
import flask as fk

# from Conf1 import ip, Port, DebugE

app = Flask(__name__)

@app.route("/index1")
def Tohome1():
    return fk.redirect("/")

@app.route("/")
def index1():
    return fk.render_template("index1.html")

@app.route("/index2") #, methods = ['POST'])
def index2():
    return fk.render_template("auth/index2.html")

@app.route("/index3")
def index3():
    return fk.render_template("auth/index3.html")

@app.route("/blank")
def blankpage1():
    return fk.render_template("Blank1.html")

# this host="192.168.1.24",port=3306,debug=True
# V6 host="2a00:1370:8184:1874:d46a:64bf:8a27:ce64",debug=True
def Rrun(Host: str, Port: int, Debug: bool):
    if (__name__ == "__main__"):
    
        app.run(host=Host, port=Port, debug=Debug,)

# ip = "192.168.1.22"
ip = ''
Port = ''
DebugE = True

Rrun(ip, Port, DebugE)

# http://192.168.1.24:3306/index1


