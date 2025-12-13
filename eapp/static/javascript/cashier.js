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

