const ROLE_MAPPING = {
    'Quản lý': 'ADMIN',
    'Thu Ngân': 'CASHIER',
    'Nhân Viên': 'STAFF',
    'Thủ Kho': 'WAREHOUSE_KEEPER'
    };

function openModal(mode, staff = null) {
    const modal = document.getElementById('staffModal');
    const modalInner = modal.firstElementChild;

    modal.classList.remove('hidden');
    setTimeout(() => {
        modalInner.classList.remove('scale-95');
        modalInner.classList.add('scale-100');
    }, 10);

    if (mode === 'ADD') {

        document.getElementById('modalTitle').innerText = "Thêm Nhân Viên Mới";

        document.getElementById('inpId').value = "";
        document.getElementById('inpName').value = "";
        document.getElementById('inpPhone').value = "";
        document.getElementById('inpEmail').value = "";
        document.getElementById('inpAddress').value = "";
        document.getElementById('inpRole').value = "STAFF";
        document.getElementById('inpPassword').value = "";

        document.getElementById('passNote').innerText = "(Mặc định: 123456)";
        document.getElementById('statusContainer').classList.add('hidden');

    } else {

        document.getElementById('modalTitle').innerText = "Cập Nhật Thông Tin";

        document.getElementById('inpId').value = staff.id;
        document.getElementById('inpName').value = staff.name;
        document.getElementById('inpPhone').value = staff.phone;
        document.getElementById('inpEmail').value = staff.email || "";
        document.getElementById('inpAddress').value = staff.address || "";


        document.getElementById('inpRole').value = staff.role;

        document.getElementById('inpPassword').value = "";
        document.getElementById('passNote').innerText = "(Để trống nếu không đổi)";

        document.getElementById('statusContainer').classList.remove('hidden');
        document.getElementById('inpActive').checked = staff.status;
    }
}

function closeModal() {
    const modal = document.getElementById('staffModal');
    const modalInner = modal.firstElementChild;
    modalInner.classList.add('scale-95');
    modalInner.classList.remove('scale-100');
    setTimeout(() => { modal.classList.add('hidden'); }, 200);
}



async function saveStaff() {
    const id = document.getElementById('inpId').value;
    const name = document.getElementById('inpName').value.trim();
    const phone = document.getElementById('inpPhone').value.trim();
    const email = document.getElementById('inpEmail').value.trim();
    const address = document.getElementById('inpAddress').value.trim();
    const role = document.getElementById('inpRole').value;
    const password = document.getElementById('inpPassword').value;
    const isActive = document.getElementById('inpActive').checked;

    if (!name || !phone) {
        alert("Vui lòng nhập Tên và Số điện thoại!");
        return;
    }

    const phoneRegex = /^0\d{9}$/;
    if (!phoneRegex.test(phone)) {
        alert("Số điện thoại không hợp lệ (10 số, bắt đầu bằng 0)!");
        return;
    }

    const url = id ? '/api/admin/staff/update' : '/api/admin/staff/add';

    const data = {
        id: id,
        name: name,
        phone: phone,
        email: email,
        address: address,
        role: role,
        password: password,
        active: isActive
    };

    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert("Lỗi: " + result.message);
        }
    } catch (err) {
        alert("Lỗi kết nối Server!");
        console.error(err);
    }
}

function deleteStaff(id) {
    if (!confirm("Bạn có chắc chắn muốn KHÓA tài khoản này?")) return;

    fetch('/api/admin/staff/delete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id})
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert("Lỗi: " + data.message);
        }
    });
}


function searchTable() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase().trim();
    const rows = document.querySelectorAll('#staffTableBody tr');

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
    });
}