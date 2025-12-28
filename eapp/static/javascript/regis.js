// Hàm toggle password
function togglePassword(formSelector, inputId, iconId) {
  const form = document.querySelector(formSelector);
  const pw = form.querySelector(`#${inputId}`);
  const icon = form.querySelector(`#${iconId}`);

  icon.addEventListener("click", () => {
    const isPassword = pw.type === "password";
    pw.type = isPassword ? "text" : "password";
    icon.classList.toggle("fa-eye", !isPassword);
    icon.classList.toggle("fa-eye-slash", isPassword);
  });
}

// Gọi hàm cho từng form
togglePassword("#regis-form", "password", "password-toggle-icon");
togglePassword("#regis-form", "confirm", "password-confirm-toggle-icon");


document.getElementById("regis-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const res = await fetch("/api/regis", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  if (data.status === "error") {
    showAlert("error", "Sai mật khẩu", data.message);
  } else if (data.status === "success") {
    window.location.href = "/login";
  }
})



