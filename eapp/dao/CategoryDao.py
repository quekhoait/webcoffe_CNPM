from eapp.models import DishCategory



def list(params: dict = None):
    try:
        query = DishCategory.query
        return query.all()
    except Exception as ex:
        print(f"Lỗi khi truy vấn danh sách DishCategory: {ex}")
        return []
