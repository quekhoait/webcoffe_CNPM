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
        ("Cà Phê Đen", "Ly", 20000, "https://i.pinimg.com/1200x/62/1d/28/621d284813ae9e5cc457c1e72630bc3b.jpg"),
        ("Cà Phê Sữa", "Ly", 25000, "https://i.pinimg.com/1200x/ac/e2/ff/ace2fffc49471c96278f15340b5075f1.jpg"),
        ("Bạc Sỉu", "Ly", 28000, "https://product.hstatic.net/200000473381/product/vietnamese_white_coffee_959d080a2d0446238b51afadcdf62ebe_master.jpg")
    ],
    "Trà": [
        ("Trà Đào Cam Sả", "Ly", 35000, "https://i.pinimg.com/736x/13/8b/be/138bbef83a271861125ab2f58f0c8926.jpg"),
        ("Trà Chanh", "Ly", 20000, "https://i.pinimg.com/736x/c6/4d/26/c64d26e91c7c1a09916bcc3223da561b.jpg"),
        ("Trà Gừng", "Ly", 22000, "https://i.pinimg.com/1200x/dc/25/1a/dc251af80d9a20c51999bbed816ef02e.jpg")
    ],
    "Nước Ép": [
        ("Nước Ép Cam", "Ly", 35000, "https://i.pinimg.com/1200x/c2/6a/4a/c26a4abb816850ea054c45c382ac8ae5.jpg"),
        ("Nước Ép Táo", "Ly", 38000, "https://i.pinimg.com/736x/6c/d7/a1/6cd7a1a904d9475a05ed70f5aad81363.jpg"),
        ("Nước Ép Dưa Hấu", "Ly", 30000, "https://i.pinimg.com/736x/24/28/e8/2428e88ca1d3fa2533cc4d94f371c52d.jpg")
    ],
    "Đá Xay": [
        ("Cookie Đá Xay", "Ly", 45000, "https://i.pinimg.com/1200x/b3/44/1b/b3441b6d5641c803d3feb7d2a1db6271.jpg"),
        ("Mocha Đá Xay", "Ly", 48000, "https://glofood.vn/upload/baiviet/hinh02-9852.jpg"),
        ("Matcha Đá Xay", "Ly", 45000, "https://i.pinimg.com/736x/1e/cd/9c/1ecd9c273a1b34e3d7bfcc80bac18ec7.jpg"),
    ],
    "Topping": [
        ("Trân Châu", "Phần", 10000, "https://i.pinimg.com/1200x/3a/34/2e/3a342e6da0864aaf14cc02d92dafad6b.jpg"),
        ("Thạch Phô Mai", "Phần", 12000, "https://i.pinimg.com/1200x/16/b9/46/16b94659ea7e9e461c995ddb78b713fb.jpg"),
        ("Kem Cheese", "Phần", 15000, "https://file.hstatic.net/200000079049/article/lam-kem-cheese_0ccc1181d28749dda84c01dea2d9e087.jpg"),
    ],
    "Bánh Ngọt": [
        ("Bánh Flan", "Phần", 15000, "https://i.pinimg.com/1200x/74/9a/b7/749ab7e9ea0ee79f0044270d5940fb47.jpg"),
        ("Tiramisu", "Miếng", 30000, "https://i.pinimg.com/736x/0e/c2/89/0ec289492947872976c5c52215280faa.jpg"),
        ("Bánh Mousse Chocolate", "Miếng", 35000, "https://i.pinimg.com/736x/e2/31/25/e23125c622f49a8894b547e9bbb78068.jpg")
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
    # Cho cà phê
    {"name": "Cà phê hạt rang", "unit": "gram", "price": 0.6, "description": "Dùng để xay"},
    {"name": "Sữa đặc", "unit": "ml", "price": 0.08, "description": "Pha cà phê sữa"},
    {"name": "Sữa tươi không đường", "unit": "ml", "price": 0.1, "description": "Pha latte/cappuccino"},
    {"name": "Bột cacao", "unit": "gram", "price": 0.3, "description": "Dùng cho mocha hoặc chocolate nóng"},
    # Cho trà
    {"name": "Trà đen", "unit": "gram", "price": 0.2, "description": "Pha trà đá/trà nóng"},
    {"name": "Trà xanh", "unit": "gram", "price": 0.25, "description": "Pha trà xanh/trà sữa"},
    {"name": "Syrup đào", "unit": "ml", "price": 0.15, "description": "Dùng cho trà đào"},
    {"name": "Cam tươi", "unit": "quả", "price": 5000, "description": "Cam cho trà đào"},
    {"name": "Sả tươi", "unit": "cây", "price": 2000, "description": "Sả cho trà đào"},
    {"name": "Gừng tươi", "unit": "gram", "price": 0.1, "description": "Gừng cho trà gừng"},
    # Cho nước ép
    {"name": "Cam ép", "unit": "ml", "price": 0.12, "description": "Nước cam ép tươi"},
    {"name": "Táo ép", "unit": "ml", "price": 0.15, "description": "Nước táo ép"},
    {"name": "Dưa hấu ép", "unit": "ml", "price": 0.1, "description": "Nước dưa hấu"},

    # Cho đá xay
    {"name": "Bột cookie", "unit": "gram", "price": 0.4, "description": "Cho cookie đá xay"},
    {"name": "Syrup mocha", "unit": "ml", "price": 0.2, "description": "Cho mocha đá xay"},
    {"name": "Bột matcha", "unit": "gram", "price": 0.35, "description": "Cho matcha đá xay"},
    # Cho topping
    {"name": "Bột năng", "unit": "gram", "price": 0.05, "description": "Cho trân châu"},
    {"name": "Phô mai", "unit": "gram", "price": 0.25, "description": "Cho thạch phô mai"},
    {"name": "Kem tươi", "unit": "ml", "price": 0.3, "description": "Cho kem cheese"},
    # Cho bánh ngọt
    {"name": "Trứng gà", "unit": "quả", "price": 3000, "description": "Cho bánh flan, tiramisu"},
    {"name": "Bột mì", "unit": "gram", "price": 0.1, "description": "Cho bánh"},
    {"name": "Chocolate", "unit": "gram", "price": 0.4, "description": "Cho mousse chocolate"},
    # Chung
    {"name": "Đường", "unit": "gram", "price": 0.05, "description": "Ngọt hóa đồ uống"},
    {"name": "Đá viên", "unit": "gram", "price": 0, "description": "Dùng cho đồ lạnh"},
]

