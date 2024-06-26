from .models import ProductStock


class Cart:
    def __init__(self, req):
        self.session = req.session
        cart = self.session.get('session_key', {})
        self.cart = cart
        # Ensure cart is saved in the session
        self.session['session_key'] = cart

    def add_item(self, product):
        # Convert product ID to string for consistency
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
        else:
            if product.is_promoted:
                self.cart[product_id] = {
                    'price': str(product.promo_price), 'quantity': 1}
            else:
                self.cart[product_id] = {
                    'price': str(product.price), 'quantity': 1}

        self.session.modified = True  # Mark the session as modified to ensure it is saved

    def remove_item(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]

        self.session.modified = True  # Mark the session as modified to ensure it is saved

    def clear_item(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True  # Mark the session as modified to ensure it is saved

    def __len__(self):
        # Return the total number of items in the cart
        return sum(item['quantity'] for item in self.cart.values())

    def get_cart_items(self):
        product_ids = self.cart.keys()
        products = ProductStock.objects.filter(id__in=product_ids)
        cart_items = []
        for product in products:
            item = {
                'product': product,
                'quantity': self.cart[str(product.id)]['quantity'],
                'total_price': int(self.cart[str(product.id)]['price']) * self.cart[str(product.id)]['quantity']
            }
            cart_items.append(item)
        return cart_items

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear_cart(self):
        self.session['session_key'] = {}
        self.session.modified = True
