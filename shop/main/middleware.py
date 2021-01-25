import uuid

from .models import AnonymousUser, Cart, Category, Customer
from .utils import set_cookie


class AddContextMiddleware:
    """A middleware provides additional info to views and templates.

    Before: adds ``Customer`` and ``Cart`` to `request`.
    After: adds `categories`, `cart`, `customer` to template context.

    """
    anon_created = False

    def __init__(self, get_response):
        self.get_response = get_response
        self.categories = Category.objects.root_nodes()

    def __call__(self, request):
        if request.user.is_authenticated:
            # Gets a customer and a cart by a registered user
            print('REGISTERED')
            self.customer = Customer.objects.get(registered=request.user)
            self.cart = Cart.objects.get(owner=self.customer, in_order=False)
        elif 'anon_identifier' in request.COOKIES:
            print('ANON')
            # Gets a customer and a cart by an anonymous user
            self.anon_identifier = request.COOKIES.get('anon_identifier')
            user = AnonymousUser.objects.get(identifier=self.anon_identifier)
            self.customer = Customer.objects.get(anonymous=user)
            self.cart = Cart.objects.get(owner=self.customer, in_order=False)
        else:
            # Creates an anonymous user and a cart
            print('FIRST TIME')
            self.anon_identifier = uuid.uuid4()
            self.anon_created = True
            user = AnonymousUser.objects.create(
                identifier=self.anon_identifier)
            self.customer = Customer.objects.create(anonymous=user)
            self.cart = Cart.objects.create(owner=self.customer)
        request.initial_data = {'customer': self.customer, 'cart': self.cart}
        response = self.get_response(request)
        if self.anon_created:
            self.anon_created = False
            set_cookie(response, 'anon_identifier', self.anon_identifier)
        return response

    def process_template_response(self, request, response):
        response.context_data['categories'] = self.categories
        response.context_data['cart'] = self.cart
        response.context_data['customer'] = self.customer
        return response
