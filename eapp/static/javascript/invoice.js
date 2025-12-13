
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

    fetch('/api/order', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price,
            "bonus_quantity": bonusQuantity,
            "is_set_quantity" : setQuantity
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        
        const dish = document.getElementById(`invoice-item-${id}`)
        
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

function removeItemFromInvoice(id){
    fetch('api/remove-item',{
        method : 'post',
        body : JSON.stringify({
            "id" : id
        }),
        headers : {
            "Content-Type" : "application/json"
        }
    }).then(res => res.json()).then(data => {
        document.getElementById(`invoice-item-${id}`).remove()
        
        document.getElementById("total-price").innerText = data.total_price + ' đ';
        document.getElementById("total-price-tmp").innerText = data.total_price_tmp + ' đ';
    })
}

function submitInvoice() {
    fetch('/api/invoice', {
        method: 'post',
        body: JSON.stringify({
            'staff_id' : 1
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
    fetch('/api/invoice', {
        method: 'delete'
    }).then(res => res.json()).then(data => {
        orderItem = document.querySelector('.list-order-item')
        orderItem.innerHTML = ""
        document.getElementById("total-price").innerText = 0;
        document.getElementById("total-price-tmp").innerText = 0;
        alert("Xóa hóa đơn thành công!")
    })
}

function inputQuantity(id,name,price,element){
    addToOrder(id,name,price,element.value,true)
}