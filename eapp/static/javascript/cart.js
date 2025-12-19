//Thanh toán lại
document.getElementById("btn-repay-payment").addEventListener("click",function(event) {
        event.stopPropagation();
      fetch("/api/repay_payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        invoice_id: this.dataset.invoiceId
    })
    })
    .then(res => res.json()).then(data => {
          if (data.status === "success") {
           window.open(data.pay_url, "_blank");
        } else {
            alert(data.message);
        }
    });
})



//xóa sản phảm trong cart

document.querySelectorAll(".btn-remove-product-cart").forEach(btn => {
    btn.addEventListener("click", function () {
        const productId = this.dataset.productId;
        console.log("id:", productId);

        fetch("/api/remove_prod_in_cart", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                product_id: productId
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                showAlert("success","Thông báo", "Xóa sản phẩm thành công")
                location.reload(); // reload cart
            } else {
                alert(data.message);
            }
        });
    });
});
