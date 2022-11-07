from itertools import chain

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render

from main.models import GunItem, AmmoItem, GearItem, AccessoryItem


def search_items(request):
    """Handle a search items request.
    
    TODO: Optimize this nonsense.
    """
    query = request.GET.get('query', default='')
    query = SearchQuery(query)
    vector = SearchVector('title', weight='A') + \
             SearchVector('description', weight='B')
    rank = SearchRank(vector, query)

    gun_results = GunItem.objects.annotate(rank=rank)\
        .filter(rank__gte=0.1).order_by('-rank')
    ammo_results = AmmoItem.objects.annotate(rank=rank)\
        .filter(rank__gte=0.1).order_by('-rank')
    gear_results = GearItem.objects.annotate(rank=rank)\
        .filter(rank__gte=0.1).order_by('-rank')
    accessory_results = AccessoryItem.objects.annotate(rank=rank)\
        .filter(rank__gte=0.1).order_by('-rank')
    
    results = list(chain(gun_results, ammo_results, gear_results,
        accessory_results))
    results = sorted(results, key=lambda item: item.rank, reverse=True)
    return render(request, 'search.html', {'results': results})
