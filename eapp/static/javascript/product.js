

function loadProducts(params = {}) {
    const query = new URLSearchParams(params).toString();
    const productList = document.getElementById('menu-product-items')
    fetch('/api/dish?' + query)
        .then(res => res.text())
        .then(html => {
            productList.innerHTML = html
        })
        .catch(err => console.error(err));
}

document.getElementById('search-product').addEventListener('input', (e) => {
    loadProducts({ 'name': e.target.value })
})


//Cart

const mycart = document.getElementById("my_cart");
const cartIcon = document.getElementById("cart_icon");
const cartCancelIcon = document.getElementById("icon_cancel_cart");

cartIcon.addEventListener("click", () => {
    mycart.classList.remove("hidden");
    fetch('/api/get-cart-by-userId')
        .then(res => res.text())
        .then(html => {
            document.getElementById("cart_component_item").innerHTML = html;
        })
        .catch(err => console.error(err));
});

// Đóng cart khi click icon X
cartCancelIcon.addEventListener("click", () => {
    mycart.classList.add("hidden");
});

// Đóng cart khi click ra ngoài
document.addEventListener("click", function (event) {
    if (mycart.classList.contains("hidden")) return;
    if (cartIcon.contains(event.target)) return;
    if (mycart.contains(event.target)) return;
    mycart.classList.add("hidden");
});

function addToCart(productId, quantity=1) {
    fetch('/api/add_to_cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == "success") {
        alert(1)
            showAlert("success", "Thông báo", data.message);
        } else {
            alert('Lỗi: ' + data.message);
        }
    })
    .catch(err => console.error(err));
}





