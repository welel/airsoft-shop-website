"""A module contains useful functions.

"""
import datetime

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from main.models import Category, CATEGORY_MODEL
from shopping.models import Cart, CartItem


def get_item(category_slug: str, item_slug: str) -> dict:
    """Gets a ``Item`` instance from database.
    
    TODO: Why is it here?

    """
    root_category = get_object_or_404(Category, slug=category_slug)
    model = CATEGORY_MODEL[root_category.get_root().name]
    item = get_object_or_404(model, slug=item_slug)
    ct = ContentType.objects.get_for_model(item)
    return {'object': item, 'content_type': ct}


def get_cart_item(request, category_slug, item_slug):
    """Gets or creates a ``CartItem`` instance from database."""
    item = get_item(category_slug, item_slug)
    cart_id = request.COOKIES['cart_id']
    cart_item, created = CartItem.objects.get_or_create(
        cart=Cart.objects.get(pk=cart_id),
        content_type=item['content_type'],
        object_id=item['object'].id
    )
    return {'object': cart_item, 'created': created}


def set_cookie(response, key, value, days_expire=7):
    """Sets a key-value pair to response cookies.

    `max_age` equals 30 days.

    """
    max_age = 30 * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=days_expire),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(key, value, max_age=max_age, expires=expires)
