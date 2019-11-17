from flask import Blueprint, redirect, render_template, request, flash, session

from database import base
from database.base import User
from forms import UserForm, LoginForm
from flask_login import login_required, login_user, logout_user, current_user


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/check_registration')
@login_required
def _user():
    q = base.db_session.query(User).filter(User.email == current_user.email)
    user = q.first()
    return render_template("my_page.html", user=user)


def login_process(form):
    email = form.data['email']
    password = form.data['password']

    q = base.db_session.query(User).filter(User.email == email)
    user = q.first()

    if user:
        if user.authenticate(password):
            login_result = login_user(user)
            if login_result:
                print("User {0} is login successfully!".format(user.email))
                session['user'] = user.to_json()

            return '/'
        else:
            flash('비밀번호를 다시 확인하여 입력해주세요.')
            return '/auth/login'
    else:
        flash('이메일 및 비밀번호를 다시 확인하여 입력해주세요.')
        return '/auth/login'


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("!!!! ", current_user)
        return redirect('/')

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            redirect_url = login_process(form)
            return redirect(redirect_url)

    return render_template('login.html', form=form, current_user=current_user)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')