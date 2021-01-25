"""Views of main application.

Many of views use `request.initial_data` dict.
This dictionary may store:
    customer (Customer) - current customer.
    cart (Cart) - current customer's cart.
    item (Item subclass) - an item taken by url query.
    cart_item (CartItem) - a cart item gotten from database
                           by item or created.
Note that customer and cart available everywhere (initializing in
middleware), but `item` and `cart_item` available only by using
decorators from `.utils` module.

"""
import operator
import uuid
from functools import reduce

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy

from .forms import OrderForm
from .models import (
    AnonymousUser,
    Cart,
    Category,
    Customer,
    CATEGORY_MODEL,
    LatestItemManager,
    Order
)
from .utils import get_cart_item, get_item, set_cookie


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
    """Adds a ``CartItem`` instance to customer's cart."""
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
    """Deletes a ``CartItem`` instance from customer's cart."""
    cart = request.initial_data['cart']
    cart_item, created = request.initial_data['cart_item'].values()
    cart.items.remove(cart_item)
    cart_item.delete()
    cart.save()
    messages.add_message(request, messages.INFO,
                         'Product deleted successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


# TODO: Sort cart items in the cart with respect to item's title.
@get_cart_item
def change_cart_item_quantity(request):
    """Changes quantity of items in a ``CartItem`` instance."""
    cart_item, created = request.initial_data['cart_item'].values()
    cart_item.quantity = int(request.POST.get('cart_item_quantity', 1))
    cart_item.save()
    cart_item.save(update_fields=['quantity'])
    messages.add_message(request, messages.INFO,
                         'Quantity changed successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


@login_required(login_url='signin')
@transaction.atomic
def make_order(request):
    """Handles an order page and POST request.

    GET method: renders order table and order form.
    POST method: validates filled form and creates an order.

    """
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
            return HttpResponseRedirect(reverse('index'))
    else:
        form = OrderForm()
    return TemplateResponse(request, 'checkout.html', {'form': form})


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            response = HttpResponseRedirect(reverse('index'))
            user = form.save()
            customer = Customer.objects.create(registered=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            anon_identifier = request.COOKIES.get('anon_identifier')
            if anon_identifier:
                anon_user = AnonymousUser.objects.get(
                    identifier=anon_identifier)
                anon_customer = Customer.objects.get(anonymous=anon_user)
                cart = Cart.objects.get(owner=anon_customer, in_order=False)
                cart.owner = customer
                cart.save()
                anon_user.delete()
                anon_customer.delete()
                response.delete_cookie('anon_identifier')
            else:
                cart = Cart.objects.create(owner=customer)
            return response
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            response = HttpResponseRedirect(reverse('index'))
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # TODO: add cart items from anonymous cart (and delete anon user)
            response.delete_cookie('anon_identifier')
            return response
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


@login_required()
def logout_(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
