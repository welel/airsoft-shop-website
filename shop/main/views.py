from django.shortcuts import render
from .models import LatestItemManager, AmmoItem, GunItem
from django.views.generic import DetailView


def testv(request):
    items = LatestItemManager.get_last_items()
    return render(request, 'index.html', {'items': items})
    
    
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