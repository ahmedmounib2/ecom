from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from store.models import Product


def process_order(request):
    if request.method == 'POST':
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()  # Call the function to get cart products
        quantities = cart.get_quants()  # Call the function to get quantities
        totals = cart.cart_total()

        # Get billing info from the form
        payment_form = PaymentForm(request.POST)
        # Get shipping session data 
        my_shipping = request.session.get('my_shipping')

        # gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']         
        amount_paid = totals

        # Create a shipping address from session info
        shipping_address = (
                f"{my_shipping.get('shipping_address', '')}/n"
                f"{my_shipping.get('shipping_city', '')}/n"
                f"{my_shipping.get('shipping_state', '')}/n"
                f"{my_shipping.get('shipping_zipcode', '')}/n"
                f"{my_shipping.get('shipping_country', '')}"
            )

        # create an order
        if request.user.is_authenticated:
            user = request.user
        else:
            # For anonymous users, assign None or some default value to user
            user = None

        create_order = Order.objects.create(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)

        # add order items
        # get the order ID
        order_id = create_order.pk
        for product in cart_products:
            product_id = product.id
            if product.is_sale:
                price = product.sale_price
            else:
                price = product.price

            # get product info
            for key, value in quantities.items():
                if int(key) == product.id:
                    create_order_item = OrderItem(order=create_order, product=product, user=user, quantity=value, price=price)  # Use create_order instead of order_id
                    create_order_item.save()

        # delete our cart after order is processed
        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]
        

        messages.success(request, "Order Placed")
        return redirect('home')
    
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def billing_info(request):
    if request.method == 'POST':
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check if user is logged in
        if request.user.is_authenticated:
            # Get billing information form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":my_shipping, "billing_form":billing_form})
        else:
            # Not logged in
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":my_shipping, "billing_form":billing_form})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
      
    if request.user.is_authenticated:
        # Checkout as logged-in user
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_form = ShippingForm()
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        # Checkout as guest 
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
