from eapp.models import Product, ProductRecipe
from sqlalchemy import desc
from eapp import db


def list(params: dict = None):
    try:
        query = Product.query
        if params:
            if 'category_id' in params:
                query = query.filter(Product.dish_category_id == params['category_id'])

            if 'name' in params:
                query = query.filter(Product.name.contains(params['name']))

            if 'filter' in params:
                if params['filter'] == 'new':
                    # sx theo ngày tạo giảm dần
                    query = query.order_by(desc(Product.created_date))
                elif params['filer'] == 'best':
                    # sx theo số lượt đánh giá giảm dần
                    query = query.order_by(desc(Product.rating_count))

        return query.all()

    except Exception as ex:
        print(f"Lỗi khi lọc món: {ex}")
        return []
    

def get_by_id(id):
    try:
        return Product.query.get(id)
    except Exception as ex:
        print(f"Lỗi khi món theo id: {ex}")
        return None



def list(params=None):
    return Product.query.order_by(Product.id.desc()).all()


def get_by_id(id):
    return Product.query.get(id)


def add_product(data):
    try:
        new_product = Product(
            name=data.get('name'),
            price=data.get('price'),
            unit=data.get('unit'),
            dish_category_id=data.get('dish_category_id'),
            description=data.get('description'),
            image=data.get('image')
        )
        db.session.add(new_product)
        db.session.commit()
        return True
    except Exception as ex:
        print(f"Lỗi thêm: {ex}")
        db.session.rollback()
        return False


def update_product(product_id, data):
    try:
        product = Product.query.get(product_id)
        if not product: return False

        product.name = data.get('name')
        product.price = data.get('price')
        product.unit = data.get('unit')
        product.dish_category_id = data.get('dish_category_id')
        product.description = data.get('description')

        if data.get('image'):
            product.image = data.get('image')

        db.session.commit()
        return True
    except Exception as ex:
        print(f"Lỗi sửa: {ex}")
        db.session.rollback()
        return False


def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            #xóa công thức trước
            ProductRecipe.query.filter_by(product_id=product_id).delete()

            db.session.delete(product)
            db.session.commit()
            return True
        return False
    except Exception as ex:
        print(f"Lỗi xóa: {ex}")
        db.session.rollback()
        return False