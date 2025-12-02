
function loadDishes(params = {}) {
    const query = new URLSearchParams(params).toString();
    const dishList = document.getElementById('dish-list');

    // if (dishCache[query]) {
    //     dishList.innerHTML = dishCache[query].map(renderDish).join('')
    //     return
    // }

    fetch('/api/dish?' + query)
        .then(res => res.text())
        .then(html => {
            dishList.innerHTML = html

            // if(Object.keys(data).length === 0){
            //     console.log('empty');
            //     dishList.innerHTML = renderAlert()
            //     return;
            // }

            // dishList.innerHTML = data.map(d => renderDish(d)).join('')
            // data.forEach(d => container.innerHTML += renderDish(d));
        })
        .catch(err => console.error(err));
}

document.querySelectorAll('#category-list button').forEach(ele => {
    ele.addEventListener('click', () => {
        cateId = ele.dataset?.id
        params = cateId
            ? { 'dish_category_id': parseInt(cateId) }
            : {}
        loadDishes(params)
    })
})

document.getElementById('search-input').addEventListener('change', (e) => {
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
        // location.reload()
        alert("OKK")
    })
}

function inputQuantity(id,name,price,element){
    addToOrder(id,name,price,element.value,true)
}