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