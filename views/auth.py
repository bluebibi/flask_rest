from flask import Blueprint, redirect, render_template, request, flash, session

from database import base
from database.base import User
from forms import UserForm, LoginForm, MyPageUserForm
from flask_login import login_required, login_user, logout_user, current_user


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/my_page', methods=['GET', 'POST'])
@login_required
def _user():
    form = MyPageUserForm()

    q = base.db_session.query(User).filter(User.email == current_user.email)
    user = q.first()

    if request.method == 'POST':
        if form.validate_on_submit():
            user.email = request.form['email']
            user.name = request.form['name']
            user.set_password(request.form['password'])
            user.affiliation = request.form['affiliation']
            base.db_session.commit()
            flash('귀하의 회원정보가 수정 되었습니다.')
            return redirect('/auth/my_page')

    return render_template("my_page.html", user=user, form=form)


def login_process(form):
    email = form.data['email']
    password = form.data['password']

    q = base.db_session.query(User).filter(User.email == email)
    user = q.first()

    if user:
        if user.authenticate(password):
            login_result = login_user(user)
            if login_result:
                print("사용자(사용자 이메일:{0})의 로그인 성공!".format(current_user.email))
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


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            new_user.email = request.form['email']
            new_user.name = request.form['name']
            new_user.set_password(request.form['password'])
            new_user.affiliation = request.form['affiliation']

            base.db_session.add(new_user)
            base.db_session.commit()
            flash('귀하는 회원가입이 성공적으로 완료되었습니다. 가입하신 정보로 로그인을 다시 하시기 바랍니다.')
            return redirect('/auth/login')

    return render_template("signup.html", form=form)