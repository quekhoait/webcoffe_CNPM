document.addEventListener("DOMContentLoaded", () => {

    function cancel_form(){
        document.getElementById("form_check_password").classList.add("hidden");
        document.body.classList.remove("overflow-hidden");
    }

    function update_profile(){
        const info=document.querySelectorAll('#form_information input');

        info.forEach(input => {
            input.readOnly = false; // bỏ readOnly
        });
    }

  /** Toggle password */
  function togglePassword(inputId, iconId) {
    const pw = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    icon.parentElement.addEventListener("click", () => {
      const isPassword = pw.type === "password";
      pw.type = isPassword ? "text" : "password";

      icon.classList.toggle("fa-eye", !isPassword);
      icon.classList.toggle("fa-eye-slash", isPassword);
    });
  }
  togglePassword("current-password", "password-form-toggle-icon");

  /** Submit form */
document.getElementById("form-confirm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const currentPw = document.getElementById("current-password").value.trim();
    if (!currentPw) {
      showAlert("warning", "Thiếu mật khẩu", "Vui lòng nhập mật khẩu để tiếp tục.");
      return;
    }

    try {
        const res = await fetch("/api/check_password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: currentPw })
        });

        const data = await res.json();

        if (data.status === "success") {
            showAlert("success", "Xác nhận thành công", "Bạn có thể tiếp tục cập nhật.");
            cancel_form(); // ẩn popup
            document.getElementById("btn_update").classList.add("hidden");
            document.getElementById("btn_save").classList.remove("hidden");
            update_profile(); // bỏ readOnly input
        } else {
            showAlert("error", "Sai mật khẩu", data.message);
        }

    } catch (err) {
        console.error(err);
        showAlert("error", "Lỗi server", "Đã có lỗi xảy ra, thử lại sau.");
    }
});



  /** Cancel */
  document.getElementById("btn_cancel").addEventListener("click", () => {
    cancel_form();
  });

  /** Open update */
  document.getElementById("btn_update").addEventListener("click", () => {
    document.getElementById("form_check_password").classList.remove("hidden");
    document.body.classList.add("overflow-hidden");
  });


});
