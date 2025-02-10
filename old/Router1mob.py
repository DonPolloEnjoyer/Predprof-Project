
"Server router, uses settings from Conf1.py "

from flask  import Flask
import flask as fk


app = Flask(__name__)


@app.route("/index1")
def index1():
    # return f'test your var: {doom}'
    # return 'Hell doom%s' % doom
    return fk.render_template("index1.html")

@app.route("/index2") #, methods = ['POST'])
def index2():
    return fk.render_template("index2.html")

@app.route("/index3")
def index3():
    return fk.render_template("index3.html")

@app.route("/blank")
def blankpage1():
    return fk.render_template("Blank1.html")

"""this host="192.168.1.24",port=3306,debug=True"""
"""V6 host="2a00:1370:8184:1874:d46a:64bf:8a27:ce64",port=3306,debug=True"""
# configure launch settings

# ip = "192.168.1.24"
ip = "127.0.0.1"
Port = 3306
DebugE = True

def Rrun(Host: str, Port: int, Debug: bool):
    if (__name__ == "__main__"):
    
        app.run(host=Host, port=Port, debug=Debug, ssl_context=None)

Rrun(ip, Port, DebugE)


