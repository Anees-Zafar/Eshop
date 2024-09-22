from django import template
from store.models import Products
register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product , cart):
    key=cart.keys()
    for id in key:
        if int(id)==product.id:
            return True
        
    return False

@register.filter(name='is_in_cart')
def is_exist_cart(product , cart):
    key=cart.keys()
    
    if key:
        return True
           
        
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product , cart):
    key=cart.keys()
    for id in key:
        if int(id)==product.id:
            return cart.get(id)
        
    return 0



@register.filter(name='price_total')
def price_total(product , cart):
    return product.price * cart_quantity(product , cart)
    

@register.filter(name='cart_total')
def cart_total(product,cart):
    total_sum = 0
    for id  in product:
        total_sum += price_total(id, cart)

    return total_sum


@register.filter(name='order_product_total')
def order_product_total(num1,num2):
    return num1 * num2
    
@register.filter(name='cart_total_quantity')
def cart_total_quantity(cart):
    if isinstance(cart, dict):  
        total_quantity = 0
        for quantity in cart.values():
            total_quantity += quantity
        return total_quantity
    return 0 



@register.filter(name='is_on_cart')
def is_on_cart(product, cart):
    product_id = str(product.id)
    if product_id in cart:
        return True
    return False