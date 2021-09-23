# project/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint
from flask_login import login_required


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/')
@login_required
def home():
    # return render_template('main/index.html')
    return render_template('main/dashboard.html')


@main_blueprint.route('/register')
@login_required
def register():
    # return render_template('main/index.html')
    return render_template('main/register.html')



@main_blueprint.route('/login')
@login_required
def login():
    # return render_template('main/index.html')
    return render_template('main/login.html')


@main_blueprint.route('/profile')
@login_required
def profile():
    # return render_template('main/index.html')
    return render_template('main/profile.html')


@main_blueprint.route('/loadResource')
@login_required
def upload():
    # return render_template('main/index.html')
    return render_template('main/loadResource.html')


@main_blueprint.route('/basic-table')
@login_required
def projectlist():
    # return render_template('main/index.html')
    return render_template('main/basic-table.html')


@main_blueprint.route('/imgdetection')
@login_required
def detect_algo():
    # return render_template('main/index.html')
    return render_template('main/imgdetection.html')


@main_blueprint.route('/detect')
@login_required
def detect():
    # return render_template('main/index.html')
    return render_template('main/index.html')


@main_blueprint.route('/display_output')
@login_required
def display_output():
    # return render_template('main/index.html')
    return render_template('main/display_output.html')


@main_blueprint.route('/logout')
@login_required
def logout():
    # return render_template('main/index.html')
    return render_template('main/login.html')
