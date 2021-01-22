import operator
from functools import reduce

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db import transaction

from .forms import OrderForm
from .models import (
    Category,
    LatestItemManager,
    AmmoItem,
    GunItem,
    AccessoryItem,
    GearItem,
    CartItem,
    Order
)


CATEGORY_MODEL = {
    GunItem.category_parent: GunItem,
    AmmoItem.category_parent: AmmoItem,
    AccessoryItem.category_parent: AccessoryItem,
    GearItem.category_parent: GearItem,
}


def index(request):
    """Renders the home page of the site."""
    items = LatestItemManager.get_last_items()
    return TemplateResponse(request, 'index.html', {'items': items})


def item_details(request, category_slug, item_slug):
    """Renders an item details page."""
    root_category = Category.objects.get(slug=category_slug).get_root().name
    model = CATEGORY_MODEL[root_category]
    item = get_object_or_404(model, slug=item_slug)
    return TemplateResponse(request, 'item_details.html', {'item': item})


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


# TODO: Merge add/delete `CartItem` views with a decorator.
def add_to_cart(request, category_slug, item_slug):
    """Adds a `CartItem` to customer's cart."""
    root_category = Category.objects.get(slug=category_slug).get_root().name
    item = get_object_or_404(CATEGORY_MODEL[root_category], slug=item_slug)
    ct = ContentType.objects.get_for_model(item)
    cart = request.initial_data['cart']
    cart_item, created = CartItem.objects.get_or_create(
        customer=cart.owner, cart=cart, content_type=ct, object_id=item.id,
    )
    if created:
        cart.items.add(cart_item)
    else:
        cart_item.quantity += 1
        cart_item.save()
    cart.save()
    messages.add_message(request, messages.INFO, 'Product added successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


def delete_from_cart(request, category_slug, item_slug):
    """Deletes a `CartItem` from customer's cart."""
    cart = request.initial_data['cart']
    root_category = Category.objects.get(slug=category_slug).get_root().name
    item = get_object_or_404(CATEGORY_MODEL[root_category], slug=item_slug)
    ct = ContentType.objects.get_for_model(item)
    cart_item = CartItem.objects.get(customer=cart.owner, cart=cart,
                                     content_type=ct, object_id=item.id)
    cart.items.remove(cart_item)
    cart_item.delete()
    cart.save()
    messages.add_message(request, messages.INFO,
                         'Product deleted successfully.')
    return HttpResponseRedirect(reverse_lazy('customer_cart'))


# TODO: Sort cart items in the cart with respect to '?'(decide later).
def change_cart_item_quantity(request, category_slug, item_slug):
    root_category = Category.objects.get(slug=category_slug).get_root().name
    item = get_object_or_404(CATEGORY_MODEL[root_category], slug=item_slug)
    ct = ContentType.objects.get_for_model(item)
    cart = request.initial_data['cart']
    cart_item = CartItem.objects.get(customer=cart.owner, cart=cart,
                                     content_type=ct, object_id=item.id)
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
