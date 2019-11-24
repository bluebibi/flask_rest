from flask import Blueprint, redirect, render_template, request, flash, session

from database import base
from database.base import User
from forms import UserForm, LoginForm
from flask_login import login_required, login_user, logout_user, current_user
import requests

auth_blueprint = Blueprint('auth', __name__)

kakao_oauth = {}

@auth_blueprint.route('/check_registration')
@login_required
def _user():
    q = base.db_session.query(User).filter(User.email == current_user.email)
    user = q.first()
    return render_template("my_page.html", user=user)


def login_process(email, password):
    q = base.db_session.query(User).filter(User.email == email)
    user = q.first()

    print(email, password, user, "11111")

    if user:
        print(email, password, user, "22222")

        if user.authenticate(password):
            print(email, password, user, "33333")

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
            redirect_url = login_process(form.data['email'], form.data['password'])
            return redirect(redirect_url)

    return render_template('login.html', form=form, current_user=current_user)


@auth_blueprint.route('kakao_oauth_redirect')
def kakao_oauth_redirect():
    if "access_token" not in kakao_oauth:
        code = str(request.args.get('code'))
        url = "https://kauth.kakao.com/oauth/token"
        data = "grant_type=authorization_code" \
                "&client_id=0eb67d9cd0372c01d3915bbd934b4f6d" \
                "&redirect_uri=http://localhost:8080/auth/kakao_oauth_redirect" \
                "&code={0}".format(code)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Cache-Control": "no-cache"
        }
        response = requests.post(
            url=url,
            data=data,
            headers=headers
        )

        print(response.json())

        kakao_oauth["access_token"] = response.json()["access_token"]
        kakao_oauth["expires_in"] = response.json()["expires_in"]
        kakao_oauth["refresh_token"] = response.json()["refresh_token"]
        kakao_oauth["refresh_token_expires_in"] = response.json()["refresh_token_expires_in"]
        kakao_oauth["scope"] = response.json()["scope"]
        kakao_oauth["token_type"] = response.json()["token_type"]

        if "kaccount_email" not in kakao_oauth:
            kakao_me_and_signup()

    redirect_url = login_process(kakao_oauth["kaccount_email"], "1234")
    return redirect(redirect_url)

def kakao_me_and_signup():
    url = "https://kapi.kakao.com/v1/user/me"
    headers = {
        "Authorization": "Bearer {0}".format(kakao_oauth["access_token"]),
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    response = requests.post(
        url=url,
        headers=headers
    )
    print("kakap_me", response.json())

    kakao_oauth["kaccount_email"] = response.json()["kaccount_email"]
    kakao_oauth["id"] = response.json()["id"]
    kakao_oauth["kakao_profile_image"] = response.json()["properties"]["profile_image"]
    kakao_oauth["nickname"] = response.json()["properties"]["nickname"]
    kakao_oauth["kakao_thumbnail_image"] = response.json()["properties"]["thumbnail_image"]

    user = User(name=kakao_oauth["nickname"], email=kakao_oauth["kaccount_email"], affiliation=None)
    user.set_password("1234")
    base.db_session.add(user)
    base.db_session.commit()


def kakao_logout():
    url = "https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Authorization": "Bearer {0}".format(kakao_oauth["access_token"])
    }
    response = requests.post(
        url=url,
        headers=headers
    )

    print(response.status_code)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    if kakao_oauth:
        kakao_logout()

    return redirect('/')