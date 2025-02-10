
import sqlite3
# from app import DATABASE, get_db_connection, init_db

DATABASE = "D:\\Prog1\\PredprofOL1\\Server\\database.db"

def Get_db(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

db = Get_db(DATABASE)

# def New_db():
#     init_db()

def db_exec(SQLcode):
    try:
        sel = db.executescript(SQLcode)
        db.close()
        return sel
    except:
        db.executescript(SQLcode)
        db.commit()
        db.close()

def db_JusExec(SQLcode):
    db.executescript(SQLcode)
    db.commit()
    db.close()

def db_execParam(SQLcode, _param):
    db.execute(SQLcode, _param)
    db.commit()
    db.close()

def db_seldcit(SQLcode, _param):
    sel = db.execute(SQLcode, _param)
    db.close()
    return sel

def db_exec_schema(Path):
    with open(Path) as sql:
        db.executescript(sql.read())
    db.commit()
    db.close()

def db_execParamIn():
    db_execParam(input("SQL code: "),
            input("param(space sliced): ").split(sep=" "))

def db_execIn():
    db_exec(input("SQL code: "))

def SelIn():
    sel = db_seldcit(input("SQL code: "),
            input("param(space sliced): ").split(sep=" "))
    return sel

# db_exec_schema("schemainv.sql")
# db_exec_schema("D:\\Prog1\\PredprofOL1\\Server\\schemainv.sql")
# user = db.execute(
#     "SELECT user_request_inv FROM userlist WHERE user_id = ?",
#     (1, )).fetchone()[0]
# print(user)
# # db.commit()
# db.close()
# print("db remote")


