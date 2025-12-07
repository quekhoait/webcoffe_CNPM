
function setupQuantityControl(wrapper) {
    const qtyDisplay = wrapper.querySelector('.qty-display');
    const minusBtn = wrapper.querySelector('.minus-btn');
    const plusBtn = wrapper.querySelector('.plus-btn');

    if (!qtyDisplay || !minusBtn || !plusBtn) {
        console.error('Lỗi: Không tìm thấy các phần tử điều khiển số lượng trong wrapper.');
        return;
    }

    let currentQuantity = parseInt(qtyDisplay.textContent) || 1; 

    const updateDisplay = () => {
        qtyDisplay.textContent = currentQuantity;
        // Vô hiệu hóa nút trừ nếu số lượng = 1
        minusBtn.disabled = currentQuantity <= 1;
        minusBtn.style.opacity = currentQuantity <= 1 ? 0.5 : 1;
    };

    // Xử lý nút tăng
    plusBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn chặn hành vi mặc định (ví dụ: submit form)
        currentQuantity++;
        updateDisplay();
    });

    // Xử lý nút giảm
    minusBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn chặn hành vi mặc định
        if (currentQuantity > 1) {
            currentQuantity--;
            updateDisplay();
        }
    });
    updateDisplay(); 
}

document.addEventListener('DOMContentLoaded', () => {
    const allControls = document.querySelectorAll('.quantity-control-wrapper');

    allControls.forEach(controlWrapper => {
        setupQuantityControl(controlWrapper);
    });
});