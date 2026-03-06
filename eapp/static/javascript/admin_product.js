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
//Mở model product
function openModal(mode, product = null) {
    const modal = document.getElementById('productModal');
    modal.classList.remove('hidden');
    setTimeout(() => { modal.firstElementChild.classList.remove('scale-95'); modal.firstElementChild.classList.add('scale-100'); }, 10);

    const container = document.getElementById('recipeContainer');
    container.innerHTML = '';

    if (mode === 'ADD') {
        document.getElementById('modalTitle').innerText = "Thêm Món Mới";
        // Reset form
        document.getElementById('inpId').value = "";
        document.getElementById('inpName').value = "";
        document.getElementById('inpPrice').value = "";
        document.getElementById('inpUnit').value = "";
        document.getElementById('inpDesc').value = "";
        document.getElementById('previewImage').classList.add('hidden');

        // reset danh mục mới
        document.getElementById('inpCategory').value = "";
        document.getElementById('inpCategoryName').value = "";

        addRecipeRow();
    } else {
        document.getElementById('modalTitle').innerText = "Cập Nhật Món";
        document.getElementById('inpId').value = product.id;
        document.getElementById('inpName').value = product.name;
        document.getElementById('inpPrice').value = product.price;
        document.getElementById('inpUnit').value = product.unit;
        document.getElementById('inpDesc').value = product.description;

        //set danh mục mới
        document.getElementById('inpCategory').value = product.category_id || product.dish_category_id;

        if (typeof ALL_CATEGORIES !== 'undefined') {
            const catId = product.category_id || product.dish_category_id;
            const cat = ALL_CATEGORIES.find(c => c.id == catId);
            document.getElementById('inpCategoryName').value = cat ? cat.name : "";
        }

        // ảnh
        if (product.image) {
            document.getElementById('previewImage').src = product.image;
            document.getElementById('previewImage').classList.remove('hidden');
        } else {
            document.getElementById('previewImage').classList.add('hidden');
        }

        // công thức
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


        if (id && qty > 0) {
            recipes.push({ ingredient_id: id, quantity: qty });
        }
    });
    fd.append('recipes', JSON.stringify(recipes));
        console.log(fd.get('recipes'))
        if (!fd.get('name') ||!fd.get('price') ||!fd.get('unit') || !fd.get('category_id')||!fd.get('description')) {
            showAlert("error", "Thông báo", "Vui lòng nhập đầy đủ thông tin món!");
            return;
        }
        if(recipes.length===0){
              showAlert("error", "Thông báo","Chưa ghi công thức!");
            return;
        }


    const url = fd.get('id') ? '/api/admin/product/update' : '/api/admin/product/add';
  showAlert("loading", "Đang lưu", "Vui lòng chờ...");
    try {
        const res = await fetch(url, { method: 'POST', body: fd });
        const data = await res.json();

        if (data.success) {

             showAlert("success", "Thông báo", "Lưu thành công");
            window.location.reload();
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

function toggleCatDropdown() {
    const dropdown = document.getElementById('cat-dropdown');
    if (dropdown.classList.contains('hidden')) {

        document.querySelectorAll('.ing-dropdown').forEach(d => d.classList.add('hidden'));
        dropdown.classList.remove('hidden');
    } else {
        dropdown.classList.add('hidden');
    }
}

function selectCategory(id, name) {

    document.getElementById('inpCategory').value = id;
    document.getElementById('inpCategoryName').value = name;

    document.getElementById('cat-dropdown').classList.add('hidden');
}

document.addEventListener("click", e => {

    if (!e.target.closest('#cat-container')) {
        const catDrop = document.getElementById('cat-dropdown');
        if(catDrop) catDrop.classList.add('hidden');
    }

    if (!e.target.closest('.recipe-row')) {
        document.querySelectorAll('.ing-dropdown').forEach(el => el.classList.add('hidden'));
    }
});


function toggleFilterDropdown() {
    const d = document.getElementById('filter-dropdown');

    const otherDrops = document.querySelectorAll('.ing-dropdown, #cat-dropdown');
    otherDrops.forEach(el => el.classList.add('hidden'));

    if (d.classList.contains('hidden')) {
        d.classList.remove('hidden');
    } else {
        d.classList.add('hidden');
    }
}

function selectFilter(id, name) {

    document.getElementById('inpFilterName').value = name;
    document.getElementById('filter-dropdown').classList.add('hidden');

    filterTableData(name);
}


function filterTableData(categoryName) {
    const rows = document.querySelectorAll('tbody tr'); // Lấy tất cả dòng trong bảng
    const keyword = document.getElementById('searchInput').value.toLowerCase();

    rows.forEach(row => {

        const productName = row.querySelector('td:nth-child(1) .font-bold').innerText.toLowerCase();

        const categoryCell = row.querySelector('td:nth-child(3)');
        const rowCategory = categoryCell ? categoryCell.innerText.trim() : "";

        const matchCategory = (categoryName === 'Tất cả loại' || rowCategory === categoryName);
        const matchKeyword = productName.includes(keyword);

        if (matchCategory && matchKeyword) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}


function searchTable() {

    const currentCategory = document.getElementById('inpFilterName').value;
    filterTableData(currentCategory);
}


document.addEventListener("click", e => {

    if (!e.target.closest('.recipe-row')) {
        document.querySelectorAll('.ing-dropdown').forEach(el => el.classList.add('hidden'));
    }

    if (!e.target.closest('#cat-container')) {
        const catDrop = document.getElementById('cat-dropdown');
        if(catDrop) catDrop.classList.add('hidden');
    }

    if (!e.target.closest('#filter-container')) {
        const filterDrop = document.getElementById('filter-dropdown');
        if(filterDrop) filterDrop.classList.add('hidden');
    }
});

async function addQuickCategory() {
    const nameInput = document.getElementById('inpNewCatName');
    const desInput = document.getElementById('inpNewCatDes');

    const name = nameInput.value.trim();
    const des = desInput.value.trim();
    if (!name || !des) {
        showAlert("error", "Thông báo", "Vui lòng nhập đầy đủ thông tin");
        return;
    }
    const url = id_cate_click
        ? "/api/admin/category/update"
        : "/api/admin/category/add";

    const payload = id_cate_click
        ? { id: id_cate_click, name: name, description: des }
        : { name: name, description: des };

    try {
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            showAlert(
                "success",
                "Thông báo",
                id_cate_click ? "Cập nhật thành công!" : "Thêm danh mục thành công!"
            );

            setTimeout(() => location.reload(), 1000);
        } else {
            showAlert("error", "Thông báo", data.message);
        }
    } catch (err) {
        console.error(err);
        showAlert("error", "Thông báo", "Lỗi kết nối server");
    }
}

let id_cate_click=null;
document.querySelectorAll(".btn_edit_cate").forEach(btn => {
    btn.addEventListener("click", function () {
        id_cate_click = this.dataset.id
        document.getElementById("inpNewCatName").value = this.dataset.name;
        document.getElementById("inpNewCatDes").value = this.dataset.desc;
    });
});