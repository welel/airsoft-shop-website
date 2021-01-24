"""Module contains useful decorators and functions.

Decorators that get data from database for views:
    get_item
    get_cart_item

"""
import datetime
from functools import wraps

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .models import CartItem, Category, CATEGORY_MODEL


def get_item(view):
    """Adds an instance of subclass of ``Item`` to `request` and calls view.

    Gets `category_slug` and `item_slug` from url and gets ``..Item``
    object by slugs and adds `item` and it's ``ContentType`` to
    `request` additional information. Then sends `request` to a view.

    """
    @wraps(view)
    def wrapper(*args, **kwargs):
        request = args[0]
        category_slug = kwargs['category_slug']
        item_slug = kwargs['item_slug']
        root_category = get_object_or_404(Category, slug=category_slug)
        model = CATEGORY_MODEL[root_category.get_root().name]
        item = get_object_or_404(model, slug=item_slug)
        ct = ContentType.objects.get_for_model(item)
        request.initial_data['item'] = {'object': item, 'content_type': ct}
        return view(request)
    return wrapper


def get_cart_item(view):
    """Adds an instance of ``CartItem`` to `request` and calls view.

    Gets ``CartItem`` or creates new one and adds to `request`
    additional information. Then sends `request` to a view.

    """
    @get_item
    @wraps(view)
    def wrapper(*args):
        request = args[0]
        cart = request.initial_data['cart']
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            content_type=request.initial_data['item']['content_type'],
            object_id=request.initial_data['item']['object'].id
        )
        request.initial_data['cart_item'] = {'cart_item': cart_item,
                                             'created': created}
        return view(request)
    return wrapper


def set_cookie(response, key, value, days_expire=7):
    max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires
    )
