from .models import Cart, Category, Customer


class AddContextMiddleware:
    """A middleware provides additional info to views and templates.

    Before: adds ``Customer`` and ``Cart`` to `request`.
    After: adds `categories`, `cart`, `customer` to template context.

    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.categories = Category.objects.root_nodes()

    def __call__(self, request):
        # TODO: if_auth
        self.customer, created = Customer.objects.get_or_create(
            user=request.user)
        self.cart, created = Cart.objects.get_or_create(owner=self.customer,
                                                        in_order=False)
        request.initial_data = {'customer': self.customer, 'cart': self.cart}
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        response.context_data['categories'] = self.categories
        response.context_data['cart'] = self.cart
        response.context_data['customer'] = self.customer
        return response
