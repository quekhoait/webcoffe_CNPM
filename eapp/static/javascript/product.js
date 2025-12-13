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





