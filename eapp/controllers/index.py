from flask import render_template, session, request, redirect, url_for
from eapp import db
from eapp.models.Order import Order, OrderDetail
from datetime import datetime

from sqlalchemy import desc #hàm sx giảm dần
from eapp.models.Product import Dish
from eapp.models.Category import DishCategory
from flask import render_template, request


#coffeeProducts = [
#     {
#         'idMon': 1,
#         'TenMon': "Cà Phê Đen Đá Truyền Thống",
#         'DonVi': "Ly",
#         'DonGia': "29000",
#         'TrangThai': "Còn hàng",
#         'MoTa': "Vị đậm đà, thơm lừng từ hạt Robusta rang xay. Thức uống kinh điển.",
#         'HinhAnh': "coffee_den_da.jpg",
#         'NgayTao': "2024-01-10 10:30:00",
#         'NgayCapNhat': "2024-11-20 14:00:00",
#         'DanhMucMon_idDanhMucMon': 1,
#         'DiemDanhGia': "4.8",
#         'SoLuotDanhGia': "215",
#     },
#     {
#         'idMon': 2,
#         'TenMon': "Cà Phê Sữa Đá",
#         'DonVi': "Ly",
#         'DonGia': "35000",
#         'TrangThai': "Còn hàng",
#         'MoTa': "Hòa quyện giữa cà phê đậm và sữa đặc béo ngậy.",
#         'HinhAnh': "coffee_sua_da.jpg",
#         'NgayTao': "2024-01-10 10:30:00",
#         'NgayCapNhat': "2024-10-15 08:45:00",
#         'DanhMucMon_idDanhMucMon': 1,
#         'DiemDanhGia': "4.9",
#         'SoLuotDanhGia': "350",
#     },
#     {
#         'idMon': 3,
#         'TenMon': "Espresso Nóng",
#         'DonVi': "Tách",
#         'DonGia': "45000",
#         'TrangThai': "Còn hàng",
#         'MoTa': "Một shot cà phê nguyên chất, lớp Crema hoàn hảo.",
#         'HinhAnh': "espresso_hot.jpg",
#         'NgayTao': "2024-03-01 11:00:00",
#         'NgayCapNhat': "2024-03-01 11:00:00",
#         'DanhMucMon_idDanhMucMon': 1,
#         'DiemDanhGia': "4.5",
#         'SoLuotDanhGia': "98",
#     },
#     {
#         'idMon': 4,
#         'TenMon': "Cà Phê Dừa Đá Xay",
#         'DonVi': "Ly lớn",
#         'DonGia': "59000",
#         'TrangThai': "Hết hàng tạm thời",
#         'MoTa': "Thức uống giải khát, mát lạnh với hương dừa và cà phê.",
#         'HinhAnh': "coffee_dua_xay.jpg",
#         'NgayTao': "2024-05-20 15:30:00",
#         'NgayCapNhat': "2024-11-20 09:00:00",
#         'DanhMucMon_idDanhMucMon': 2,
#         'DiemDanhGia': "4.7",
#         'SoLuotDanhGia': "155",
#     },
#     {
#         'idMon': 5,
#         'TenMon': "Latte Hạnh Nhân Nóng",
#         'DonVi': "Tách",
#         'DonGia': "65000",
#         'TrangThai': "Còn hàng",
#         'MoTa': "Cà phê sữa béo ngậy với hương thơm hạnh nhân dịu nhẹ.",
#         'HinhAnh': "latte_almond.jpg",
#         'NgayTao': "2024-11-15 09:00:00",
#         'NgayCapNhat': "2024-11-15 09:00:00",
#         'DanhMucMon_idDanhMucMon': 1,
#         'DiemDanhGia': "4.6",
#         'SoLuotDanhGia': "112",
#     },
# ]


def load_login():
    return render_template('page/login.html')
  
def load_regis():
    return render_template('page/register.html')
  
def load_home():
    return render_template('page/home.html', is_home=True)

