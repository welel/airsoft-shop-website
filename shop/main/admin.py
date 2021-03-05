from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .forms import AccessoryItemForm, AmmoItemForm, GearItemForm, GunItemForm
from .models import (
    AccessoryItem,
    AmmoItem,
    Category,
    GearItem,
    GunItem,
)


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
