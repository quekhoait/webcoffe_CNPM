
function openModal(mode, staff = null) {
    const modal = document.getElementById('staffModal');

    modal.classList.remove('hidden');

    setTimeout(() => { 
        modal.firstElementChild.classList.remove('scale-95'); 
        modal.firstElementChild.classList.add('scale-100'); 
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

        const roleMap = {
            'Quản lý': 'ADMIN', 'ADMIN': 'ADMIN',
            'Thu Ngân': 'CASHIER', 'CASHIER': 'CASHIER',
            'Nhân Viên': 'STAFF', 'STAFF': 'STAFF',
            'Thủ Kho': 'WAREHOUSE_KEEPER', 'WAREHOUSE_KEEPER': 'WAREHOUSE_KEEPER'
        };
        document.getElementById('inpRole').value = roleMap[staff.role] || 'STAFF';

        document.getElementById('inpPassword').value = ""; 
        document.getElementById('passNote').innerText = "(Để trống nếu không đổi)";
        
        document.getElementById('statusContainer').classList.remove('hidden');
        if(staff.status === false){
            document.getElementById('statusContainer').querySelector('span').innerText="Ngừng hoạt động"
        }else{
            document.getElementById('statusContainer').querySelector('span').innerText="Đang hoạt động"
        }

    }
}

function closeModal() {
    const modal = document.getElementById('staffModal');

    modal.firstElementChild.classList.add('scale-95');
    modal.firstElementChild.classList.remove('scale-100');

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
        alert("Số điện thoại không hợp lệ (Phải bắt đầu bằng 0 và có 10 số)!");
        return;
    }

    const url = id ? '/api/admin/employees/update' : '/api/admin/employees/add';
    
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
        alert("Lỗi kết nối đến Server!");
        console.error(err);
    }
}

function deleteStaff(id) {
    if (!confirm("Bạn có chắc chắn muốn KHÓA tài khoản nhân viên này không?")) return;
    fetch('/api/admin/employees/delete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id})
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        if(data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert("Lỗi: " + data.message);
        }
    })
    .catch(err => {
        alert("Lỗi hệ thống!" + err.message);
        console.error(err);
    });
}

function openStaff(id) {
    if (!confirm("Bạn có chắc chắn muốn mở khóa tài khoản nhân viên này không?")) return;
    fetch('/api/admin/employees/open', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id})
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        if(data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert("Lỗi: " + data.message);
        }
    })
    .catch(err => {
        alert("Lỗi hệ thống!" + err.message);
        console.error(err);
    });
}


function searchTable() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase().trim();

    const currentRole = document.getElementById('roleFilter').value || 'ALL';
    applyFilters(filter, currentRole);
}

function toggleFilterDropdown() {
    document.getElementById('filter-dropdown').classList.toggle('hidden');
}

function selectFilter(val, name) {
    document.getElementById('inpFilterName').value = name;
    document.getElementById('roleFilter').value = val;
    document.getElementById('filter-dropdown').classList.add('hidden');

    const currentSearch = document.getElementById('searchInput').value.toLowerCase().trim();
    applyFilters(currentSearch, val);
}

function applyFilters(keyword, roleVal) {
    const rows = document.querySelectorAll('#staffTableBody tr');

    rows.forEach(row => {

        const textRow = row.innerText.toLowerCase();

        const roleCellText = row.cells[2].innerText.trim(); 

        const matchKeyword = textRow.includes(keyword);
        const matchRole = (roleVal === 'ALL') || (roleCellText === roleVal);

        if (matchKeyword && matchRole) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

document.addEventListener('click', function(e) {
    const container = document.getElementById('filter-container');
    if (container && !container.contains(e.target)) {
        const dropdown = document.getElementById('filter-dropdown');
        if (dropdown) dropdown.classList.add('hidden');
    }
});