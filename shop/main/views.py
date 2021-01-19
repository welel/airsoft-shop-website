from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import Http404

from .models import Category, LatestItemManager, AmmoItem, GunItem


def index(request):
    categories = Category.objects.root_nodes()
    items = LatestItemManager.get_last_items()
    context = {
        'items': items,
        'categories': categories
    }
    return render(request, 'index.html', context)


CATEGORY_MODEL = {
        GunItem.category_parent: GunItem,
        AmmoItem.category_parent: AmmoItem,
}


def item_details(request, category, slug):
    root_category = Category.objects.get(name=category).get_root().name
    model = CATEGORY_MODEL[root_category]
    if model:
        item = get_object_or_404(model, slug=slug)
    else:
        raise Http404('Category "{}" does not exist'.format(category))
    return render(request, 'item_details.html', {'item': item})
