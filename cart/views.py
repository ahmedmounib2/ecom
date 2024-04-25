from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals":totals})


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        
        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = len(cart)

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product Added To Cart...")
        return response


def cart_update(request):
    if request.method == 'POST' and 'product_qty' in request.POST:
        try:
            # Get the product ID and quantity from the POST request
            product_id = int(request.POST.get('product_id'))
            product_qty_str = request.POST.get('product_qty')

            # Check if the quantity string is not empty
            if product_qty_str.strip():
                product_qty = int(product_qty_str)
            else:
                # If quantity is empty, raise a ValueError
                raise ValueError("Product quantity is empty")

            # Update the cart with the new quantity
            cart = Cart(request)  # Instantiate the Cart class with the request object
            cart.update(product=product_id, quantity=product_qty)

            # Prepare JSON response
            response = JsonResponse({'qty': product_qty})

            # Optionally, you can redirect to another page or display a success message
            # return redirect('cart_summary')
            messages.success(request, "Your Cart Has Been Updated...")

            return response
        except ValueError as e:
            # Handle the ValueError (e.g., log the error, return an error response)
            return JsonResponse({'error': str(e)}, status=400)


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST' and 'product_id' in request.POST:
        # Get product ID from POST data
        product_id = int(request.POST.get('product_id'))
        # Call delete function in cart
        cart.delete(product=product_id)
        # Prepare JSON response
        response = JsonResponse({'success': 'Product removed from cart successfully'})
        messages.success(request, "Item Deleted From Shopping Cart...")

        return response
    else:
        # If product ID is not found in POST data, return an error response
        response = JsonResponse({'error': 'Product ID not provided or invalid'})
        response.status_code = 400
        return response
