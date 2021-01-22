from django import forms

from .models import (
    AccessoryItem,
    AmmoItem,
    Category,
    GearItem,
    GunItem,
    Order
)


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restricts display of non-belonging categories for Item
        category = self.instance.category_parent
        if ('category' in self.fields and 
                Category.objects.filter(name=category).exists()):
            cqs = Category.objects.get(name=category).get_children()
            self.fields['category'].queryset = cqs
        
    class Meta:
        exclude = ('added', 'quantity_sold')


GunItemForm = forms.modelform_factory(GunItem, form=ItemForm)
GearItemForm = forms.modelform_factory(GearItem, form=ItemForm)
AmmoItemForm = forms.modelform_factory(AmmoItem, form=ItemForm)
AccessoryItemForm = forms.modelform_factory(AccessoryItem, form=ItemForm)


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'buying_type',
                  'comment')
