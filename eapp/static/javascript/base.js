/** Alert animation + style */
function showAlert(type, title, message) {
  const alertBox = document.getElementById("form_alert");
  const iconBox = document.getElementById("alert_icon");
  const textBox = document.getElementById("alert_text");

  // Reset tất cả style cũ
  alertBox.classList.remove(
    "bg-green-50","border-green-300","text-green-800",
    "bg-red-50","border-red-300","text-red-800",
    "bg-orange-50","border-orange-300","text-orange-800",
    "bg-blue-50","border-blue-300","text-blue-800"
  );

  iconBox.innerHTML = "";
  textBox.innerHTML = "";

  let bg = "", border = "", txt = "", icon = "";

  switch(type) {
    case "success":
      bg = "bg-green-50"; border = "border-green-300"; txt = "text-green-800";
      icon = `<i class="fas fa-check-circle text-green-500 text-2xl"></i>`;
      break;

    case "error":
      bg = "bg-red-50"; border = "border-red-300"; txt = "text-red-800";
      icon = `<i class="fas fa-times-circle text-red-500 text-2xl"></i>`;
      break;

    case "loading":
      bg = "bg-blue-50"; border = "border-blue-300"; txt = "text-blue-800";
      icon = `<i class="fas fa-spinner fa-spin text-blue-500 text-2xl"></i>`;
      break;

    default:
      bg = "bg-orange-50"; border = "border-orange-300"; txt = "text-orange-800";
      icon = `<i class="fas fa-exclamation-triangle text-orange-500 text-2xl"></i>`;
  }

  iconBox.innerHTML = icon;
  textBox.innerHTML = `
    <p class="font-bold mb-1">${title}</p>
    <p>${message}</p>
  `;
  alertBox.classList.add(bg, border, txt);
  alertBox.classList.remove("hidden");
  alertBox.style.opacity = "0";
  alertBox.style.transform = "translateX(15px)";

  setTimeout(() => {
    alertBox.style.transition = "0.3s ease";
    alertBox.style.opacity = "1";
    alertBox.style.transform = "translateX(0)";
  }, 10);

  // Tự động ẩn alert chỉ với success, error, warning
  if(type !== "loading") {
    setTimeout(() => {
      hideAlert();
    }, 5000);
  }
}

function hideAlert() {
  const alertBox = document.getElementById("form_alert");
  alertBox.style.opacity = "0";
  alertBox.style.transform = "translateX(15px)";

  setTimeout(() => {
    alertBox.classList.add("hidden");
  }, 300);
}


//Cart

const mycart = document.getElementById("my_cart");
const cartIcon = document.getElementById("cart_icon");
const cartCancelIcon = document.getElementById("icon_cancel_cart");

cartIcon.addEventListener("click", () => {
    mycart.classList.remove("hidden");
    fetch('/api/get-cart-by-userId')
        .then(res => res.text())
        .then(html => {
            document.getElementById("cart_component_item").innerHTML = html;
             setupQuantityControl();
        setupCheckboxEvents();   // thêm dòng này !!!
        calculateSubtotal();
        })
        .catch(err => console.error(err));

});

// Đóng cart khi click icon X
cartCancelIcon.addEventListener("click", () => {
    mycart.classList.add("hidden");
});

// Đóng cart khi click ra ngoài
document.addEventListener("click", function (event) {
    if (mycart.classList.contains("hidden")) return;
    if (cartIcon.contains(event.target)) return;
    if (mycart.contains(event.target)) return;
    mycart.classList.add("hidden");
});

function addToCart(productId, quantity=1) {
    fetch('/api/add_to_cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == "success") {
        alert(1)
            showAlert("success", "Thông báo", data.message);
        } else {
            alert('Lỗi: ' + data.message);
        }
    })
    .catch(err => console.error(err));
}

