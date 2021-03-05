from .models import Cart, Category, Customer
from .utils import set_cookie


class CategoryMiddleware:
    """A middleware provides root categories to templates.

    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.categories = Category.objects.root_nodes()

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        response.context_data['categories'] = self.categories
        return response


class ShoppingCartMiddleware:
    """A middleware manages a shopping cart (``Cart``).

    A middleware provides `cart_id` for views. If an user is
    authenticated 'cart_id' gets from the database by a customer.
    If an user is anonymous `cart_id` gets from the cookie or
    creates new one.
    After request `cart_id` attaches to the cookie.
    Also a middleware provides a ``Cart`` instance to templates.

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            request.COOKIES['cart_id'] = Cart.objects.get(owner=customer,
                                                          in_order=False).pk
        elif 'cart_id' not in request.COOKIES:
            request.COOKIES['cart_id'] = Cart.objects.create().pk
        response = self.get_response(request)
        if 'cart_id' not in response.cookies:
            set_cookie(response, 'cart_id', request.COOKIES['cart_id'])
        return response

    def process_template_response(self, request, response):
        cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
        response.context_data['cart'] = cart
        return response
