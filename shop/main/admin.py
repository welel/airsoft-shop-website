from django.contrib import admin
from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from .models import *



# TODO: SimpleArrayField(forms.CharField(max_length=100))
class GunAdmin(admin.ModelAdmin):  

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name == 'category' and 
                Category.objects.filter(name='Airsoft Guns').exists()):
            qsc = Category.objects.get(name='Airsoft Guns').get_children()
            return forms.ModelChoiceField(qsc)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AmmoAdmin(admin.ModelAdmin):  
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name == 'category' and 
                Category.objects.filter(name='BBS & Pellets').exists()):
            qsc = Category.objects.get(name='BBS & Pellets').get_children()
            return forms.ModelChoiceField(qsc)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class GearAdmin(admin.ModelAdmin):  
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name == 'category' and 
                Category.objects.filter(name='Tactical Gear').exists()):
            qsc = Category.objects.get(name='Tactical Gear').get_children()
            return forms.ModelChoiceField(qsc)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AccessoryAdmin(admin.ModelAdmin):  
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name == 'category' and 
                Category.objects.filter(name='Accessories').exists()):
            qsc = Category.objects.get(name='Accessories').get_children()
            return forms.ModelChoiceField(qsc)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(GunItem, GunAdmin)
admin.site.register(AmmoItem, AmmoAdmin)
admin.site.register(GearItem, GearAdmin)
admin.site.register(AccessoryItem, AccessoryAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Customer)
