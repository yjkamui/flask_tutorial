from flask import Blueprint, render_template,url_for,request,redirect,flash
from flask_login import login_user,logout_user,login_required, current_user
from . import db
from .models import User,Task
from .forms import RegistrationForm,LoginForm,TaskForm
from werkzeug.security import check_password_hash, generate_password_hash

index_bp=Blueprint('index',__name__,url_prefix='/')
auth_bp=Blueprint('auth',__name__,url_prefix='/auth')
task_bp=Blueprint('task',__name__,url_prefix='/task')

@index_bp.route('/',methods=['GET','POST'])
@index_bp.route('/index', methods=['GET','POST'])
@login_required
def index():
    form=TaskForm()
    if form.validate_on_submit():
        task=Task(taskname=form.taskname.data,due_date=form.due_date.data)
        db.session.add(task)
        db.session.commit()

        flash('Task was added.','success')
        return redirect(url_for('index.index'))
    tasks=Task.query.all()
    return render_template('index.html',form=form,tasks=tasks)


@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            flash('User already exists','error')
        else:
            if form.password1.data==form.password2.data:
                password=generate_password_hash(form.password1.data)
                user=User(username=form.username.data,password=password)
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created','success')
                return redirect(url_for('auth.login'))
            else:
                flash('Registration failed. Passwords did not match.','error')
    return render_template('register.html',form=form)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('Login has been succeeded.','success')
            return redirect(url_for('index.index'))
        else:
            flash('Login failed.Please check username and password.','error')
    return render_template('login.html',form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@task_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted.', 'success')
    return redirect(url_for('index.index'))




