def load_about_us():
    return render_template('page/about_us.html')



def checkout_page():
    current_user = session.get('user')

    #test
    if not current_user:
        current_user = {'id': 1, 'name': 'Khách hàng Test', 'phone': '0909000111', 'email': 'test@gmail.com'}

    #giỏ hàng
    cart = session.get('cart', {})
    if not cart:
        cart = {
            '1': {'id': 1, 'name': 'Cafe Demo', 'price': 25000, 'quantity': 2, 'image': ''}
        }

    # TongTam
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    # TongPhuPhi (Ví dụ = 0)
    surcharge = 0
    # TongThanhToan
    total_amount = subtotal + surcharge

    #xử lý đặt hàng
    if request.method == 'POST':
        try:
            payment_method = request.form.get('payment_method')

            if payment_method == 'MOMO':
                order_status = 2 #đã thanh toán

            else:
                order_status = 1 #chờ xử lý

            #tạo đơn hàng
            new_order = Order(
                customer_id=current_user['id'],  # NguoiDung_idKhachHang
                payment_method=payment_method,  # HinhThucThanhToan
                subtotal=subtotal,  # TongTam
                surcharge=surcharge,  # TongPhuPhi
                total_amount=total_amount,  # TongThanhToan
                created_date=datetime.now(),  # NgayLap
                status_id=order_status # TrangThai

            )
            db.session.add(new_order)
            db.session.flush()  # Lấy ID vừa tạo

            # Lưu chi tiết
            for item in cart.values():
                item_total = item['price'] * item['quantity']
                detail = OrderDetail(
                    order_id=new_order.id,  # HoaDon_idHoaDon
                    dish_id=item['id'],  # Mon_idMon
                    quantity=item['quantity'],  # SoLuong
                    price=item['price'],  # DonGia
                    total_price=item['price'] * item['quantity'] # ThanhTien
                )
                db.session.add(detail)

            db.session.commit()

            #xóa giỏ hàng sau khi đặt thành công
            if session.get('cart'): session.pop('cart', None)

            return redirect('/')

        except Exception as ex:
            db.session.rollback()
            print(f"Lỗi DB: {ex}")
            return "Lỗi xử lý đơn hàng", 500

    #hiển thị
    user_info = {
        'fullname': current_user.get('name', ''),
        'phone': current_user.get('phone', ''),
        'email': current_user.get('email', '')
    }

    return render_template('page/checkout.html',
                           cart_items=cart.values(),
                           total_price=total_amount,
                           user_info=user_info)



def menu_page():
    # /menu?q=cafe&category=1&filter=new
    search_query = request.args.get('q', '')  #từ khóa tìm kiếm
    category_id = request.args.get('category')  #id danh mục
    filter_type = request.args.get('filter')  #lọc

    categories = DishCategory.query.all()

    query = Dish.query

    # tìm kiếm
    if search_query:
        # tìm món có tên chứa từ khóa
        query = query.filter(Dish.name.contains(search_query))

    # lọc
    if category_id:
        try:
            cat_id_int = int(category_id)
            query = query.filter(Dish.dish_category_id == cat_id_int)
        except ValueError:
            pass

    #sắp xếp món
    if filter_type == 'new':
        #sx theo ngày tạo giảm dần
        query = query.order_by(desc(Dish.created_date))
    elif filter_type == 'best':
        #sx theo số lượt đánh giá giảm dần
        query = query.order_by(desc(Dish.rating_count))
    else:
        #mặc định sx theo ID
        query = query.order_by(Dish.id)

    products = query.all()


    return render_template('page/menu.html',
                           products=products,
                           categories=categories,
                           # Gửi lại các tham số để View biết cái nào đang được chọn
                           current_cate_id=int(category_id) if category_id else None,
                           current_filter=filter_type,
                           search_query=search_query)

def load_profile():
    tab = request.args.get("tab", "profile")
    return render_template("page/profile.html", tab=tab)

def load_my_cart():
    return render_template('page/cart.html')


