function loadDishes(params = {}) {
    const query = new URLSearchParams(params).toString();
    const productList = document.getElementById('product-list');

    fetch('/api/products?' + query)
        .then(res => res.text())
        .then(html => {
            console.log(html);
            productList.innerHTML = html
        })
        .catch(err => console.error(err));
}

document.querySelectorAll('#category-list button').forEach(ele => {
    ele.addEventListener('click', (e) => {
        document.querySelectorAll('#category-list button').forEach(btn => {
            btn.classList.remove('active-category')
            btn.classList.add('inactive-category')
        })
        e.target.classList.add('active-category')
        e.target.classList.remove('inactive-category')
        cateId = ele.dataset?.id
        params = cateId
            ? { 'category_id': parseInt(cateId) }
            : {}
        loadDishes(params)
    })
})

document.getElementById('search-input').addEventListener('input', (e) => {
    console.log(e.target.value);

    loadDishes({ 'name': e.target.value })
})


function addToOrder(id, name, price, bonusQuantity = 1, setQuantity = false) {
    const dish = document.getElementById(`invoice-item-${id}`)

    if (dish && !setQuantity) {
        const currentQty = parseInt(dish.querySelector('input').value)
        messageError = isInvalidValue(currentQty, bonusQuantity)
        if (messageError) {
            alert(messageError)
            return;
        }
    }

    fetch('/api/order', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price,
            "bonus_quantity": bonusQuantity,
            "is_set_quantity": setQuantity
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (!data.success) {
            if (data.ingredient_insufficient && data.ingredient_insufficient.length > 0) {
                alert("Nguyên liệu không đủ cho số lượng hiện tại.\n" +
                    "Bạn chỉ có thể làm tối đa: " + data.makeable_quantity + " món.");
                if (dish)
                    dish.querySelector('input').value = data.item.quantity
            } else {
                alert(data.message);
            }
            return;
        }

        if (dish) {
            dish.querySelector('input').value = data.item.quantity
            dish.querySelector(`#invoice-item-price-${id}`).innerText = data.item.quantity * data.item.price + ' đ';
        } else {

            orderItem = document.querySelector('.list-order-item')
            orderItem.insertAdjacentHTML('beforeend', data.item_html)
        }


        document.getElementById("total-price").innerText = data.total_price + ' đ';
        document.getElementById("total-price-tmp").innerText = data.total_price_tmp + ' đ';
    })
}


function removeItemFromInvoice(id) {
    fetch('/api/remove-item', {
        method: 'post',
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        document.getElementById(`invoice-item-${id}`).remove()

        document.getElementById("total-price").innerText = data.total_price + ' đ';
        document.getElementById("total-price-tmp").innerText = data.total_price_tmp + ' đ';
    })
}

function submitInvoice() {
    socket.emit('send', { msg: 'OK da gui', warehouse_id: 1 });

    orderItem = document.querySelector('.list-order-item')
    if (!orderItem || orderItem.children.length === 0) {
        alert("Hóa đơn phải có ít nhất 1 món")
        return;
    }
    fetch('/api/invoice', {
        method: 'post',
        body: JSON.stringify({
            'staff_id': 1
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        orderItem = document.querySelector('.list-order-item')

        orderItem.innerHTML = ""
        document.getElementById("total-price").innerText = 0;
        document.getElementById("total-price-tmp").innerText = 0;
        alert("Lập hóa đơn thành công!")
    })
}

function clearInvoice() {
    fetch('/api/invoices', {
        method: 'delete'
    }).then(res => res.json()).then(data => {
        orderItem = document.querySelector('.list-order-item')
        orderItem.innerHTML = ""
        document.getElementById("total-price").innerText = 0;
        document.getElementById("total-price-tmp").innerText = 0;
        alert("Xóa hóa đơn thành công!")
    })
}

function inputQuantity(id, name, price, element) {
    messageError = isInvalidValue(null, element.value)
    if (messageError) {
        alert(messageError)
        element.value = 1
    }
    addToOrder(id, name, price, element.value, true)
}

function isInvalidValue(currentValue, newValue) {
    let message = null
    const parsed = Number(newValue)
    if (!Number.isInteger(parsed)) {
        message = "Vui lòng nhập 1 số nguyên"
    } else if (currentValue == null && parsed <= 0) {
        message = "Vui lòng nhập số hơn 0"
    } else if (currentValue + parsed <= 0) {
        message = "Số lượng phải lớn hơn 0"
    }
    return message
}


