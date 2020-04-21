from flask import *
from db import *

app = Flask(__name__)

logged_in = False
sql = []



@app.route('/')
def index():
    return app.send_static_file('login.html')



@app.route('/login')
def login():
    global logged_in
    eml = request.args.get("eml")
    pwd = request.args.get("pwd")

    sql = '''SELECT Email from Users WHERE Email = ? and Password = ?'''

    stored_data = query_value(sql, args=(eml,pwd))
    if stored_data is not None:
        logged_in = True
        return "True"


    else:
        return "Login information is incorrect"


@app.route('/oil_search')
def oil_search1():
   return app.send_static_file('oil_search.html')


@app.route('/home1')
def home1():
    return app.send_static_file('home1.html')

@app.route('/oil_search')
def oil_search():
    global sql
    if True:#logged_in:          #temporary
        oil1 = request.args.get("oil1")
        oil2 = request.args.get("oil2")
        oil3 = request.args.get("oil3")


        sql = '''select Oil_name, Description, Oil_Benefits, 
              Oil_Uses from oils where Oil_name = ? or Oil_name = ? 
              or Oil_name = ?  '''


        stored_data = query(sql, args=(oil1,oil2,oil3))

        if stored_data is not None:
            pass

        else:
            return "No information found"



if __name__ == "__main__":
    app.run("127.0.0.1", 5000)


