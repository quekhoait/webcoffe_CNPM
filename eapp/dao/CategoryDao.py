from eapp.models import Category
from eapp import db


def list(params: dict = None):
    try:
        query = Category.query
        return query.all()
    except Exception as ex:
        print(f"Lỗi khi truy vấn danh sách DishCategory: {ex}")
        return []


def create_category(name):
    try:
        existing = Category.query.filter(Category.name == name).first()
        if existing:
            return None

        new_cat = Category(name=name)
        db.session.add(new_cat)
        db.session.commit()
        return new_cat
    except Exception as e:
        print(f"Lỗi thêm danh mục: {e}")
        db.session.rollback()
        return None