document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Ngăn reload
    const formData = new FormData(e.target);

    const res = await fetch("/api/login", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    if (data.status === "error") {
        document.getElementById("error-login-box").classList.remove("hidden");
        document.getElementById("error-login-text").innerText = data.message;
    } else if (data.status === "success") {
        alert("Đăng nhập thành công")
        window.location.href = data.redirect_url;
    }
  })

  function togglePassword(formSelector, inputId, iconId) {
    const form = document.querySelector(formSelector);
    const pw = form.querySelector(`#${inputId}`);
    const icon = form.querySelector(`#${iconId}`);

    icon.addEventListener("click", () => {
    console.log(form, pw, icon)
        const isPassword = pw.type === "password";
        pw.type = isPassword ? "text" : "password";
        icon.classList.toggle("fa-eye", !isPassword);
        icon.classList.toggle("fa-eye-slash", isPassword);
    });
}
//
togglePassword("#login-form", "password-login", "password-login-toggle-icon");
