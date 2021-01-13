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
    
    
class ProductDetailView(DetailView):
    
    CT_MODEL_MODEL_CLASS = {
        'guns': GunItem,
        'ammo': AmmoItem,
    }
    
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
    
    context_object_name = 'product'
    template_name = 'single.html'
    slug_url_kwarg = 'slug'