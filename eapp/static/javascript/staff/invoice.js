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

function renderDish(dish) {
    return `
    <div class="w-full bg-white rounded-xl shadow-md p-2">
    <div class="flex overflow-hidden rounded-lg">
        <img
                src="${dish.image}"
                class="w-full h-48 object-cover"
        >
    </div>
        <div class="mt-3 px-1">
            <p class="text-lg font-semibold text-gray-800">${dish.name}</p>
            <p class="text-base text-gray-500">${dish.price}</p>
        </div>
    </div>
    `;
}

function loadDishes(params = {}) {
    const query = new URLSearchParams(params).toString();
    fetch('/api/dish?' + query)
        .then(res => res.json())
        .then(data => {
            const dishList = document.getElementById('dish-list');
            dishList.innerHTML = '';
            dishList.innerHTML = data.map(d => renderDish(d)).join('')
            // data.forEach(d => container.innerHTML += renderDish(d));
            
        })
        .catch(err => console.error(err));
}

document.addEventListener('DOMContentLoaded', () => {
    loadDishes();
})