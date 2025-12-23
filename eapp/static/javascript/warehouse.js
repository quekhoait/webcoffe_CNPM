function toggleWarehouseInput(type) {
    const destDiv = document.getElementById('dest-warehouse-div');
    const srcDiv = document.getElementById('source-warehouse-div');
    
    if (type === 'IMPORT') {
        srcDiv.classList.add('hidden');
        destDiv.classList.remove('hidden')
    } else if (type === 'UPDATE'){
        destDiv.classList.add('hidden');
        srcDiv.classList.remove('hidden')
    } else if (type === 'EXPORT'){
        destDiv.classList.add('hidden')
        srcDiv.classList.remove('hidden')
    }else{
        destDiv.classList.remove('hidden');
        srcDiv.classList.remove('hidden');
    }
}
let ingredients = []
document.addEventListener("DOMContentLoaded", async () => {
    ingredients = load_ingredients()
    createIngredientComboBoxRow();
});



console.log(document.getElementById("ingredients-container").children.length)

function createIngredientComboBoxRow() {
    const container = document.getElementById("ingredients-container");

    const rowIndex = container.children.length - 1;

    const rowHTML = `
            <div class="ingredient-row flex gap-2 relative w-full">
                <div class="relative w-[70%]">

                    <div class="flex items-center border border-gray-300 rounded-lg bg-white">
                        <input id="ingredient-input-${rowIndex}" placeholder="Chọn hoặc tìm nguyên liệu" autocomplete="off"
                            class="flex-1 p-3 outline-none" type="text">
                        <button type="button" id="toggle-button-${rowIndex}" class="px-3 text-gray-600 cursor-pointer select-none">
                            ▼
                        </button>
                    </div>

                    <div id="ingredient-dropdown-${rowIndex}"
                        class="absolute w-full bg-white border border-gray-200 rounded-lg shadow-md hidden max-h-60 overflow-auto z-20">
                    </div>
                </div>

                <input id="ingredient-quantity-${rowIndex}" type="number" name="quantity" placeholder="SL"
                    class="w-[30%] p-3 border border-gray-300 rounded-lg outline-none text-center" required>
                <button type="button" class="delete-row hidden p-3 text-red-500 hover:text-red-700">
                ✕
                </button>
            </div>
    `

    container.insertAdjacentHTML("beforeend", rowHTML)

    const input = document.getElementById(`ingredient-input-${rowIndex}`)
    const dropdown = document.getElementById(`ingredient-dropdown-${rowIndex}`)
    const toggleBtn = document.getElementById(`toggle-button-${rowIndex}`)
    const quantity = document.getElementById(`ingredient-quantity-${rowIndex}`)

    const newRow = container.querySelector(".ingredient-row:last-child");
    const deleteBtn = newRow.querySelector(".delete-row");

    deleteBtn.addEventListener("click", () => {
        newRow.remove();
    });

    input.addEventListener('input', () => {
        showDropdown(input, dropdown)
    })

    toggleBtn.addEventListener("click", () => {
        if (dropdown.classList.contains("hidden")) showDropdown(input, dropdown);
        else hideDropdown(dropdown);
    });

    dropdown.addEventListener("click", e => {
        const item = e.target.closest("[data-id]");
        if (item) {
            input.value = item.dataset.value;
            input.dataset.id = item.dataset.id;
            hideDropdown(dropdown);

            const lastRow = container.querySelector(".ingredient-row:last-child");

            const nameInput = lastRow.querySelector("input[type=text]");
            const quantityInput = lastRow.querySelector("input[type=number]");


            quantityInput.focus()
            if (nameInput.value) {
                createIngredientComboBoxRow();
            }
        }
    });

}

function load_ingredients(params = {}) {
    const URLparams = new URLSearchParams(params).toString()
    fetch("/api/ingredients?" + URLparams, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        ingredients = data
    }).catch(err => console.log(err))
}


function showDropdown(input, dropdown) {
    dropdown.classList.remove("hidden");
    renderListComboBox(input.value, dropdown);
}

function hideDropdown(dropdown) {
    dropdown.classList.add("hidden");
}

function renderListComboBox(keyword, dropdown) {
    const kw = keyword.toLowerCase();
    const selectedIds = getSelectedIngredientIds();

    const results = ingredients.filter(i =>
        i.name.toLowerCase().includes(kw) &&
        !selectedIds.includes(String(i.id))
    );

    dropdown.innerHTML =
        results.length === 0
            ? `<div class="p-3 text-gray-500">Không tìm thấy</div>`
            : results.map(i => `
                <div class="p-3 hover:bg-gray-100 cursor-pointer"
                    data-id="${i.id}"
                    data-value="${i.name}">
                    ${i.name} (${i.unit})
                </div>
            `).join("");
}


document.getElementById('toggle-edit-button').addEventListener('click', e => {
    buttons = document.querySelectorAll('#ingredients-container .ingredient-row .delete-row')
    
    const isShow = e.target.classList.toggle('show');

    buttons.forEach(btn => {
        if (isShow) btn.classList.remove('hidden');
        else btn.classList.add('hidden');
    });
})


document.addEventListener("click", e => {
    // Lấy tất cả dropdown
    document.querySelectorAll(".ingredient-row div.absolute").forEach(dd => {
        const input = dd.closest(".ingredient-row").querySelector("input");
        const toggleBtn = dd.closest(".ingredient-row").querySelector("button");

        // Nếu click ngoài dropdown, input, toggleBtn thì ẩn dropdown
        if (!dd.contains(e.target) && e.target !== input && e.target !== toggleBtn) {
            hideDropdown(dd);
        }
    });
});


// """
// slip_data:
//     slip_type
//     note
//     stock_user_id
//     invoice_id (option)
//     destination_warehouse_id
//     source_warehouse_id
//     ingredients (list)
//         ingredient_id
//         quantity
// """
function createWarehouseSlip(){
    const slipType = document.getElementById("slip-type").value;
    const destinationWarehouseId = document.querySelector("#dest-warehouse-div:not(.hidden) select")?.value ?? null;
    const sourceWarehouseId = document.querySelector("#source-warehouse-div:not(.hidden) select")?.value ?? null;
    const note = document.getElementById("note").value;
    
    const ingredients = Array.from(document.querySelectorAll(".ingredient-row:not(:last-child)")).map(row => {
        const input = row.querySelector("input[type=text]");
        const quantityInput = row.querySelector("input[type=number]");
        return {
            ingredient_id: input.dataset.id,
            quantity: parseFloat(quantityInput.value) || 0
        };
    })

    const slipData = {
        slip_type: slipType,
        note: note,
        destination_warehouse_id: destinationWarehouseId,
        source_warehouse_id: sourceWarehouseId,
        ingredients: ingredients
    };

    fetch("/api/warehouse-slips", {
        method: "POST",
        body: JSON.stringify(slipData),
        headers: {
            "Content-Type": "application/json"
        },
    }).then(res => res.json()).then(data => {
        if (data.success) {
            alert("Tạo phiếu kho thành công!");
            window.location.reload();
        } else {
            alert("Lỗi khi tạo phiếu kho: " + data.message);
        }}
    )
}

function getSelectedIngredientIds() {
    return Array.from(document.querySelectorAll(".ingredient-row input[type=text]"))
        .map(input => input.dataset.id)
        .filter(Boolean); // loại null / undefined
}
