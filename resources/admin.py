from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required


from . import login_manager, csrf
from main import app

from models.user import UserModel
from models.user_role import UserRoleModel
from models.field import FieldModel
from models.employer import EmployerModel
from models.provider import ProviderModel
from models.jobs import JobModel
from forms.auth import RegisterForm
from forms.job import FieldForm

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

@app.route('/dashboard')
@login_required
def dashboard():
    form = RegisterForm() 
    currentuser = current_user
    user = UserModel.fetch_by_id(id=currentuser.id)
    user_roles = UserRoleModel.fetch_by_user_id(user_id=user.id)
    role = user_roles.role.role
    is_admin = False
    is_employer = False
    is_provider = False
    if role == 'Super Admin' or role == 'Admin':
        is_admin = True
    if role == 'Employer':
        is_employer = True
    if role == 'Provider':
        is_provider = True

    return render_template('admin/dashboard.html', is_employer=is_employer, is_provider=is_provider, is_admin=is_admin, form=form, user=user, currentuser=currentuser)

@app.route('/admin/users')
@login_required
def get_users():
    users = UserModel.fetch_all()
    return render_template('admin/users/users.html', users=users)

@app.route('/user/account/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    form = RegisterForm()
    user_id = current_user.id
    user= current_user
    if form.validate_on_submit():
        if id != user_id:
            flash('You cannot modify another user!', 'danger')

        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']

        UserModel.update(id=id, full_name=full_name, phone=phone, email=email)
        flash(f'{full_name} has been updated', 'success')

        return(redirect(url_for('dashboard')))
    return render_template('admin/users/edit_user.html', user=user, form=form)

@app.route('/user/account/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user_id = current_user.id
    if id != user_id:
        flash('You cannot modify another user!', 'danger')

    user = UserModel.fetch_by_id(id)
    full_name = user.full_name

    UserModel.delete_by_id(id)
    flash(f'{full_name} has been updated', 'success')

    return(redirect(url_for('index')))

@app.route('/admin/employers')
@login_required
def get_employers():
    currentuser = current_user
    employers = EmployerModel.fetch_all()
    return render_template('admin/employer/employers.html', employers=employers)
    

@app.route('/admin/providers')
@login_required
def get_providers():
    currentuser = current_user
    providers = ProviderModel.fetch_all()
    return render_template('admin/provider/providers.html', providers=providers)

@app.route('/admin/fields')
@login_required
def fields():
    fields = FieldModel.fetch_all()
    return render_template('admin/fields/fields.html', fields=fields)


@app.route('/fields/add', methods=['GET', 'POST'])
@login_required
def add_field():
    form = FieldForm()
    if form.validate_on_submit():
        name = form.name.data
        new_field = FieldModel(name=name)
        new_field.insert_record()
        flash(f'Field {name} added', 'success')
        return redirect(url_for('fields'))
    return render_template('admin/fields/add_field.html', form=form)

@app.route('/fields/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_field(id):
    form = FieldForm()
    field = FieldModel.fetch_by_id(id)
    if form.validate_on_submit():
        name = form.name.data
        FieldModel.update(id=id, name=name)
        flash(f'Field {name} updated', 'success')
        return redirect(url_for('fields'))
    return render_template('admin/fields/edit_field.html', field=field, form=form)