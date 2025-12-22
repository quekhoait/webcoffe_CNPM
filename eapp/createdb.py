import hashlib

from eapp import db, app
# from eapp.models import Category as DishCategory, Product as Dish, DishStatus
from eapp.models import Category, Product, ProductStatus
import random

from eapp.models.ProductRecipe import ProductRecipe
from eapp.models.Rule import RuleType
from eapp.models.Account import Role

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



accounts = [
    {
        "username": "admin",
        "password": str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
        "phone": "0123456789",
        "name": "Huy dep trai",
        "role": Role.ADMIN
    },
    {
        "username": "cashier",
        "password":str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
        "phone" : "0987654321",
        "name": "Nhân Viên Thu Ngân 1",
        "role": Role.CASHIER
    },
    {
        "username": "staff",
        "password": str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
        "phone" : "0912345678",
        "name": "Nhân Viên Phục Vụ 1",
        "role": Role.STAFF
    },
    {
        "username": "khaoit",
        "password": str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
        "phone": "0916445657",
        "address":"quem",
        "name": "HUy ngu",
        "role":Role.USER
    }
]

ingredients_data = [
    # Nhóm cà phê
    {"name": "Cà phê hạt rang", "unit": "gram", "price": 0.6, "description": "Dùng để xay"},
    {"name": "Bột cà phê", "unit": "gram", "price": 0.5, "description": "Cà phê đã xay sẵn"},
    {"name": "Sữa đặc", "unit": "ml", "price": 0.08, "description": "Pha cà phê sữa"},
    {"name": "Sữa tươi không đường", "unit": "ml", "price": 0.1, "description": "Pha latte/cappuccino"},
    {"name": "Bột cacao", "unit": "gram", "price": 0.3, "description": "Dùng cho mocha hoặc chocolate nóng"},

    # Nhóm trà
    {"name": "Trà đen", "unit": "gram", "price": 0.2, "description": "Pha trà đá/trà nóng"},
    {"name": "Trà xanh", "unit": "gram", "price": 0.25, "description": "Pha trà xanh/trà sữa"},
    {"name": "Syrup đào", "unit": "ml", "price": 0.15, "description": "Dùng cho trà đào"},
    {"name": "Syrup dâu", "unit": "ml", "price": 0.15, "description": "Dùng cho trà dâu"},

    # Nhóm topping
    {"name": "Trân châu đen", "unit": "gram", "price": 0.2, "description": "Dùng cho trà sữa/trà trái cây"},
    {"name": "Thạch rau câu", "unit": "gram", "price": 0.1, "description": "Dùng cho topping"},
    {"name": "Kem tươi", "unit": "ml", "price": 0.3, "description": "Dùng trang trí/latte"},

    # Nhóm phụ liệu
    {"name": "Đường", "unit": "gram", "price": 0.05, "description": "Ngọt hóa đồ uống"},
    {"name": "Đá viên", "unit": "gram", "price": 0, "description": "Dùng cho đồ lạnh"},
]

warehouse_data = [
    {"name": "Kho Tổng", "location": "Tầng hầm"},
    {"name": "Kho Quầy", "location": "Tầng trệt"}
]

stock_data = [
    # Kho Tổng  
    {"warehouse_id": 1, "ingredient_id": 1, "quantity": 5000},  # Cà phê hạt rang
    {"warehouse_id": 1, "ingredient_id": 6, "quantity":3000},  # Trà đen
    {"warehouse_id": 1, "ingredient_id": 2, "quantity": 1000},  # Cà phê hạt rang
    {"warehouse_id": 1, "ingredient_id": 13, "quantity": 2000}, # Đường
    {"warehouse_id": 1, "ingredient_id": 14, "quantity": 10000}, # Đá viên
    {"warehouse_id": 1, "ingredient_id": 10, "quantity": 1000}, # Trân châu đen
    {"warehouse_id": 1, "ingredient_id": 11, "quantity": 800},  # Thạch rau câu
    {"warehouse_id": 1, "ingredient_id": 12, "quantity": 1500}, # Kem tươi
]

