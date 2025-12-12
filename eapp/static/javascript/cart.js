const my_current_cart=document.querySelectorAll('.cart-component-item');
  setupQuantityControl(my_current_cart);
  setupCheckboxEvents(my_current_cart);   // thêm dòng này !!!
  calculateSubtotal(my_current_cart);