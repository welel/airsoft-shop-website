import operator
from functools import reduce

from django.db.models import Q
from django.template.response import TemplateResponse

from .models import Category, CATEGORY_MODEL, LatestItemManager
from shopping.utils import get_item


def index(request):
    """Renders the home page of the site."""
    items = LatestItemManager.get_last_items()
    return TemplateResponse(request, 'index.html', {'items': items})


def item_details(request, category_slug, item_slug):
    """Renders an item details page."""
    item = get_item(category_slug, item_slug)['object']
    return TemplateResponse(request, 'item_details.html', {'item': item})


# TODO: Read `mptt` docs and find out a better way to filter items.
def items_category(request, category_slug):
    """Renders a page with items by a category."""
    category = Category.objects.get(slug=category_slug)
    root_category = category.get_root()
    model = CATEGORY_MODEL[root_category.name]
    categories = list(category.get_children())
    categories.append(category)
    conditions = reduce(operator.or_, [Q(**{'category': category})
                                       for category in categories])
    items = model.objects.filter(conditions)
    context = {'category': category, 'items': items}
    return TemplateResponse(request, 'category.html', context)
