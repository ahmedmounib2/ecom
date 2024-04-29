from store.models import Product, Profile
class Cart():
    def __init__(self,request):
        self.session = request.session
        # Get request
        self.request = request

        # Get the current session if it exists
        cart = self.session.get('cart')

        # if the user is new, no cart! create one !
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart



    def add(self, product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified= True

        # deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save carty to profile model
            current_user.update(old_cart=str(carty))


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()
        # use ids to lookup products in dataase model
        products = Product.objects.filter(id__in=product_ids)
       
        # return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get cart
        ourcart = self.cart
        # update dictionaries
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart

        return thing
    
    def delete(self,product):
        product_id = str(product)
        # delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def cart_total(self):
        # get product IDs
        product_ids = self.cart.keys()
        # look up those keys in products database Model
        products = Product.objects.filter(id__in=product_ids)
        # get quantities
        quantities = self.cart
        
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total
