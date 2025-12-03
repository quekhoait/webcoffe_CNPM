from eapp import db, app
from eapp.models import Category as DishCategory, Product as Dish, DishStatus
import random

from eapp.models.Rule import RuleType

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

rules_seed = [
    {
        "name": "phí phục vụ",
        "rule_type": RuleType.SERVICE,
        "value": 10,
        "unit": "%",
        "instance_rule_id": None,
        "description": "Phí phục vụ áp dụng cho tất cả đơn hàng",
        "active": True
    },{
        "name": "Nguyên liệu tồn kho tối thiểu",
        "rule_type": RuleType.INGREDIENT,
        "value": 5,
        "unit": None,
        "instance_rule_id": None,
        "description": "Mức tồn kho tối thiểu cho mỗi nguyên liệu",
        "active": True
    }
] 

invoice_status_seed = [
    {"name": "Chờ xử lý", "code": "PENDING", "description": "Hóa đơn mới được tạo và đang chờ xử lý."},
    {"name": "Đã thanh toán", "code": "PAID", "description": "Hóa đơn đã được thanh toán đầy đủ."},
    {"name": "Đã hủy", "code": "CANCELLED", "description": "Hóa đơn đã bị hủy và không còn hiệu lực."}
    # {"name": "Đang xử lý", "description": "Hóa đơn mới được tạo và đang chờ xử lý."},
    # {"name": "Đã thanh toán", "description": "Hóa đơn đã được thanh toán đầy đủ."},
    # {"name": "Đã hủy", "description": "Hóa đơn đã bị hủy và không còn hiệu lực."}
]

roles = [
    {"name": "Admin", "description": "Quản trị viên hệ thống với toàn quyền."},
    {"name": "Cashier", "description": "Nhân viên thu ngân, chịu trách nhiệm xử lý thanh toán."},
    {"name": "Staff", "description": "Nhân viên phục vụ và hỗ trợ khách hàng."}
]

accounts = [
    {
        "username": "admin",
        "password": "123",
        "phone": "0123456789",
        "name": "Huy dep trai",
        "role_id": 1
    },
    {
        "username": "cashier",
        "password": "123",
        "phone" : "0987654321",
        "name": "Nhân Viên Thu Ngân 1",
        "role_id": 2
    },
    {
        "username": "staff",
        "password": "staffpass",
        "phone" : "0912345678",
        "name": "Nhân Viên Phục Vụ 1",
        "role_id": 3
    }
]

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("🔄 Đang tạo dữ liệu mẫu cho quán cà phê...")

        # Tạo categories
        created_categories = {}

        for cat_name in cafe_categories:
            cat = DishCategory(name=cat_name, description=f"Danh mục {cat_name.lower()} của quán.")
            db.session.add(cat)
            created_categories[cat_name] = cat
        
        db.session.commit()

        

        for role_data in roles:
            from eapp.models.Role import Role
            role = Role(**role_data)
            db.session.add(role)

        db.session.commit()

        # Seed accounts
        for acc_data in accounts:
            from eapp.models.Account import Account
            acc = Account(**acc_data)
            db.session.add(acc)
        db.session.commit()
                    
        
        # Seed invoice statuses
        from eapp.models.InvoiceStatus import InvoiceStatus
        for status_data in invoice_status_seed:
            status = InvoiceStatus(**status_data)
            db.session.add(status)
        
        db.session.commit()

        # Seed dishes
        for cat_name, items in cafe_dishes.items():
            category = created_categories[cat_name]

            for name, unit, price in items:
                dish = Dish(
                    name=name,
                    unit=unit,
                    price=price,
                    status=DishStatus.ACTIVE,
                    description=f"{name} được pha chế theo công thức đặc biệt của quán.",
                    image=DEFAULT_IMAGE,
                    rating_score=round(random.uniform(3.5, 5), 1),
                    rating_count=random.randint(10, 200),
                    dish_category_id=category.id,
                )
                db.session.add(dish)


        db.session.commit()

        # Seed rules
        from eapp.models.Rule import Rule
        for rule_data in rules_seed:
            rule = Rule(**rule_data)
            db.session.add(rule)    
        db.session.commit()

        print("☕️ Seed dữ liệu quán cà phê thành công!")
