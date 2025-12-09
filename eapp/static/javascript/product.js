

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

function addToCart(productId) {
    fetch('/api/add-to-cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Đã thêm vào giỏ hàng!');
            location.reload();
        } else { alert('Lỗi: ' + data.message); }
    });
}