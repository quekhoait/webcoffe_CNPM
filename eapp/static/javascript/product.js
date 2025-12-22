
function loadProducts(params = {}) {
    const query = new URLSearchParams(params).toString();
    const productList = document.getElementById('menu-product-items')
    fetch('/api/get_product?' + query)
        .then(res => res.text())
        .then(html => {
        console.log(html)
            productList.innerHTML = html

        })
        .catch(err => console.error(err));

}

const searchProduct = document.getElementById('search-product')
    if(searchProduct){
        searchProduct.addEventListener('input', (e) => {
            loadProducts({ 'name': e.target.value })
        })
    }



document.getElementById("btn_payment").addEventListener("click", () => {
    const cartItems = document.querySelectorAll('.cart-component-item-popup');
    const selectedItems = getSelectedItems(cartItems);
    if (selectedItems.length === 0) {
        showAlert("warning", "Thông báo", "Vui lòng chọn ít nhất 1 sản phẩm");
        return;
    }
    fetch("/payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(selectedItems)
    })
    .then(() => {
         window.location.href = "/payment";
    });

});


function getSelectedItems(cartItems) {
    let selectedItems = [];
    cartItems.forEach(item => {
        const checkbox = item.querySelector('.select-cart-component');
        if (!checkbox || !checkbox.checked) return;
        selectedItems.push({
            product_id: item.dataset.productId,
            quantity: parseInt(item.querySelector('.qty-display').innerText),
        });
    });
    return selectedItems;
}


//Tiến hành thanh toán
document.getElementById("btn-accept-payment").addEventListener("click",()=> {
 const note = document.getElementById("order-note").value;

    const paymentMethod = document.querySelector(
        'input[name="payment_method"]:checked'
    )?.value;
      fetch("/api/created_payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
         body: JSON.stringify({
            note: note,
            payment_method: paymentMethod
        })
    })
    .then(res => res.json()).then(data => {
          if (data.status === "success") {
           window.open(data.pay_url, "_blank");
        } else {
            alert(data.message);
        }
    });
})






