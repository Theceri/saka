from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user

from . import  login_manager, csrf
from main import app

from models.user import UserModel
from models.field import FieldModel
from models.provider import ProviderModel
from models.skill import SkillModel
from models.jobs import JobModel
from models.application import ApplicationModel

from forms.provider import ProviderForm, SkillForm


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

@app.route('/apply/job/<int:id>')
@login_required
def apply(id):
    currentuser = current_user
    print('======================================================')
    print(currentuser.id)
    print('======================================================')
    provider = ProviderModel.fetch_by_user_id(user_id=currentuser.id)
    print('======================================================')
    print(provider)
    print('======================================================')
    job = JobModel.fetch_by_id(id)
    print('======================================================')
    print(job.id)
    print('======================================================')
    new_application = ApplicationModel(provider_id=provider.id, job_id=job.id)
    new_application.insert_record()
    print(provider.id)
    print(job.id)
    flash(f'Applied for {job.name}', 'success')
    return redirect(url_for('jobs'))

@app.route('/user/<int:id>/applications/')
def provider_applications(id):
    provider = ProviderModel.fetch_by_user_id(user_id=id)
    applications = ApplicationModel.fetch_by_provider(provider_id=provider.id)
    return render_template('admin/provider/provider_applications.html', applications=applications)

@app.route('/applicant/<int:id>')
def applicant_detail(id):
    provider = ProviderModel.fetch_by_id(id)
    skills = SkillModel.fetch_by_provider(provider_id=provider.id)
    currentuser = current_user
    
    return render_template('admin/provider/provider.html', provider=provider, skills=skills, currentuser=currentuser)

@app.route('/applicant/select/application/<int:id>')
def select_applicant(id):
    application = ApplicationModel.fetch_by_id(id)
    ApplicationModel.select_applicant(id)
    return redirect(url_for('view_applications', id= application.id))


@app.route('/user/provider/add', methods=['GET','POST'])
@login_required
def add_provider():
    form = ProviderForm()
    currentuser = current_user
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        field = form.field.data
        new_provider = ProviderModel(name=name, description=description, field_id=int(field), user_id=currentuser.id)
        new_provider.insert_record()

        flash(f'Added {name}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('admin/provider/add_provider.html', form=form)

@app.route('/user/provider/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_provider(id):
    form = ProviderForm()
    provider = ProviderModel.fetch_by_id(id)
    fields = FieldModel.fetch_all()
    currentuser = current_user
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        field = form.field.data
        ProviderModel.update(id=id, name=name, description=description, field_id=int(field))

        flash(f'Edited {name}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('admin/provider/edit_provider.html', form=form, provider=provider, fields=fields)

@app.route('/user/<int:id>/provider')
@login_required
def provider_detail(id):
    provider = ProviderModel.fetch_by_user_id(user_id=id)
    skills = SkillModel.fetch_by_provider(provider_id=provider.id)
    currentuser = current_user
    
    return render_template('admin/provider/provider.html', provider=provider, skills=skills, currentuser=currentuser)

@app.route('/skills/add', methods=['GET','POST'])
def add_skills():
    form = SkillForm()
    currentuser = current_user
    provider = ProviderModel.fetch_by_user_id(user_id=currentuser.id)
    if form.validate_on_submit():
        skills = form.skills.data
        skill_list = skills.split(',')
        for skill in skill_list:
            new_skill = SkillModel(name=skill.title(), provider_id=provider.id)
            new_skill.insert_record()
        flash('Skills added', 'success')
        return redirect(url_for('provider_detail', id=provider.user_id))
    return render_template('admin/provider/skills/add_skill.html', form=form)
