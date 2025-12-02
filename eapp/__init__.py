from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from eapp.models.Account import Account
load_dotenv()
import os
import cloudinary

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
app = Flask(__name__)
app.secret_key = 'JKHJHJK786575ghjghjg78675HJGJHGF^&$%$^*%*&^%&^&*%^&'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["PAGE_SIZE"] = 8
print(app.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(app)
login_manager = LoginManager(app=app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from eapp.models.Account import Account
    return Account.query.get(int(user_id))

from eapp import routes

cloudinary.config(cloud_name=os.getenv("CLOUD_NAME"),
                  api_key=os.getenv("API_KEY"),
                  api_secret='API_SECRET')

