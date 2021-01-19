"""The filter `specifications` forms html code of item details.

There is the filters to form:
    * Other details (item_spec).
    * Features (item_features).
"""
from django import template
from django.utils.safestring import mark_safe


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
ROW = '<li class="fs-5">{name}: {value}</li>'
ROW2 = '<li class="fs-5">{feature}</li>'


# TODO: Add able to display FPS, gram, ect. metrics.
ITEM_SPECS = {
    'Airsoft Guns': {
        'Power source': 'power_source',
        'Muzzle velocity': 'muzzle_velocity',
        'Magazine capacity': 'magazine_capacity'
    },
    'BBS & Pellets': {
        'Diameter': 'diameter',
        'Quantity': 'quantity'
    },
    'All': {
        'Color': 'color',
        'Weight': 'weight'
    }
}


# TODO: safer
def get_item_spec(item):
    content = []
    for spec_dict in (ITEM_SPECS[item.category_parent], ITEM_SPECS['All']):
        for name, value in spec_dict.items():
            value = getattr(item, value)
            if not value:
                print(value)
                continue
            content.append(ROW.format(name=name, value=value))
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
