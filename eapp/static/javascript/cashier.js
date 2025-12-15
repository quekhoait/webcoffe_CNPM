let currentInvoiceType = 'offline'
let currentInvoiceStatus = 'all'

function loadInvoices() {
    const paramsURL = new URLSearchParams()
    paramsURL.append('invoice_type', currentInvoiceType)
    if (currentInvoiceStatus != 'all') {
        paramsURL.append('invoice_status', currentInvoiceStatus)
    }
    fetch('/api/invoices?' + paramsURL, {
        method: 'get'
    }).then(res => res.text()).then(data => {
        if (currentInvoiceType == 'online') {
            document.querySelector('#invoice-online div').innerHTML = data
        } else {
            document.querySelector('#invoice-offline div').innerHTML = data
        }
    })
}

function LoadInvoiceOffline() {
    currentInvoiceType = 'offline'
    renderStatusBar({ 'invoice_type': currentInvoiceType })
    loadInvoices()
}

function loadInvoiceOnline() {
    currentInvoiceType = 'online'
    renderStatusBar({ 'invoice_type': currentInvoiceType })
    loadInvoices()
}

function renderStatusBar(params = {}) {
    const param = new URLSearchParams(params).toString()
    fetch('/cashier/status-bar?' + param, {
        method: 'get'
    }).then(res => res.text()).then(data => {
        document.getElementById('status-bar').innerHTML = data
        bindStatusEvent()
    })
}

function filterInvoiceByStatus(invoice_status) {
    currentInvoiceStatus = invoice_status
    loadInvoices()
}

bindStatusEvent()

function bindStatusEvent() {
    const statusNavigation = document.querySelectorAll('#status-navigation button')

    statusNavigation.forEach(btn => {
        btn.addEventListener('click', () => {
            statusNavigation.forEach(btn => {
                btn.classList.remove('active-status')
            })

            btn.classList.add('active-status')

            filterInvoiceByStatus(btn.dataset.status)
        })
    })
}

document.addEventListener('click', (e) => {
    const card = e.target.closest('.invoice-card')
    if (!card) return;

    const invoiceId = card.dataset.id
    document.querySelectorAll('.invoice-card').forEach(card => {
        card.classList.remove('active-invoice-card')
    });

    card.classList.add('active-invoice-card')
    viewInvoiceDetail(invoiceId)
})

function viewInvoiceDetail(invoiceId) {
    fetch('/api/invoice-detail?invoice_id=' + invoiceId, {
        method: 'get'
    }).then(res => res.text()).then(data => {
        document.getElementById('invoice-detail').innerHTML = data
    })
}

function updateInvoiceStatus(invoiceId, invoiceStatus) {
    fetch('/api/invoices', {
        method: 'patch',
        body: JSON.stringify({
            'invoice_id': invoiceId,
            'invoice_status': invoiceStatus
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data['success']) {
            loadInvoices()
        }
        alert(data['message'])
    })
}