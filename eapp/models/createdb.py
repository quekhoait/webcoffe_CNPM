from eapp import db, app
from eapp.models import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()