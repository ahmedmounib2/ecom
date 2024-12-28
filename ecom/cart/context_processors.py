from .cart import Cart

# create context processor so the cart is displayed on all sites
def cart(request):
    # Return the default data from our cart
    return {'cart': Cart(request)}