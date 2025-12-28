from flask import Flask, url_for, session, redirect
from authlib.integrations.flask_client import OAuth
from eapp import db  # Giả sử bạn khởi tạo db trong file __init__ hoặc tương đương
from eapp.models import Account
from eapp.models.Account import Role
import os
from flask_login import login_user

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.secret_key = os.getenv("SECRET_KEY_GOOGLE")
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("YOUR_CLIENT_ID"),
    client_secret=os.getenv("YOUR_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)



def login():
    redirect_uri = url_for('callback_google', _external=True)
    return google.authorize_redirect(redirect_uri)



def auth():
    token = google.authorize_access_token()
    print("token", token)
    user_info = token.get('userinfo')
    g_id = user_info.get('sub')
    user = Account.query.filter((Account.google_id == g_id) | (Account.email == user_info['email'])).first()
    if not user:
        user = Account(
            username=user_info.get('name'),  # Dùng email làm username tạm thời
            google_id=user_info.get('sub'),
            email=user_info.get('email'),
            name=user_info.get('name'),
            avatar=user_info.get('picture'),
            provider='google',
            role=Role.USER
        )
        db.session.add(user)
        db.session.commit()
    elif not user.google_id:
        # Nếu đã có email trong DB nhưng chưa có google_id (liên kết tài khoản)
        user.google_id = g_id
        user.provider = 'google'
        db.session.commit()

    # 3. Đăng nhập (Dùng session hoặc flask_login)
    login_user(user)
    return redirect(url_for("home"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Cho phép chạy http local
    app.run(debug=True)