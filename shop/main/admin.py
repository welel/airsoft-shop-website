from django.contrib import admin
from django import forms

from .models import *



class GunCategoryChoiceField(forms.ModelChoiceField):
    pass


class BulletsCategoryChoiceField(forms.ModelChoiceField):
    pass


class GunAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return GunCategoryChoiceField(Category.objects.filter(
                        slug__in=('rifles', 'pistols'))
                        )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BulletsAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return BulletsCategoryChoiceField(Category.objects.filter(
                        slug='bullets')
                        )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(GunItem, GunAdmin)
admin.site.register(BulletsItem, BulletsAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Customer)
