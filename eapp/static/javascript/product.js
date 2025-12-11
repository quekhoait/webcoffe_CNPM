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


//Tính số tiền
function calculateSubtotal() {
    let total = 0;
    const items = document.querySelectorAll('.cart-component-item');
    console.log(items)
    items.forEach(item => {
        const checkbox = item.querySelector('.select-cart-component');
        const price = parseFloat(item.querySelector('p.price').innerText);
        const qty = parseInt(item.querySelector('span.qty-display').innerText);
        console.log(price)
        if (checkbox.checked) {
            total += price * qty;
        }
    });
   document.getElementById('subTotal-cart').innerText = total;
}

function setupCheckboxEvents() {
    const checkboxes = document.querySelectorAll('.select-cart-component');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            calculateSubtotal();
        });
    });
}

function setupQuantityControl() {
    const controls = document.querySelectorAll('.quantity-control-wrapper');
    controls.forEach(control => {
        const minusBtn = control.querySelector('.minus-btn');
        const plusBtn = control.querySelector('.plus-btn');
        const qtyDisplay = control.querySelector('.qty-display');

        if (!minusBtn || !plusBtn || !qtyDisplay) return;
        let currentQty = parseInt(qtyDisplay.textContent) || 1;
        function update() {
            qtyDisplay.textContent = currentQty;
            minusBtn.disabled = currentQty <= 1;
            minusBtn.style.opacity = currentQty <= 1 ? 0.5 : 1;
        }

        plusBtn.onclick = () => {
            currentQty++;
            update();
            calculateSubtotal()
        };

        minusBtn.onclick = () => {
            if (currentQty > 1) {
                currentQty--;
                update();
                calculateSubtotal()
            }
        };
        update();
    });
}


