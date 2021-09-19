from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, flash, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime
from flask_mail import Mail, Message
import MySQLdb.cursors
import re
from werkzeug.utils import secure_filename, send_from_directory

import os
import subprocess

app = Flask(__name__)

app.config['SECRET_KEY']='6fa8b08a74314c132ed5632be1b8aed1'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'traffic_controller'

app.config.update(
            DEBUG=True,
            #email settings
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME='',
            MAIL_PASSWORD=''

            )

mail = Mail(app)

mysql = MySQL(app)


uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) 

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def hello_world():
    return render_template('index.html', title='Home')

@app.route("/home")
def home():
    return render_template('index0.html')

@app.route("/profilia")
def profilia():
    return render_template('profile0.html')

@app.route("/dashboard")
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dashboard.html', title='User Dashboard', username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', title='Register', msg=msg)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', title='Login', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        user = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', title='Profile', user=user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# -------------------------------------loadResources-------------------------------------------------
@app.route("/loadResource",methods=["POST","GET"])
# @app.route("/upload",methods=["POST","GET"])
def upload():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        cursor = mysql.connection.cursor()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        now = datetime.now()
        if request.method == 'POST':
            area = request.form['area']
            roundabout = request.form['roundabout']
            camcode = request.form['camcode']
            

            files = request.files.getlist('files[]')
            #print(files)
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    # cur.execute("INSERT INTO images (file_name, uploaded_on) VALUES (%s, %s)",[filename, now])
                    cur.execute("INSERT INTO uploads (file_name,area_name,roundabout,camera_code, uploaded_on) VALUES (%s,%s,%s,%s,%s)",(filename,area,roundabout,camcode,now))
                    mysql.connection.commit()
                print(file)
            cur.close()   
            flash('File(s) successfully uploaded') 
            # return redirect(url_for('upload'),200)   
        # return redirect('/loadResource')
        return render_template('loadResource.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
# -----------------------------------------end loadResources----------------------------------------

#------------------------------------ testing upload all input and output images to page------------------------------

@app.route("/detect")
def uploader():
    # Check if user is loggedin
    if 'loggedin' in session:
        path = 'static/uploads/'
        uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))        # Sorting as per image upload date and time
        print(uploads)
        #uploads = os.listdir('static/uploads')
        uploads = ['uploads/' + file for file in uploads]
        uploads.reverse()
        return render_template("detect.html",uploads=uploads) 
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/displayOutput")
def display_output():
    # Check if user is loggedin
    if 'loggedin' in session:
        path = 'static/output_images/'
        uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))        # Sorting as per image upload date and time
        print(uploads)
        #uploads = os.listdir('static/uploads')
        uploads = ['output_images/' + file for file in uploads]
        uploads.reverse()
        return render_template("displayOutput.html",uploads=uploads) 

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
# -------------------------------------end of testing-----------------------------------------------

# --------------------------------------uploading image to detect---------------------------------------
@app.route("/imgdetection",methods=['GET'])
def detect_algo():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('imgdetection.html')

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
# --------------------------------------end of uploading image to detect----------------------------------

# -------------------------------------------fetch data to table-------------------------------------------


@app.route('/basic-table',methods=['GET','POST'])
def projectlist():
    # Check if user is loggedin
    if 'loggedin' in session:
    # def basic_table():
        #creating variable for connection
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #executing query
        cursor.execute("select * from uploads")
        #fetching all records from database
        data=cursor.fetchall()
        #returning back to projectlist.html with all records from MySQL which are stored in variable data
        return render_template("basic-table.html",data=data)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#--------------------------------------------- end fetch data to table----------------------------------------

@app.route("/basic-table")
def basic_table():
    return render_template("basic-table.html")

@app.route("/detect", methods=['POST'])
def detect():
    # Check if user is loggedin
    if 'loggedin' in session:
        if not request.method == "POST":
            return
        video = request.files['video']
        video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
        print(video)
        subprocess.run("dir", shell=True)
        subprocess.run(['python', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename))],shell=True)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    obj = secure_filename(video.filename)
    return obj

@app.route('/return-files', methods=['GET'])
def return_file():
    # Check if user is loggedin
    if 'loggedin' in session:
        obj = request.args.get('obj')
        loc = os.path.join("runs/detect", obj)
        print(loc)
        try:
            return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
            # return send_from_directory(loc, obj)
        except Exception as e:
            return str(e)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('static/video_1.mp4', code=200))