document.addEventListener("DOMContentLoaded", () => {

  /** ----- Các hàm tiện ích ----- */

  // Ẩn popup xác nhận mật khẩu
  function cancel_form() {
    const formCheck = document.getElementById("form_check_password");
    if (formCheck) formCheck.classList.add("hidden");
    document.body.classList.remove("overflow-hidden");
  }


  function update_profile(flag) {
    const info = document.querySelectorAll('#form_information_profile input');
    info.forEach(input => {
      input.readOnly = flag;
      if (input.type == 'file') {
        input.disabled = flag;
      }
    })
  }

  // Hiển thị/ẩn password
  function togglePassword(inputId, iconId) {
    const pw = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    if (!pw || !icon) return;

    icon.parentElement.addEventListener("click", () => {
      const isPassword = pw.type === "password";
      pw.type = isPassword ? "text" : "password";
      icon.classList.toggle("fa-eye", !isPassword);
      icon.classList.toggle("fa-eye-slash", isPassword);
    });
  }

  togglePassword("current-password", "password-form-toggle-icon");

  /** ----- Xác nhận mật khẩu trước khi mở edit ----- */
  const formConfirm = document.getElementById("form-confirm");
  if (formConfirm) {
    formConfirm.addEventListener("submit", async (e) => {
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
          cancel_form();
          document.getElementById("btn_update").classList.add("hidden");
          document.getElementById("btn_save_profile").classList.remove("hidden");
          update_profile(false); // mở input
          formConfirm.reset();
        } else {
          showAlert("error", "Sai mật khẩu", data.message);
        }

      } catch (err) {
        console.error(err);
        showAlert("error", "Lỗi server", "Đã có lỗi xảy ra, thử lại sau.");
      }
    });
  }

  /** ----- Nút Cancel ----- */
  const btnCancel = document.getElementById("btn_cancel");
  if (btnCancel) {
    btnCancel.addEventListener("click", cancel_form);
  }

  /** ----- Nút Update ----- */
  const btnUpdate = document.getElementById("btn_update");
  if (btnUpdate) {
    btnUpdate.addEventListener("click", () => {
      document.getElementById("form_check_password").classList.remove("hidden");
      document.body.classList.add("overflow-hidden");
    });
  }


  const btnSave = document.getElementById("btn_save_profile");
  if (btnSave) {
    btnSave.addEventListener("click", async () => {
      const form = document.getElementById("form_information_profile");
      const formData = new FormData(form);
      formData.append("id", current_user_id);

      showAlert("loading", "Đang lưu", "Vui lòng chờ...");

      try {
        const res = await fetch("/api/update_account", {
          method: "POST",
          body: formData
        });

        const data = await res.json();
        if (data.status === "error") {
          showAlert("error", "Lỗi", data.message);
        } else if (data.status === "success") {
          showAlert("success", "Thông báo", data.message);
          document.getElementById("btn_update").classList.remove("hidden");
          document.getElementById("btn_save_profile").classList.add("hidden");
          update_profile(true);
        }
      } catch (err) {
        console.error(err);
        showAlert("error", "Lỗi", "Server không phản hồi.");
      }
    });
  }


});
