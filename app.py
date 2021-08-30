from flask import Blueprint, Flask, render_template, redirect, flash, url_for, session, jsonify
from flask_mysqldb import MySQL, MySQLdb
from datetime import datetime
# from Daily_runs import func,func_2
# import glob

from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan"

# mysql configuration
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "traffic_ai"
mysql = MySQL(app)
# end mysql configuration

uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) 

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --------------------------------------uploading image to detect---------------------------------------
@app.route("/index0",methods=['GET','POST'])
def detect_algo():
    return render_template('index0.html')
# --------------------------------------end of uploading image to detect----------------------------------

 

#  -----------------------------------show image on page--------------------------------------------
# @app.route('/detect/<filename>')
# def display_image(filename):
#     #print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)
# ------------------------------------end show image on page----------------------------------------

#------------------------------------ testing upload all input and output images to page------------------------------
@app.route("/detect")
def uploader():
        path = 'static/uploads/'
        uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))        # Sorting as per image upload date and time
        print(uploads)
        #uploads = os.listdir('static/uploads')
        uploads = ['uploads/' + file for file in uploads]
        uploads.reverse()
        return render_template("detect.html",uploads=uploads) 

@app.route("/displayOutput")
def display_output():
        path = 'static/output_images/'
        uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))        # Sorting as per image upload date and time
        print(uploads)
        #uploads = os.listdir('static/uploads')
        uploads = ['output_images/' + file for file in uploads]
        uploads.reverse()
        return render_template("displayOutput.html",uploads=uploads) 
# -------------------------------------end of testing-----------------------------------------------
# @app.route('/')
# @app.route('/index')
# # @app.route('/detect')
# def show_index():
#     full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sample2.jpg')
#     return render_template("detect.html", user_image = full_filename)

# @app.route('/')
# @app.route('/index')
# def home():
#  image_names = os.listdir('static/uploads')
#  render_template('detect.html', image_name=image_names)


# -------------------------------------loadResources-------------------------------------------------
@app.route("/loadResource",methods=["POST","GET"])
# @app.route("/upload",methods=["POST","GET"])
def upload():
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
# -----------------------------------------end loadResources----------------------------------------

# -------------------------------------------fetch data to table-------------------------------------------

# @app.route('/projectlist',methods=['GET','POST'])
@app.route('/basic-table',methods=['GET','POST'])
def projectlist():
    #creating variable for connection
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #executing query
    cursor.execute("select * from uploads")
    #fetching all records from database
    data=cursor.fetchall()
    #returning back to projectlist.html with all records from MySQL which are stored in variable data
    return render_template("basic-table.html",data=data)

#--------------------------------------------- end fetch data to table----------------------------------------
# ----------------------------------------------display image on html page----------------------------------------------------------
# import os
# @app.route('/hello', methods=['POST'])
# def hello():
#    path = request.form['path']
#    func(path)
#    func_2()
#    image = [i for i in os.listdir('static/output_images') if i.endswith('.jpg')][0]
#    return render_template('detect.html', user_image = image)
# ----------------------------------------------end display image on html page------------------------------------------------------

# ----------------img upload----------------------------
# @app.route('/',methods=["POST","GET"])
# def index():
#     return render_template('index.html')

# @app.route("/upload",methods=["POST","GET"])
# def upload():
#     cursor = mysql.connection.cursor()
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     now = datetime.now()
#     if request.method == 'POST':
#         files = request.files.getlist('files[]')
#         #print(files)
#         for file in files:
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 cur.execute("INSERT INTO images (file_name, uploaded_on) VALUES (%s, %s)",[filename, now])
#                 mysql.connection.commit()
#             print(file)
#         cur.close()   
#         flash('File(s) successfully uploaded') 
#         return redirect(url_for('upload'),200)   
#     return redirect('/')
#-------------------end img upload-----------------------------
 
#----------- original index page-------------------
@app.route("/",methods=['GET','POST'])
def hello_world():
    return render_template('index.html')

    # if request.method =='POST':
    #     username = request.form['username']
    #     email =request.form['email']

    #     cur = mysql.connection.cursor()
    #     cur.execute("INSERT INTO users (name,email)VALUES (%s,%s)",(username,email))

    #     mysql.connection.commit()
    #     cur.close()

    #     return "success"
    # return render_template('index.html')
#--------------------- end original index-------------------------


#------------------------ upload resources--------------------------------

# @app.route("/loadResource",methods=['GET','POST'])
# def load_resource():
#     if request.method == 'POST':
#         area = request.form['area']
#         roundabout = request.form['roundabout']
#         camcode = request.form['camcode']
#         image = request.form['image']

#         cur = mysql.connection.cursor()

#         cur.execute("INSERT INTO lights (Resource_name,Area_name,Roundabout,Camera_code) VALUES (%s,%s,%s,%s)",(area,roundabout,camcode,image))

#         mysql.connection.commit()

#         cur.close()

#         return "success"

#     return render_template("loadResource.html")

#--------------------end upload resources----------------------- 


@app.route("/basic-table")
def basic_table():
    return render_template("basic-table.html")




@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
    subprocess.run("dir",shell=True)
    subprocess.run(['python', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename))],shell=True)

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    obj = os.path.join(uploads_dir, secure_filename(video.filename))
    # obj = secure_filename(video.filename)
    return obj

@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    loc = os.path.join("runs/detect", obj)
    print(loc)
    try:
        return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
        # return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)

@app.route('/display/<filename>')
def display_video(filename):
	print('display_video filename: ' + filename)
	return redirect(url_for('static/video_1.mp4', code=200))
