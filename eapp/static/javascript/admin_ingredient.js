list = document.getElementById('ingredient-list')
document.getElementById('searchInput').addEventListener('input',(e) => {
    kw = e.target.value
    if (kw)
        fetch(`/api/admin/ingredients?keyword=${kw}`).then(res => res.text()).then(data => {
            list.innerHTML = data
        })
    else {
                fetch(`/api/admin/ingredients`).then(res => res.text()).then(data => {
            list.innerHTML = data
        })
    }
})
