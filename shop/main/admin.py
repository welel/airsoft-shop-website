from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import *
from .forms import GunItemForm, AmmoItemForm, GearItemForm, AccessoryItemForm


class GunItemAdmin(admin.ModelAdmin, DynamicArrayMixin):  
    form = GunItemForm


class AmmoItemAdmin(admin.ModelAdmin, DynamicArrayMixin):  
    form = AmmoItemForm


class GearItemAdmin(admin.ModelAdmin, DynamicArrayMixin):  
    form = GearItemForm


class AccessoryItemAdmin(admin.ModelAdmin, DynamicArrayMixin):  
    form = AccessoryItemForm


admin.site.register(Category)
admin.site.register(GunItem, GunItemAdmin)
admin.site.register(AmmoItem, AmmoItemAdmin)
admin.site.register(GearItem, GearItemAdmin)
admin.site.register(AccessoryItem, AccessoryItemAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
