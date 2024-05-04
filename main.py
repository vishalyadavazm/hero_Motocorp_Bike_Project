import os

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='vishal'
app.config['MYSQL_DB'] = 'projectTask'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/upload")
def fileupload():
    return render_template("file_upload.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sing_up.html")

@app.route("/service")
def service():
    return render_template("serviccePage.html")


@app.route('/login_validation', methods=['POST'])
def login_validation():
    password = request.form.get('password')
    name = request.form.get('name')

    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE name = %s AND password = %s"
    cursor.execute(query, (name, password))

    user = cursor.fetchone()
    cursor.close()

    if user:
        return render_template("home.html")
    else:
        return render_template("login.html",error="Wrong name/ password")


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    mobile = request.form['mobile']

    cursor = mysql.connection.cursor()
    query = "INSERT INTO users (name, password, email, mobile) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, password, email, mobile))
    mysql.connection.commit()
    cursor.close()
    return render_template("login.html")



@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form['name'],
    city = request.form['city'],
    mobile = request.form['mobile'],
    bikesModel = request.form['bikesModel']
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = file.filename
        file_extension = os.path.splitext(filename)[1]
        file_content = file.read()


        cursor = mysql.connection.cursor()
        query = ("INSERT INTO service_requests (name, mobile, city, bike_model, filename, file_extension) VALUES (%s, %s, %s,%s,"
                 "%s,%s)")
        cursor.execute(query, (name, mobile, city, bikesModel,filename, file_extension))
        mysql.connection.commit()
        cursor.close()

        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
