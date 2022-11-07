from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy

from .forms import OrderForm
from .models import Cart, CartItem, Order
from .utils import get_cart_item, set_cookie
from user.models import Customer


def customer_cart(request):
    """Renders a page of a customer's cart."""
    cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
    context = {'cart_items': CartItem.objects.filter(cart=cart)}
    return TemplateResponse(request, 'customer_cart.html', context)


def add_to_cart(request, category_slug, item_slug):
    """Adds a ``CartItem`` instance to a cart."""
    cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
    cart_item = get_cart_item(request, category_slug, item_slug)
    cart_item, created = cart_item.values()
    if created:
        cart_item.cart = cart
    else:
        cart_item.quantity += 1
    cart_item.save()
    cart.save()
    messages.info(request, 'Product added successfully.')
    return HttpResponseRedirect(reverse_lazy('index') + '#products')


def delete_from_cart(request, category_slug, item_slug):
    """Deletes a ``CartItem`` instance from a cart."""
    cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
    cart_item = get_cart_item(request, category_slug, item_slug)['object']
    cart_item.delete()
    cart.save()
    messages.info(request, 'Product deleted successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


def clear_cart(request):
    """Deletes all cart items from a cart."""
    cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        cart_item.delete()
    cart.save()
    messages.info(request, 'The cart cleared successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


# TODO: Sort cart items in a cart with respect to a item's title.
def change_cart_item_quantity(request, category_slug, item_slug):
    """Changes quantity of items in a ``CartItem`` instance."""
    cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
    cart_item = get_cart_item(request, category_slug, item_slug)['object']
    cart_item.quantity = int(request.POST.get('cart_item_quantity', 1))
    cart_item.save(update_fields=['quantity', 'total_price'])
    cart.save()
    messages.info(request, 'Quantity changed successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


@login_required(login_url='signin')
@transaction.atomic
def make_order(request):
    """Handles an order page and POST request.

    GET method: renders an order table and order form.
    POST method: validates a filled form and creates an order.

    """
    cart = Cart.objects.get(pk=request.COOKIES['cart_id'])
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        order = Order(customer=customer)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            order.cart = cart
            cart.in_order = True
            cart.save(update_fields=["in_order"])
            order.save()
            new_cart = Cart.objects.create(owner=customer)
            response = HttpResponseRedirect(reverse('index'))
            set_cookie(response, 'cart_id', new_cart.pk)
            messages.info(request, 'Order was added successfully.')
            return HttpResponseRedirect(reverse('index'))
    else:
        cart_items = CartItem.objects.filter(cart=cart)
        context = {'form': OrderForm(), 'cart': cart, 'cart_items': cart_items}
    return TemplateResponse(request, 'checkout.html', context)
