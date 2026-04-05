async function saveIngredient() {
//    const id = document.getElementById('inpId_ingre').value;
    const name = document.getElementById('inpName_ingre').value.trim();
    const price = document.getElementById('inpPrice_ingre').value.trim();
    const unit = document.getElementById('inpUnit_ingre').value.trim();
    const description = document.getElementById('inpDesc_ingre').value.trim();

    if (!name || !price || !unit || !description) {
        alert("Vui lòng nhập đầy đủ thông tin!");
        return;
    }
    const url = '/api/admin/ingredient/add'
    const data = {
        name: name,
        price: price,
        unit: unit,
        description: description
    };
    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await res.json();

        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert("Lỗi: " + result.message);
        }
    } catch (err) {
        alert("Lỗi kết nối đến Server!");
        console.error(err);
    }
}

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