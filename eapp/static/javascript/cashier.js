function loadInvoices(params = {}, invoice_type) {
    const paramsURL = new URLSearchParams(params).toString()
    fetch('/api/invoices?' + paramsURL,{
        method : 'get'
    }).then(res =>res.text()).then(data => {
        if(invoice_type == 'online'){

        }else{
            document.querySelector('#invoice-offline div').innerHTML = data
        }
    })
}