warehouse_data = [
    {"name": "Kho Tổng", "location": "Tầng hầm"},
    {"name": "Kho Quầy", "location": "Tầng trệt"}
]

stock_data = [
    {"warehouse_id": 1, "ingredient_id": 1, "quantity": 5000},  # Cà phê hạt rang (nhiều vì chính)
    {"warehouse_id": 1, "ingredient_id": 2, "quantity": 2000},  # Sữa đặc
    {"warehouse_id": 1, "ingredient_id": 3, "quantity": 3000},  # Sữa tươi không đường
    {"warehouse_id": 1, "ingredient_id": 4, "quantity": 1500},  # Bột cacao
    {"warehouse_id": 1, "ingredient_id": 5, "quantity": 4000},  # Trà đen (nhiều vì trà phổ biến)
    {"warehouse_id": 1, "ingredient_id": 6, "quantity": 2500},  # Trà xanh
    {"warehouse_id": 1, "ingredient_id": 7, "quantity": 2000},  # Syrup đào
    {"warehouse_id": 1, "ingredient_id": 8, "quantity": 1800},  # Syrup dâu
    {"warehouse_id": 1, "ingredient_id": 9, "quantity": 500},  # Cam tươi (ít vì tươi, dễ hỏng)
    {"warehouse_id": 1, "ingredient_id": 10, "quantity": 300},  # Sả tươi (ít vì tươi)
    {"warehouse_id": 1, "ingredient_id": 11, "quantity": 1000},  # Gừng tươi # Lá trà oolong
    {"warehouse_id": 1, "ingredient_id": 12, "quantity": 3000},  # Cam ép
    {"warehouse_id": 1, "ingredient_id": 13, "quantity": 2500},  # Táo ép
    {"warehouse_id": 1, "ingredient_id": 14, "quantity": 2000},  # Dưa hấu ép
    {"warehouse_id": 1, "ingredient_id": 15, "quantity": 1500},  # Bột cookie
    {"warehouse_id": 1, "ingredient_id": 16, "quantity": 1200},  # Syrup mocha
    {"warehouse_id": 1, "ingredient_id": 17, "quantity": 1000},  # Bột matcha
    {"warehouse_id": 1, "ingredient_id": 18, "quantity": 800},  # Bột năng (cho trân châu)
    {"warehouse_id": 1, "ingredient_id": 19, "quantity": 600},  # Phô mai
    {"warehouse_id": 1, "ingredient_id": 20, "quantity": 1000},  # Kem tươi
    {"warehouse_id": 1, "ingredient_id": 21, "quantity": 5000},  # Trứng gà (nhiều cho bánh)
    {"warehouse_id": 1, "ingredient_id": 22, "quantity": 4000},  # Bột mì
    {"warehouse_id": 1, "ingredient_id": 23, "quantity": 2000},  # Chocolate
    {"warehouse_id": 1, "ingredient_id": 24, "quantity": 10000}  # Đường (rất nhiều)

]

