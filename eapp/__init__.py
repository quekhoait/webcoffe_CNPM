from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

import os
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
app = Flask(__name__)
app.secret_key = 'JKHJHJK786575ghjghjg78675HJGJHGF^&$%$^*%*&^%&^&*%^&'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:12345@localhost/coffestore"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["PAGE_SIZE"] = 8

db = SQLAlchemy(app)

from eapp import routes
from eapp.models.Order import Order, OrderDetail
