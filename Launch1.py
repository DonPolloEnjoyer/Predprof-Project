
"Start the sever"


inner = open("app.py", 'r').read()
Router = compile(source=inner,filename="app.py",mode="exec")
exec(Router)

# del ip, Port, DebugE #, first1

