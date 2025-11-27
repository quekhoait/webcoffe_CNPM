def count_order(order):
    total_quantity, total_price = 0,0
    if order:
        
        for o in order.value():
            total_quantity += o['quantity']
            total_price += o['price']*o['quantity']
    return {
        "total_quantity" : total_quantity,
        "total_price" : total_price
    }