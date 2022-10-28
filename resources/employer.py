from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user

from main import app
from . import login_manager, csrf

from models.user import UserModel
from models.employer import EmployerModel
from models.field import FieldModel
from models.jobs import JobModel
from models.application import ApplicationModel

from forms.employer import EmployerForm
from forms.job import JobForm


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id)) # Fetch the user from the database

@app.route('/user/employer/add/<int:id>', methods=['GET','POST'])
@login_required
def add_employer(id):
    form = EmployerForm()
    currentuser = current_user
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        new_employer = EmployerModel(name=name, description=description, user_id=currentuser.id)
        new_employer.insert_record()

        flash('Employer details have been added', 'success')
        return redirect(url_for('dashboard'))
    return render_template('admin/employer/add_employer.html', form=form)

@app.route('/user/employer/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_employer(id):
    form = EmployerForm()
    currentuser = current_user
    employer = EmployerModel.fetch_by_id(id)
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        EmployerModel.update(name=name, description=description)

        flash(f'Updated employer {name}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('admin/employer/edit_employer.html', employer=employer, form=form)

@app.route('/user/<int:id>/employer')
@login_required
def employer_detail(id):
    form = EmployerForm()
    employer = EmployerModel.fetch_by_user_id(user_id=id)
    
    return render_template('admin/employer/employer.html', employer=employer, form=form)

@app.route('/employer/post/job', methods=['GET', 'POST'])
@login_required
def post_job():
    form = JobForm()

    currentuser = current_user
    user_id = currentuser.id
    employer = EmployerModel.fetch_by_user_id(user_id=user_id)

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        qualifications = form.qualifications.data
        field_id = form.field.data
        employer_id = employer.id

        new_job = JobModel(name=name, description=description, qualifications=qualifications, field_id=field_id, employer_id=employer_id)
        new_job.insert_record()

        flash(f'Added job: {name}', 'success')
        return redirect(url_for('jobs'))
    return render_template('admin/jobs/add_job.html', form=form)

@app.route('/employer/edit/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    fields = FieldModel.fetch_all()
    job = JobModel.fetch_by_id(id)
    currentuser = current_user
    user_id = currentuser.id
    employer = EmployerModel.fetch_by_user_id(user_id=user_id)

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        qualifications = form.qualifications.data
        field_id = form.field.data
        employer_id = employer.id

        JobModel.update(id=id, name=name, description=description, qualifications=qualifications, field_id=field_id)

        flash(f'Updated job: {name}', 'success')
        return redirect(url_for('jobs'))
    return render_template('admin/jobs/edit_job.html', job=job, form=form, fields=fields)


@app.route('/<int:id>/employer/jobs/', methods=['GET', 'POST'])
@login_required
def employer_jobs(id):
    employer = EmployerModel.fetch_by_user_id(user_id=id)
    jobs = JobModel.fetch_by_employer(employer_id=employer.id)
    return render_template('admin/jobs/jobs_by_employer.html', jobs=jobs)

@app.route('/job/applications/<int:id>')
@login_required
def view_applications(id):
    applications = ApplicationModel.fetch_by_job(job_id=id)
    job = JobModel.fetch_by_id(id)

    return render_template('admin/jobs/job_applications.html', applications=applications, job=job)
