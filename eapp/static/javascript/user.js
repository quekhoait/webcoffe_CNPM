
document.getElementById("regis-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Ngăn reload
    const formData = new FormData(e.target);

    const res = await fetch("/api/regis", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    if (data.status === "error") {
        alert(1)
        document.getElementById("error-box").classList.remove("hidden");
        document.getElementById("error-text").innerText = data.message;
    } else if (data.status === "ok") {
      alert(2)
        window.location.href = "/login";
    }
  })