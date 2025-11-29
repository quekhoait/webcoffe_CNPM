from eapp.models import Category



def list(params: dict = None):
    try:
        query = Category.query
        return query.all()
    except Exception as ex:
        print(f"Lỗi khi truy vấn danh sách DishCategory: {ex}")
        return []
