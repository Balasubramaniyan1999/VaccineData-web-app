from flask import Flask,redirect,render_template,url_for,request,session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'data'

#database connection
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="covid"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)




#loginpage
@app.route('/',methods = ['POST','GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        con = mysql.connection.cursor()
        con.execute('select * from useraccounts where username = %s and password = %s',(username,password))
        account = con.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for("home"))
        else:
            print("Incorrect username and password")
    return render_template('login.html')

#logout
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

#register
@app.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        con = mysql.connection.cursor()
        sql = "insert into useraccounts(username,password) value (%s,%s)"
        con.execute(sql,[username,password])
        mysql.connection.commit()
        con.close()
    return render_template('register.html')

#loading home page
@app.route("/home")
def home():
    return render_template("home.html")

#view data
@app.route("/view")
def view():
    con = mysql.connection.cursor()
    sql = "select * from userdata"
    con.execute(sql)
    res = con.fetchall()
    return render_template("view.html",data = res)

#add user
@app.route("/adduser",methods = ['POST','GET'])
def addUser():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        vaccinename = request.form['vaccinename']
        con = mysql.connection.cursor()
        sql = "insert into userdata(name,age,vaccinename) value (%s,%s,%s)"
        con.execute(sql,[name,age,vaccinename])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template("addUser.html")


#Delete User
@app.route("/deleteuser",methods = ['GET','POST'])
def deleteUser():
    if request.method == 'POST':
        id = request.form['id']
        con = mysql.connection.cursor()
        sql = "delete from userdata where id = {}".format(id)
        con.execute(sql)
        mysql.connection.commit()
        con.close()
        return redirect(url_for("view"))
    return render_template("delete.html")

    
if __name__ == '__main__':
    app.run(debug=True)