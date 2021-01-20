import operator
from functools import reduce

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.db.models import Q

from .models import (
    Category,
    LatestItemManager,
    AmmoItem,
    GunItem,
    AccessoryItem,
    GearItem,
    Customer,
    Cart
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
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, owner=customer)
    context = {'customer': customer, 'cart': cart}
    return TemplateResponse(request, 'customer_cart.html', context)
