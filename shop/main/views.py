from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.http import Http404

from .models import Category, LatestItemManager, AmmoItem, GunItem


CATEGORY_MODEL = {
        GunItem.category_parent: GunItem,
        AmmoItem.category_parent: AmmoItem,
}


def index(request):
    """Renders the home page of the site."""
    items = LatestItemManager.get_last_items()
    return TemplateResponse(request, 'index.html', {'items': items})


def item_details(request, category, slug):
    """Renders an item details page."""
    root_category = Category.objects.get(name=category).get_root().name
    try:
        model = CATEGORY_MODEL[root_category]
    except KeyError:
        raise Http404('Model category {} does not exist'.format(root_category))
    item = get_object_or_404(model, slug=slug)
    return TemplateResponse(request, 'item_details.html', {'item': item})