product_recipes_data = {
    "Cà Phê Đen": [
        {"ingredient_name": "Cà phê hạt rang", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Đường", "quantity": 5, "unit": "gram"},
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
    "Trà Đào Cam Sả": [
        {"ingredient_name": "Trà đen", "quantity": 5, "unit": "gram"},
        {"ingredient_name": "Syrup đào", "quantity": 20, "unit": "ml"},
        {"ingredient_name": "Cam tươi", "quantity": 1, "unit": "quả"},
        {"ingredient_name": "Sả tươi", "quantity": 2, "unit": "cây"},
        {"ingredient_name": "Đường", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Đá viên", "quantity": 50, "unit": "gram"},
    ],
    "Trà Chanh": [
        {"ingredient_name": "Trà xanh", "quantity": 5, "unit": "gram"},
        {"ingredient_name": "Cam tươi", "quantity": 0.5, "unit": "quả"},
        {"ingredient_name": "Đường", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Đá viên", "quantity": 50, "unit": "gram"},
    ],
    "Trà Gừng": [
        {"ingredient_name": "Trà đen", "quantity": 5, "unit": "gram"},
        {"ingredient_name": "Gừng tươi", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Đường", "quantity": 15, "unit": "gram"},
    ],
    "Nước Ép Cam": [
        {"ingredient_name": "Cam ép", "quantity": 200, "unit": "ml"},
        {"ingredient_name": "Đường", "quantity": 5, "unit": "gram"},
    ],
    "Nước Ép Táo": [
        {"ingredient_name": "Táo ép", "quantity": 200, "unit": "ml"},
        {"ingredient_name": "Đường", "quantity": 5, "unit": "gram"},
    ],
    "Nước Ép Dưa Hấu": [
        {"ingredient_name": "Dưa hấu ép", "quantity": 200, "unit": "ml"},
        {"ingredient_name": "Đường", "quantity": 5, "unit": "gram"},
    ],
    "Cookie Đá Xay": [
        {"ingredient_name": "Bột cookie", "quantity": 20, "unit": "gram"},
        {"ingredient_name": "Sữa tươi không đường", "quantity": 100, "unit": "ml"},
        {"ingredient_name": "Đá viên", "quantity": 100, "unit": "gram"},
    ],
    "Mocha Đá Xay": [
        {"ingredient_name": "Syrup mocha", "quantity": 20, "unit": "ml"},
        {"ingredient_name": "Cà phê hạt rang", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Sữa tươi không đường", "quantity": 100, "unit": "ml"},
        {"ingredient_name": "Đá viên", "quantity": 100, "unit": "gram"},
    ],
    "Matcha Đá Xay": [
        {"ingredient_name": "Bột matcha", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Sữa tươi không đường", "quantity": 100, "unit": "ml"},
        {"ingredient_name": "Đá viên", "quantity": 100, "unit": "gram"},
    ],
    "Trân Châu": [
        {"ingredient_name": "Bột năng", "quantity": 50, "unit": "gram"},
        {"ingredient_name": "Đường", "quantity": 20, "unit": "gram"},
    ],
    "Thạch Phô Mai": [
        {"ingredient_name": "Phô mai", "quantity": 30, "unit": "gram"},
        {"ingredient_name": "Sữa đặc", "quantity": 10, "unit": "ml"},
    ],
    "Kem Cheese": [
        {"ingredient_name": "Kem tươi", "quantity": 50, "unit": "ml"},
        {"ingredient_name": "Phô mai", "quantity": 20, "unit": "gram"},
    ],
    "Bánh Flan": [
        {"ingredient_name": "Trứng gà", "quantity": 2, "unit": "quả"},
        {"ingredient_name": "Sữa đặc", "quantity": 50, "unit": "ml"},
        {"ingredient_name": "Đường", "quantity": 30, "unit": "gram"},
    ],
    "Tiramisu": [
        {"ingredient_name": "Bột mì", "quantity": 50, "unit": "gram"},
        {"ingredient_name": "Cà phê hạt rang", "quantity": 10, "unit": "gram"},
        {"ingredient_name": "Trứng gà", "quantity": 1, "unit": "quả"},
        {"ingredient_name": "Bột cacao", "quantity": 5, "unit": "gram"},
    ],
    "Bánh Mousse Chocolate": [
        {"ingredient_name": "Chocolate", "quantity": 50, "unit": "gram"},
        {"ingredient_name": "Kem tươi", "quantity": 100, "unit": "ml"},
        {"ingredient_name": "Trứng gà", "quantity": 1, "unit": "quả"},
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

            for name, unit, price, image_url in items:
                dish = Product(
                    name=name,
                    unit=unit,
                    price=price,
                    status=ProductStatus.ACTIVE,
                    description=f"{name} được pha chế theo công thức đặc biệt của quán.",
                    image=image_url,
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
