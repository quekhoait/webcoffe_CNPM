// class Dish(BaseModel):
//     name = Column(String(100), nullable=False)
//     unit = Column(String(20), nullable=True)
//     price = Column(Float)
//     status = Column(SQLEnum(DishStatus),default=DishStatus.ACTIVE, nullable=False)
//     description = Column(String(200))
//     image = Column(String(200))
//     rating_score = Column(Float, default=5)
//     rating_count = Column(Integer, default=0)

//     dish_category_id = Column(Integer, ForeignKey(DishCategory.id), nullable=False)
// https://picsum.photos/seed/picsum/200/300

// function renderDish(dish) {
//     return `
//     <div class="dish-item w-full bg-white rounded-xl shadow-md p-2"
//     ondblclick="addToOrder(${ dish.id }, '${ dish.name }', ${ dish.price })"
//     >
//     <div class="flex overflow-hidden rounded-lg">
//         <img
//                 src="${dish.image}"
//                 class="w-full h-48 object-cover"
//         >
//     </div>
//         <div class="mt-3 px-1">
//             <p class="text-lg font-semibold text-gray-800">${dish.name}</p>
//             <p class="text-base text-gray-500">${dish.price}</p>
//         </div>
//     </div>
//     `;
// }

// function renderAlert(){
//    return `
//     <div id="alert-small-1" class="col-span-3 text-xl w-auto inline-flex items-center p-2 pe-3 mb-4 mt-4 text-fg-brand-strong rounded-full bg-brand-softer border border-brand-subtle" role="alert">
//         <span class="bg-brand-soft text-fg-brand-strong py-0.5 px-2 rounded-full">Thông Báo</span>
//         <div class="ms-2">
//             Không có món này 
//         </div>
//     </div>
// //     `
// // }

// function renderItem(data) {
//     return `
//         <div class="text-2xl grid grid-cols-6 mt-3 p-2 items-center border-b border-gray-400">
//                 <div class="col-span-3">
//                     <p class="font-semibold text-gray-800">${data.item.name}</p>
//                     <span class="text-xl text-gray-600">${data.item.price} đ</span>
//                 </div>

//                 <div class="col-span-2 flex items-center justify-center">
//                     <button class="bg-gray-200 w-10 h-10 rounded-full flex justify-center items-center"><span
//                             class="text-xl">-</span>
//                     </button>
//                     <input type="text" value="${data.item.quantity}" id="item-quantity-input-${data.item.id}" "
//                         class="w-16 h-8 text-center font-semibold border-none focus:ring-0 bg-transparent text-gray-800 ">
//                     <button class="bg-gray-200 w-10 h-10 rounded-full flex justify-center items-center"><span>+</span>
//                     </button>
//                 </div>

//                 <div class="col-span-1 text-right">
//                     <span>${data.item.price * data.total_quantity}đ</span>
//                     <button class="text-red-500 hover:text-red-700">
//                         <i class="fas fa-trash-alt"></i>
//                     </button>
//                 </div>
//             </div>
//     `
// }

// const dishCache = {}

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
        body: {},
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