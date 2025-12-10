

document.addEventListener('DOMContentLoaded', function() {
    const header = document.getElementById('header');
    const scrolledClass = 'scrolled-header';

    function toggleHeaderBackground() {
        if (window.scrollY > 50) {
            // SỬA: Thêm class CSS
            header.classList.add(scrolledClass);
            header.classList.add("fixed")
        } else {
            header.classList.remove(scrolledClass);
            header.classList.remove("fixed")
        }
    }
    window.addEventListener('scroll', toggleHeaderBackground);
    toggleHeaderBackground();
});

document.addEventListener('DOMContentLoaded', function() {
    // Hàm cuộn slider
    window.scrollProducts = function(direction) {
        const slider = document.getElementById('productSlider');

        if (!slider) {
            console.error("Không tìm thấy phần tử có ID 'productSlider'.");
            return;
        }
        const firstItem = slider.querySelector('.flex-shrink-0');
        if (!firstItem) {
            console.error("Không tìm thấy item sản phẩm bên trong slider.");
            return;
        }
        const gapSize = 16;
        const itemWidth = firstItem.offsetWidth;
        const scrollAmount = slider.clientWidth;
        slider.scrollBy({
            left: direction * scrollAmount,
            behavior: 'smooth'
        });
    };
});