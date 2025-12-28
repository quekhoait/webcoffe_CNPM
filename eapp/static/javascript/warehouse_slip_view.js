document.getElementById('list-slip').querySelectorAll('.slip').forEach(slip => {
    slip.addEventListener('click', (e) =>{
        alert(q.data.id)
        // fetch('/render_view_slip_detail').then(res => res.text()).then(data => {
        //     console.log(data);
        // })
    })
})