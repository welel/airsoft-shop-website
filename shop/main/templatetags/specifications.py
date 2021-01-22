"""The filter `specifications` forms html code of item details.

There is the filters to form:
    * Other details (item_spec).
    * Features (item_features).

"""
from django import template
from django.utils.safestring import mark_safe

from ..models import GunItem, GearItem, AmmoItem, AccessoryItem


register = template.Library()


SPEC_LIST = '''
    <p class="fs-5 pt-2">Other details:</p>
    <ul class="list-unstyled">
        {rows}
    </ul>
'''
FEATURES_LIST = '''
    <p class="fs-4 pt-2">Features:</p>
    <ul class="">
        {rows}
    </ul>
'''
ROW = '<li class="fs-5">{name}: {value} {metric}</li>'
ROW2 = '<li class="fs-5">{feature}</li>'


ITEM_SPECS = {
    GunItem.category_parent: {
        'power_source': {'label': 'Power source', 'metric': ''},
        'muzzle_velocity': {'label': 'Muzzle velocity', 'metric': 'FPS'},
        'magazine_capacity': {'label': 'Magazine capacity', 'metric': 'BB'}
    },
    AmmoItem.category_parent: {
        'diameter': {'label': 'Diameter', 'metric': 'mm'},
        'quantity': {'label': 'Quantity', 'metric': 'BB'}
    },
    GearItem.category_parent: {},
    AccessoryItem.category_parent: {},
    'All': {
        'color': {'label': 'Color', 'metric': ''},
        'weight': {'label': 'Weight', 'metric': 'lbs'}
    }
}


def get_item_spec(item):
    content = []
    for spec_dict in (ITEM_SPECS[item.category_parent], ITEM_SPECS['All']):
        for field, info in spec_dict.items():
            value = getattr(item, field)
            content.append(ROW.format(name=info['label'], value=value,
                                      metric=info['metric']))
    return '\n'.join(content)


@register.filter
def item_spec(item):
    spec = get_item_spec(item)
    return mark_safe(SPEC_LIST.format(rows=spec))


@register.filter
def item_features(item):
    content = []
    if not item.features:
        return ''
    for feature in item.features:
        content.append(ROW2.format(feature=feature))
    return mark_safe(FEATURES_LIST.format(rows='\n'.join(content)))
