//qli cthuc
function addRecipeRow(data = null) {
    const container = document.getElementById('recipeContainer');
    const template = document.getElementById('recipe-row-template');

    const clone = template.content.cloneNode(true);
    const row = clone.querySelector('.recipe-row');

    const rowId = Date.now();
    row.id = `row-${rowId}`;


    const zIndex = 1000 - container.children.length;
    row.style.zIndex = zIndex;


    const inputSearch = row.querySelector('.ing-search-input');
    const inputId = row.querySelector('.ing-id');
    const inputQty = row.querySelector('.ing-qty');
    const inputUnit = row.querySelector('.ing-unit');
    const dropdown = row.querySelector('.ing-dropdown');
    const toggleBtn = row.querySelector('.toggle-btn');
    const deleteBtn = row.querySelector('.delete-row');


    if (data && typeof ALL_INGREDIENTS !== 'undefined') {
        const found = ALL_INGREDIENTS.find(i => i.id == data.ingredient_id);
        if (found) {
            inputSearch.value = found.name;
            inputId.value = found.id;
            inputUnit.value = found.unit;
        }
        inputQty.value = data.quantity;
    }


    //nhập tìm kiếm
    inputSearch.addEventListener('input', () => {
        showDropdown(inputSearch, dropdown);
        if(inputSearch.value.trim() === "") {
            inputId.value = "";
            inputUnit.value = "";
        }
    });

    //focus vào ô tìm kiếm
    inputSearch.addEventListener('focus', () => {
        //tự động bôi đen toàn bộ text để dễ sửa
        inputSearch.select();
    });

    //nút mũi tên xổ xuống
    toggleBtn.addEventListener('click', () => {
        if (dropdown.classList.contains("hidden")) {
            showDropdown(inputSearch, dropdown);
        } else {
            hideDropdown(dropdown);
        }
    });

    //chọn item trong dropdown
    dropdown.addEventListener('click', (e) => {
        const item = e.target.closest(".dropdown-item");
        if (item) {
            inputSearch.value = item.dataset.name;
            inputId.value = item.dataset.id;
            inputUnit.value = item.dataset.unit;

            hideDropdown(dropdown);
            inputQty.focus();
        }
    });

    //xóa dòng
    deleteBtn.addEventListener('click', () => {
        row.remove();
    });


    container.appendChild(row);
}



function showDropdown(input, dropdown) {
    //đóng các dropdown khác
    document.querySelectorAll('.ing-dropdown').forEach(d => d.classList.add('hidden'));

    dropdown.classList.remove("hidden");

    dropdown.style.zIndex = "9999";

    renderListComboBox(input.value, dropdown);
}

function hideDropdown(dropdown) {
    dropdown.classList.add("hidden");
}

function renderListComboBox(keyword, dropdown) {
    const kw = keyword.toLowerCase();
    const results = ALL_INGREDIENTS.filter(i => i.name.toLowerCase().includes(kw));

    if (results.length === 0) {
        dropdown.innerHTML = `<div class="p-3 text-sm text-gray-400 italic text-center">Không tìm thấy</div>`;
    } else {

        dropdown.innerHTML = results.map(i => `
            <div class="dropdown-item p-2 hover:bg-yellow-50 cursor-pointer text-sm border-b border-gray-50 text-gray-700 flex justify-between items-center"
                 data-id="${i.id}"
                 data-name="${i.name}"
                 data-unit="${i.unit}">
                <span class="font-medium">${i.name}</span>
                <span class="text-xs text-gray-400">(${i.unit})</span>
            </div>
        `).join("");
    }
}


document.addEventListener("click", e => {
    if (!e.target.closest('.recipe-row')) {
        document.querySelectorAll('.ing-dropdown').forEach(el => el.classList.add('hidden'));
    }
});

function openModal(mode, product = null) {
    const modal = document.getElementById('productModal');
    modal.classList.remove('hidden');
    //hiệu ứng scale
    setTimeout(() => {
        modal.firstElementChild.classList.remove('scale-95');
        modal.firstElementChild.classList.add('scale-100');
    }, 10);

    const container = document.getElementById('recipeContainer');
    container.innerHTML = '';

    if (mode === 'ADD') {
        document.getElementById('modalTitle').innerText = "Thêm Món Mới";
        document.getElementById('inpId').value = "";
        document.getElementById('inpName').value = "";
        document.getElementById('inpPrice').value = "";
        document.getElementById('inpUnit').value = "";
        document.getElementById('inpDesc').value = "";
        document.getElementById('inpCategory').selectedIndex = 0;
        document.getElementById('previewImage').classList.add('hidden');

        addRecipeRow(); //thêm dòng trống
    } else {
        document.getElementById('modalTitle').innerText = "Cập Nhật Món";
        document.getElementById('inpId').value = product.id;
        document.getElementById('inpName').value = product.name;
        document.getElementById('inpPrice').value = product.price;
        document.getElementById('inpUnit').value = product.unit;
        document.getElementById('inpCategory').value = product.category_id;
        document.getElementById('inpDesc').value = product.description;

        if (product.image) {
            document.getElementById('previewImage').src = product.image;
            document.getElementById('previewImage').classList.remove('hidden');
        } else {
            document.getElementById('previewImage').classList.add('hidden');
        }

        //load công thức cũ
        if (product.ingredients && product.ingredients.length > 0) {
            product.ingredients.forEach(r => {
                addRecipeRow({
                    ingredient_id: r.ingredient_id,
                    quantity: r.quantity
                });
            });
        } else {
            addRecipeRow();
        }
    }
}

function closeModal() {
    const modal = document.getElementById('productModal');
    modal.classList.add('hidden');
    modal.firstElementChild.classList.add('scale-95');
    modal.firstElementChild.classList.remove('scale-100');
}

async function saveProduct() {
    let fd = new FormData();
    fd.append('id', document.getElementById('inpId').value);
    fd.append('name', document.getElementById('inpName').value);
    fd.append('price', document.getElementById('inpPrice').value);
    fd.append('unit', document.getElementById('inpUnit').value);
    fd.append('category_id', document.getElementById('inpCategory').value);
    fd.append('description', document.getElementById('inpDesc').value);

    const imgFile = document.getElementById('inpImage').files[0];
    if (imgFile) fd.append('image', imgFile);


    let recipes = [];
    document.querySelectorAll('.recipe-row').forEach(row => {

        let id = row.querySelector('.ing-id').value;
        let qty = row.querySelector('.ing-qty').value;
        let unit = row.querySelector('.ing-unit').value;

        if (id && qty > 0) {
            recipes.push({ ingredient_id: id, quantity: qty, unit: unit });
        }
    });
    fd.append('recipes', JSON.stringify(recipes));

    if (!document.getElementById('inpName').value || !document.getElementById('inpPrice').value) {
        alert("Vui lòng nhập tên món và giá bán!");
        return;
    }

    const url = fd.get('id') ? '/api/admin/product/update' : '/api/admin/product/add';

    try {
        const res = await fetch(url, { method: 'POST', body: fd });
        const data = await res.json();
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Lỗi: ' + data.message);
        }
    } catch (err) {
        alert('Lỗi kết nối server!');
    }
}

function deleteProduct(id) {
    if (!confirm('Bạn chắc chắn muốn xóa món này?')) return;
    fetch('/api/admin/product/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
    }).then(r => r.json()).then(d => {
        if (d.success) location.reload(); else alert(d.message);
    });
}