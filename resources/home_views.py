from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from forms.auth import LogInForm

from . import login_manager, csrf
from main import app

from models.user import UserModel
from models.jobs import JobModel
# from forms.contact import ContactForm

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    currentuser = current_user
    page_num = 1
    if request.args:
        page_num:int = request.args.get('page_num')
    jobs = JobModel.fetch_paginated(page_num=int(page_num))
    return render_template('jobs/jobs.html', jobs=jobs, currentuser=currentuser)

@app.route('/jobs/<int:id>')
def job_detail(id):
    currentuser = current_user
    job = JobModel.fetch_by_id(id=id)
    form = LogInForm()
    # user = UserModel.fetch_by_email(email=form.email.data)
    if currentuser.is_authenticated:
        session['logged_in'] = True
        # session['name'] = UserModelStaff.fetch_by_email(email).first_name
        # session['role'] = Staff.fetch_by_email(email).roles.name
        # session['staff_id'] = Staff.fetch_by_email(email).id
        print('================================================')
        print(currentuser.is_authenticated)
        print('================================================')
    return render_template('jobs/job.html', job=job, currentuser = currentuser)

@app.route('/elements')
def elements():
    return render_template('elements.html')