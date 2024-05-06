import csv
import os

from MySQLdb import IntegrityError
from flask import Flask, render_template, request, flash
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

@app.route("/csv_upload")
def csvUpalod():
    return render_template("file_csv_upload.html")
@app.route("/download")
def csvdownload():
    return render_template("download_service.html")
@app.route("/admin")
def admin():
    return render_template("admin.html")




@app.route('/login_validation', methods=['POST'])
def login_validation():
    password = request.form.get('password')
    email = request.form.get('email')
    print(password)
    print(email)
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))

    user = cursor.fetchone()

    cursor.close()

    if user:
        user_names = [user[0] for user in user]
        return render_template("home2.html",username=user[0])
    else:
        return render_template("login.html",error="Wrong name/ password")


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    mobile = request.form['mobile']

    try:
        cursor = mysql.connection.cursor()
        query = "INSERT INTO users (name, password, email, mobile) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, password, email, mobile))
        mysql.connection.commit()
        cursor.close()
        return render_template("login.html")
    except IntegrityError:
        #flash("Email address already exists. Please use a different email.")
        return render_template("sing_up.html",error="Email already exist")



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
        file_data = file.read()


        cursor = mysql.connection.cursor()
        query = ("INSERT INTO service_requests (name, mobile, city, bike_model, file_data, file_extension) VALUES (%s, %s, %s,%s,"
                 "%s,%s)")
        cursor.execute(query, (name, mobile, city, bikesModel,file_data, file_extension))
        mysql.connection.commit()
        cursor.close()

        return render_template("serviccePage.html",error="Submit Your Service request")
# Assuming max_length is the maximum length allowed for the mobile column
max_length = 15  # Example maximum length

@app.route("/csv_file", methods=['POST'])
def csvfile():
    if request.method == 'POST':
        csv_file = request.files['file']
        if csv_file:
            csv_data = csv.reader(csv_file.stream.read().decode('utf-8').splitlines())
            next(csv_data)  # Skip header if present
            cursor = mysql.connection.cursor()
            for row in csv_data:
                # Truncate mobile number if it exceeds max_length
                mobile = row[3][:max_length] if len(row[3]) > max_length else row[3]
                cursor.execute(
                    "INSERT INTO csv_upload (name, password, mobile,email) VALUES ( %s, %s, %s, %s)",
                    (row[0], row[1], row[2], mobile))

            mysql.connection.commit()
            cursor.close()
            return render_template("file_csv_upload.html",error="upload successfully")
    return 'File upload failed'

from flask import Response

@app.route("/download_service_requests_csv")
def download_service_requests_csv():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM service_requests")
    data = cursor.fetchall()
    cursor.close()

    # Create a CSV string
    csv_string = "id, name, mobile, city, bike_model,\n"
    for row in data:
        csv_string += f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n"  # Access tuple elements by index

    # Set response headers for CSV download
    headers = {
        "Content-Disposition": "attachment; filename=service_requests.csv",
        "Content-Type": "text/csv",
    }

    return Response(
        csv_string,
        status=200,
        headers=headers
    )




if __name__ == "__main__":
    app.run(debug=True)
