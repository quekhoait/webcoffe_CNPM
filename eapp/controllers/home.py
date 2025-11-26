from flask import Flask, render_template

app = Flask(__name__)

# 1. BIẾN DỮ LIỆU SẢN PHẨM PYTHON
# Đây là list các dictionary (tương đương với mảng các object trong JS)
# coffeeProducts = [
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


def home():
    return render_template('page/home.html')

def aboutUs():
    return render_template('page/about_us.html')







