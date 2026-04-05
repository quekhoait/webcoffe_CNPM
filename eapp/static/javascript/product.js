
function loadProducts(params = {}) {
    const query = new URLSearchParams(params).toString();
    const productList = document.getElementById('menu-product-items')
    fetch('/api/get_product?' + query)
        .then(res => res.text())
        .then(html => {
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


function cartToPayment(btn, cartSelector){
if (!btn) {
      return; }
  btn.addEventListener("click", () => {
    // Lấy các item popup lúc click
    const cartItems = document.querySelectorAll(cartSelector);
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
    .then(res => res.json())
    .then(data => {
        if (data.status === "error") {
            showAlert("error", "Không thể thanh toán", data.message);
            return;
        }
        window.location.href = "/payment";
    })
    .catch(err => {
        console.error(err);
        showAlert("error", "Lỗi", err.message || "Lỗi xảy ra");
    });
  });
}

// Chỉ truyền selector, NodeList sẽ được lấy khi click



function getSelectedItems(cartItems) {
    let selectedItems = [];
    cartItems.forEach(item => {
        const checkbox = item.querySelector('.select-cart-component');
        if (!checkbox || !checkbox.checked) return;
        selectedItems.push({
            product_id: item.dataset.productId || checkbox.dataset.productId,
            quantity: parseInt(item.querySelector('.qty-display').innerText),
        });
    });
    return selectedItems;
}

cartToPayment(document.getElementById("btn_payment_popup"), ".cart-component-item-popup");
cartToPayment(document.getElementById("btn_payment"), ".cart-component-item");

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
                window.location.replace(data.pay_url);
        } else {
            showAlert("error", "Thông báo", data.message)
            return;
        }
    });
})


//Truy cập product detail
function handleProductClick(id){
   window.location.href = `/product/${id}`;
}



