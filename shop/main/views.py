from django.shortcuts import render
from django.views.generic import DetailView

from .models import Category, LatestItemManager, AmmoItem, GunItem



def index(request):
    categories = Category.objects.root_nodes()
    items = LatestItemManager.get_last_items()
    return render(request, 'index.html', {
                                            'items': items,
                                            'categories': categories
                                         }
    )
    
    
class ItemDetailView(DetailView):
    
    CATEGORY_MODEL = {
        GunItem.category_parent: GunItem,
        AmmoItem.category_parent: AmmoItem,
    }
    
    def dispatch(self, request, *args, **kwargs):
        # TODO: OR 404
        root_category = Category.objects.get(
                name=kwargs['category']).get_root().name
        self.model = self.CATEGORY_MODEL[root_category]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
    
    context_object_name = 'product'
    template_name = 'single.html'
    slug_url_kwarg = 'slug'