from eapp import db, app
from eapp.models import Category, Product, ProductStatus, Account
import random

DEFAULT_IMAGE = "https://picsum.photos/seed/picsum/200/300"

# Danh mục dành cho quán cà phê
cafe_categories = [
    "Cà Phê",
    "Trà",
    "Nước Ép",
    "Đá Xay",
    "Topping",
    "Bánh Ngọt"
]

# Món theo từng category
cafe_dishes = {
    "Cà Phê": [
        ("Cà Phê Đen", "Ly", 20000),
        ("Cà Phê Sữa", "Ly", 25000),
        ("Bạc Sỉu", "Ly", 28000),
        ("Cold Brew", "Ly", 35000),
        ("Latte", "Ly", 40000),
    ],
    "Trà": [
        ("Trà Đào Cam Sả", "Ly", 35000),
        ("Trà Chanh", "Ly", 20000),
        ("Trà Gừng", "Ly", 22000),
        ("Trà Oolong", "Ly", 30000),
        ("Trà Sữa Truyền Thống", "Ly", 30000),
    ],
    "Nước Ép": [
        ("Nước Ép Cam", "Ly", 35000),
        ("Nước Ép Táo", "Ly", 38000),
        ("Nước Ép Dưa Hấu", "Ly", 30000),
        ("Nước Ép Cà Rốt", "Ly", 32000),
        ("Nước Ép Thơm", "Ly", 33000),
    ],
    "Đá Xay": [
        ("Cookie Đá Xay", "Ly", 45000),
        ("Mocha Đá Xay", "Ly", 48000),
        ("Matcha Đá Xay", "Ly", 45000),
    ],
    "Topping": [
        ("Trân Châu", "Phần", 10000),
        ("Thạch Phô Mai", "Phần", 12000),
        ("Kem Cheese", "Phần", 15000),
    ],
    "Bánh Ngọt": [
        ("Bánh Flan", "Phần", 15000),
        ("Tiramisu", "Miếng", 30000),
        ("Bánh Mousse Chocolate", "Miếng", 35000),
        ("Bông Lan Trứng Muối", "Miếng", 30000),
    ],
}

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("🔄 Đang tạo dữ liệu mẫu cho quán cà phê...")

        # Tạo categories
        created_categories = {}

        for cat_name in cafe_categories:
            cat = Category(name=cat_name, description=f"Danh mục {cat_name.lower()} của quán.")
            db.session.add(cat)
            created_categories[cat_name] = cat

        db.session.commit()

        # Seed dishes
        for cat_name, items in cafe_dishes.items():
            category = created_categories[cat_name]

            for name, unit, price in items:
                dish = Product(
                    name=name,
                    unit=unit,
                    price=price,
                    status=ProductStatus.ACTIVE,
                    description=f"{name} được pha chế theo công thức đặc biệt của quán.",
                    image=DEFAULT_IMAGE,
                    rating_score=round(random.uniform(3.5, 5), 1),
                    rating_count=random.randint(10, 200),
                    dish_category_id=category.id,
                )
                db.session.add(dish)

        db.session.commit()

        print("Seed dữ liệu quán cà phê thành công!")
