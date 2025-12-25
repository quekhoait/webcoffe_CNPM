document.addEventListener("click", async (e) => {
    const deleteBtn = e.target.closest(".delete-btn");
    if (!deleteBtn) return;

    const ruleId = deleteBtn.dataset.id;
    if (!confirm("Xóa quy định này?")) return;

    const res = await fetch(`/rules/${ruleId}`, {
        method: "DELETE",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    });

    if (res.ok) {
        document.querySelector(`.rule-row[data-id="${ruleId}"]`).remove();
    } else {
        alert("Xóa thất bại");
    }
});


document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {

        document.querySelector("#crud-modal h3").innerText = "Chỉnh sửa quy định"

        const form = document.getElementById("rule-form")
        const ruleId = btn.dataset.id
        form.action = `/rule/${ruleId}/update`

        document.getElementById("name").value = btn.dataset.name
        document.getElementById("value").value = btn.dataset.value
        document.getElementById("unit").value = btn.dataset.unit
        document.getElementById("rule_type").value = btn.dataset.type
        document.getElementById("description").value = btn.dataset.desc
        document.getElementById("active").value = btn.dataset.active
    })
})


document.getElementById("create-rule-btn").addEventListener("click", () => {
    document.querySelector("#crud-modal h3").innerText = "Thêm quy định mới"

    const form = document.getElementById("rule-form")
    form.action = "/rule"
    form.reset()
})