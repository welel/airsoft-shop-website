"""Views of main application.

Many of views use `request.initial_data` dict.
This dict may store:
    customer (Customer) - current customer.
    cart (Cart) - current customer's cart.
    item (Item subclass) - an item taken by url query.
    cart_item (CartItem) - a cart item gotten from database
                           by item or created.
Note that customer and cart available everywhere (initializing in
middleware), but item and cart_item available only by using decorators
from `.utils` module.

"""
import operator
from functools import reduce

from django.template.response import TemplateResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from .forms import OrderForm
from .models import CATEGORY_MODEL, Category, LatestItemManager, Order
from .utils import get_item, get_cart_item


def index(request):
    """Renders the home page of the site."""
    items = LatestItemManager.get_last_items()
    return TemplateResponse(request, 'index.html', {'items': items})


@get_item
def item_details(request):
    """Renders an item details page."""
    context = {'item': request.initial_data['item']['object']}
    return TemplateResponse(request, 'item_details.html', context)


# TODO: Read `mptt` docs and find out a better way to filter items.
def items_category(request, category_slug):
    """Renders a page with items by category."""
    category = Category.objects.get(slug=category_slug)
    root_category = category.get_root()
    model = CATEGORY_MODEL[root_category.name]
    categories = list(category.get_children())
    categories.append(category)
    conditions = reduce(operator.or_, [Q(**{"category": category})
                                       for category in categories])
    items = model.objects.filter(conditions)
    context = {'category': category, 'items': items}
    return TemplateResponse(request, 'category.html', context)


def customer_cart(request):
    """Renders a page with customer's cart."""
    return TemplateResponse(request, 'customer_cart.html', {})


@get_cart_item
def add_to_cart(request):
    """Adds a `CartItem` to customer's cart."""
    cart = request.initial_data['cart']
    cart_item, created = request.initial_data['cart_item'].values()
    if created:
        cart.items.add(cart_item)
    else:
        cart_item.quantity += 1
        cart_item.save()
    cart.save()
    messages.add_message(request, messages.INFO, 'Product added successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


@get_cart_item
def delete_from_cart(request):
    """Deletes a `CartItem` from customer's cart."""
    cart = request.initial_data['cart']
    cart_item, created = request.initial_data['cart_item'].values()
    cart.items.remove(cart_item)
    cart_item.delete()
    cart.save()
    messages.add_message(request, messages.INFO,
                         'Product deleted successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


# TODO: Sort cart items in the cart with respect to '?'(decide later).
@get_cart_item
def change_cart_item_quantity(request):
    cart = request.initial_data['cart']
    cart_item, created = request.initial_data['cart_item'].values()
    cart_item.quantity = int(request.POST.get('cart_item_quantity', 1))
    cart_item.save()
    cart.save()
    messages.add_message(request, messages.INFO,
                         'Quantity changed successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


@transaction.atomic
def make_order(request):
    if request.method == 'POST':
        order = Order(customer=request.initial_data['customer'])
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            cart = request.initial_data['cart']
            order.cart = cart
            cart.in_order = True
            cart.save(update_fields=["in_order"])
            order.save(update_fields=["cart"])
            request.initial_data['customer'].orders.add(order)
            messages.add_message(request, messages.SUCCESS,
                                 'Order was added successfully.')
            return HttpResponseRedirect('/')
    else:
        form = OrderForm()
    return TemplateResponse(request, 'checkout.html', {'form': form})