product_recipes_data = {
    "Cà Phê Đen": [
        {"ingredient_name": "Cà phê hạt rang", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Đá viên", "quantity": 50, "unit": "gram"},
    ],
    "Cà Phê Sữa": [
        {"ingredient_name": "Cà phê hạt rang", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Sữa đặc", "quantity": 20, "unit": "ml"},
        {"ingredient_name": "Đá viên", "quantity": 50, "unit": "gram"},
    ],
    "Bạc Sỉu": [
        {"ingredient_name": "Cà phê hạt rang", "quantity": 5, "unit": "gram"},
        {"ingredient_name": "Sữa tươi không đường", "quantity": 50, "unit": "ml"},
        {"ingredient_name": "Sữa đặc", "quantity": 10, "unit": "ml"},
        {"ingredient_name": "Đá viên", "quantity": 50, "unit": "gram"},
    ],
    "Latte": [
        {"ingredient_name": "Cà phê hạt rang", "quantity": 8, "unit": "gram"},
        {"ingredient_name": "Sữa tươi không đường", "quantity": 100, "unit": "ml"},
    ],
    "Trà Đào Cam Sả": [
        {"ingredient_name": "Trà đen", "quantity": 5, "unit": "gram"},
        {"ingredient_name": "Syrup đào", "quantity": 20, "unit": "ml"},
        {"ingredient_name": "Đá viên", "quantity": 50, "unit": "gram"},
    ],
}
from eapp.models import Invoice, InvoiceDetail
from eapp.models.Invoice import InvoiceStatusEnum, PaymentMethod
from _datetime import datetime





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




        # Seed accounts
        for acc_data in accounts:
            from eapp.models.Account import Account
            acc = Account(**acc_data)
            db.session.add(acc)
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

        # Seed rules
        from eapp.models.Rule import Rule
        for rule_data in rules_seed:
            rule = Rule(**rule_data)
            db.session.add(rule)
        db.session.commit()

        # seed ingredients
        from eapp.models.Ingredient import Ingredient
        for ingredient_data in ingredients_data:
            ingredient = Ingredient(**ingredient_data)
            db.session.add(ingredient)

        # seed warehouses
        from eapp.models.Warehouse import Warehouse
        for warehouse_info in warehouse_data:
            warehouse = Warehouse(**warehouse_info)
            db.session.add(warehouse)
        
        #seed stocks
        from eapp.models.Stock import Stock
        for stock_info in stock_data:
            stock = Stock(**stock_info)
            db.session.add(stock)
        
        db.session.commit()

        for product_name, ingredients_list in product_recipes_data.items():
            product = Product.query.filter_by(name=product_name).first()
            if not product:
                print(f"⚠️ Không tìm thấy sản phẩm {product_name}")
                continue

            for ing_data in ingredients_list:
                ingredient = Ingredient.query.filter_by(name=ing_data["ingredient_name"]).first()
                if not ingredient:
                    print(f"⚠️ Không tìm thấy nguyên liệu {ing_data['ingredient_name']}")
                    continue

                recipe = ProductRecipe(
                    product_id=product.id,
                    ingredient_id=ingredient.id,
                    quantity=ing_data["quantity"],
                    unit=ing_data["unit"]
                )
                db.session.add(recipe)

        db.session.commit()
        print("✅ Seed dữ liệu ProductRecipe thành công!")

        invoice1 = Invoice(
            order_code="INV001",
            cashier_id=1,
            customer_id=2,
            staff_id=1,
            subtotal=120000,
            extra_fee_total=10000,
            final_total=130000,
            note="Khách mua tại quầy",
            payment_method=PaymentMethod.CASH,
            invoice_status=InvoiceStatusEnum.COMPLETED,
            created_date=datetime.now()
        )

        invoice1_details = [
            InvoiceDetail(
                product_id=1,
                quantity=2,
                price=50000
            ),
            InvoiceDetail(
                product_id=2,
                quantity=1,
                price=20000
            )
        ]

        invoice1.invoice_details = invoice1_details

        # ===== Invoice 2 =====
        invoice2 = Invoice(
            order_code="INV002",
            cashier_id=None,
            customer_id=3,
            staff_id=2,
            subtotal=80000,
            extra_fee_total=0,
            final_total=80000,
            note="Đơn online",
            payment_method=PaymentMethod.MOMO,
            invoice_status=InvoiceStatusEnum.COMPLETED,
            created_date=datetime.now()
        )

        invoice2.invoice_details = [
            InvoiceDetail(
                product_id=3,
                quantity=2,
                price=40000
            )
        ]

        # ===== Invoice 3 =====
        invoice3 = Invoice(
            order_code="INV003",
            cashier_id=1,
            customer_id=4,
            staff_id=1,
            subtotal=150000,
            extra_fee_total=15000,
            final_total=165000,
            note="Khách VIP",
            payment_method=PaymentMethod.CASH,
            invoice_status=InvoiceStatusEnum.COMPLETED,
            created_date = datetime(2025, 9, 15, 10, 30, 0)
        )

        invoice3.invoice_details = [
            InvoiceDetail(
                product_id=1,
                quantity=3,
                price=50000
            )
        ]

        # ===== Add vào DB =====
        db.session.add_all([invoice1, invoice2, invoice3])
        db.session.commit()

        print("✅ Seed invoice data thành công!")


        print("☕️ Seed dữ liệu quán cà phê thành công!")
